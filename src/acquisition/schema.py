"""
4D-MGRFF Acquisition & Schema Layer
Enforces point-in-time publication timestamps and zero-lookahead data leakage.
Uses built-in SQLite3 for the provenance database backend.
"""

from dataclasses import dataclass
from datetime import datetime
import sqlite3
from typing import List, Optional
import pandas as pd

PROVENANCE_SCHEMA_SQLITE = """
CREATE TABLE IF NOT EXISTS global_risk_provenance (
    observation_id TEXT PRIMARY KEY,
    event_time TEXT NOT NULL,
    publication_time TEXT NOT NULL,
    first_available_timestamp TEXT NOT NULL,
    revision_timestamp TEXT,
    forecast_origin TEXT,
    horizon INTEGER,
    source TEXT NOT NULL,
    source_version TEXT NOT NULL,
    domain TEXT NOT NULL,
    country TEXT,
    region TEXT,
    indicator TEXT NOT NULL,
    raw_value REAL,
    transformed_value REAL,
    unit TEXT,
    transformation TEXT,
    missing_flag INTEGER DEFAULT 0,
    revision_flag INTEGER DEFAULT 0,
    eligibility_at_origin INTEGER DEFAULT 1,
    outcome REAL
);

CREATE INDEX IF NOT EXISTS idx_first_avail ON global_risk_provenance(first_available_timestamp);
CREATE INDEX IF NOT EXISTS idx_domain_ind ON global_risk_provenance(domain, indicator);
"""


@dataclass
class PointInTimeRecord:
    observation_id: str
    event_time: datetime
    publication_time: datetime
    first_available_timestamp: datetime
    source: str
    source_version: str
    domain: str
    indicator: str
    raw_value: float
    transformed_value: Optional[float] = None
    revision_timestamp: Optional[datetime] = None
    country: Optional[str] = None
    region: Optional[str] = None
    unit: Optional[str] = None
    transformation: Optional[str] = None
    missing_flag: bool = False
    revision_flag: bool = False


class PointInTimeDatabase:
    """Database managing point-in-time records with strict leakage verification."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.executescript(PROVENANCE_SCHEMA_SQLITE)

    def insert_records(self, records: List[PointInTimeRecord]):
        """Bulk insert records into provenance table."""
        cursor = self.conn.cursor()
        data = []
        for r in records:
            data.append(
                (
                    r.observation_id,
                    r.event_time.isoformat(),
                    r.publication_time.isoformat(),
                    r.first_available_timestamp.isoformat(),
                    r.revision_timestamp.isoformat() if r.revision_timestamp else None,
                    r.source,
                    r.source_version,
                    r.domain,
                    r.country,
                    r.region,
                    r.indicator,
                    r.raw_value,
                    r.transformed_value,
                    r.unit,
                    r.transformation,
                    1 if r.missing_flag else 0,
                    1 if r.revision_flag else 0,
                )
            )
        cursor.executemany(
            """
            INSERT OR REPLACE INTO global_risk_provenance (
                observation_id, event_time, publication_time, first_available_timestamp,
                revision_timestamp, source, source_version, domain, country, region,
                indicator, raw_value, transformed_value, unit, transformation,
                missing_flag, revision_flag
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            data,
        )
        self.conn.commit()

    def get_eligible_slice(
        self, forecast_origin: datetime, start_date: Optional[datetime] = None, domains: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Extract data strictly available prior to or at forecast origin t.
        Enforces Section 10.4: I_t = { x : first_available_timestamp(x) <= forecast_origin }.
        """
        origin_iso = forecast_origin.isoformat()
        query = """
            SELECT
                observation_id,
                event_time,
                first_available_timestamp,
                domain,
                indicator,
                COALESCE(transformed_value, raw_value) AS value
            FROM global_risk_provenance
            WHERE first_available_timestamp <= ?
        """
        params = [origin_iso]

        if start_date:
            query += " AND event_time >= ?"
            params.append(start_date.isoformat())

        if domains:
            placeholders = ",".join(["?"] * len(domains))
            query += f" AND domain IN ({placeholders})"
            params.extend(domains)

        query += " ORDER BY event_time ASC, indicator ASC"
        df = pd.read_sql_query(query, self.conn, params=params)
        if not df.empty:
            df["first_available_timestamp"] = pd.to_datetime(df["first_available_timestamp"])
            df["event_time"] = pd.to_datetime(df["event_time"])
        return df

    def assert_zero_leakage(self, df: pd.DataFrame, forecast_origin: datetime):
        """
        Verification assertion: raises error if any observation leaked into dataset.
        """
        if df.empty:
            return True
        first_avail = pd.to_datetime(df["first_available_timestamp"])
        leaks = df[first_avail > forecast_origin]
        if not leaks.empty:
            raise ValueError(
                f"POINT-IN-TIME LEAKAGE DETECTED: {len(leaks)} records have "
                f"first_available_timestamp > {forecast_origin}"
            )
        return True

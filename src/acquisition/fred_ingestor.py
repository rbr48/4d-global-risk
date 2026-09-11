"""
4D-MGRFF FRED Data Ingestor
Fetches high-frequency macroeconomic proxies and market benchmarks from St. Louis Fed.
Zero API key requirement (uses open FRED CSV endpoints).
"""

from datetime import timedelta
import io
from typing import Dict, List
import urllib.request
import pandas as pd

from .schema import PointInTimeRecord

FRED_CORE_SERIES: Dict[str, Dict[str, str]] = {
    "T10Y2Y": {
        "domain": "Economics",
        "description": "10-Year Minus 2-Year Treasury Yield Spread",
        "unit": "Percent",
        "pub_delay_hours": "18",  # Released end of business day
    },
    "T5YIFR": {
        "domain": "Economics",
        "description": "5-Year 5-Year Forward Inflation Expectation Rate",
        "unit": "Percent",
        "pub_delay_hours": "18",
    },
    "BAMLH0A0HYM2": {
        "domain": "Finance",
        "description": "ICE BofA US High Yield Index Option-Adjusted Spread",
        "unit": "Percent",
        "pub_delay_hours": "24",  # Published next morning (T+1)
    },
    "VIXCLS": {
        "domain": "Finance",
        "description": "CBOE Volatility Index (VIX)",
        "unit": "Index",
        "pub_delay_hours": "18",
    },
    "DCOILBRENTEU": {
        "domain": "Economics",
        "description": "Crude Oil Prices: Brent - Europe",
        "unit": "USD per Barrel",
        "pub_delay_hours": "24",
    },
    "DTWEXBGS": {
        "domain": "Economics",
        "description": "Nominal Broad U.S. Dollar Index",
        "unit": "Index",
        "pub_delay_hours": "24",
    },
}


class FREDIngestor:
    """Fetches and converts FRED series to point-in-time timestamped records."""

    def __init__(self, base_url: str = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="):
        self.base_url = base_url

    def fetch_series_dataframe(self, series_id: str, timeout: int = 15) -> pd.DataFrame:
        """Downloads raw CSV from St. Louis Fed."""
        url = f"{self.base_url}{series_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (4D-MGRFF-Research-Pipeline)"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read().decode("utf-8")
                df = pd.read_csv(io.StringIO(content))
                # FRED CSV format: DATE, {SERIES_ID}
                df.columns = ["date", "val"]
                df["val"] = pd.to_numeric(df["val"], errors="coerce")
                df = df.dropna().reset_index(drop=True)
                df["date"] = pd.to_datetime(df["date"])
                return df
        except Exception as e:
            raise RuntimeError(f"Failed to fetch series {series_id} from FRED: {e}")

    def convert_to_records(
        self, series_id: str, df: pd.DataFrame, source_version: str = "FRED_2026"
    ) -> List[PointInTimeRecord]:
        """
        Converts raw date/val rows into PointInTimeRecord enforcing publication delay.
        """
        meta = FRED_CORE_SERIES.get(series_id, {"domain": "Economics", "unit": "Index", "pub_delay_hours": "24"})
        domain = meta["domain"]
        delay_hrs = int(meta.get("pub_delay_hours", 24))

        records = []
        for _, row in df.iterrows():
            event_date = row["date"].to_pydatetime()
            # Publication time accounts for market close / release delay
            pub_time = event_date + timedelta(hours=delay_hrs)
            first_avail = pub_time  # First moment data enters information set

            obs_id = f"FRED_{series_id}_{event_date.strftime('%Y%m%d')}"
            rec = PointInTimeRecord(
                observation_id=obs_id,
                event_time=event_date,
                publication_time=pub_time,
                first_available_timestamp=first_avail,
                source="FRED",
                source_version=source_version,
                domain=domain,
                indicator=series_id,
                raw_value=float(row["val"]),
                unit=meta.get("unit", "Index"),
                missing_flag=False,
                revision_flag=False,
            )
            records.append(rec)

        return records

"""
4D-MGRFF Live FRED Ingestion Script
Fetches live historical data for core macroeconomic and financial proxies from St. Louis Fed
and stores them into the point-in-time database.
"""

import os
from datetime import datetime
import pandas as pd

from src.acquisition.schema import PointInTimeDatabase
from src.acquisition.fred_ingestor import FREDIngestor, FRED_CORE_SERIES


def ingest_live_fred_data(db_path: str = "data/processed/global_risk_database.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    db = PointInTimeDatabase(db_path=db_path)
    ingestor = FREDIngestor()
    
    total_records = 0
    print("=" * 65)
    print(" 4D-MGRFF: INGESTING LIVE POINT-IN-TIME MACROECONOMIC DATA (FRED) ")
    print("=" * 65)
    
    for series_id, meta in FRED_CORE_SERIES.items():
        print(f"\nFetching series: {series_id} ({meta['description']})...")
        try:
            df = ingestor.fetch_series_dataframe(series_id=series_id, timeout=12)
            records = ingestor.convert_to_records(series_id=series_id, df=df)
            db.insert_records(records)
            total_records += len(records)
            date_range = f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}"
            print(f"  -> Ingested {len(records)} records ({date_range})")
        except Exception as e:
            print(f"  -> Warning: Could not fetch {series_id} ({e})")
            
    print("\n" + "=" * 65)
    print(f" SUCCESS: Total {total_records} point-in-time records archived in {db_path}!")
    print("=" * 65)


if __name__ == "__main__":
    ingest_live_fred_data()

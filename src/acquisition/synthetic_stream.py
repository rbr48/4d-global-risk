"""
4D-MGRFF Synthetic & Hybrid Multidisciplinary Stream Generator
Generates realistic point-in-time panels across all 5 domains with known cross-domain propagation.
"""

from datetime import datetime, timedelta
from typing import List, Tuple
import numpy as np
import pandas as pd

from .schema import PointInTimeRecord


def generate_calibrated_multidisciplinary_panel(
    start_date: datetime = datetime(2020, 1, 1),
    num_days: int = 500,
    seed: int = 42
) -> Tuple[pd.DataFrame, List[PointInTimeRecord]]:
    """
    Simulates a 5-domain daily global risk system:
        - Geopolitics: Conflict events, diplomatic friction (ACLED/GDELT style)
        - Economics: Inflation breakeven, yield spread (FRED style)
        - Finance: VIX, credit spread
        - Technology: AI incident velocity, export restrictions
        - Climate: Temperature anomalies, severe weather index
        
    Embeds realistic multi-step propagation:
        Geopolitical shock at t -> Energy spike at t+1 -> Financial stress at t+2.
    """
    np.random.seed(seed)
    
    dates = [start_date + timedelta(days=i) for i in range(num_days)]
    
    # 1. Latent shock processes
    # Latent systemic global factor F_t (AR(1))
    f_t = np.zeros(num_days)
    rho = 0.85
    for t in range(1, num_days):
        # occasional jump shocks
        jump = np.random.choice([0.0, 3.0], p=[0.97, 0.03])
        f_t[t] = rho * f_t[t-1] + np.random.normal(0, 0.3) + jump

    # 2. Domain-specific series with propagation lags
    # Geopolitics (leads systemic cascades)
    geo_conflict = np.maximum(0, 15.0 + 8.0 * f_t + np.random.normal(0, 2.0, num_days))
    geo_news_salience = np.maximum(0.001, 0.02 + 0.015 * f_t + np.random.normal(0, 0.005, num_days))
    
    # Energy / Commodities (reacts to geopolitics with 1-day lag)
    energy_vol = np.zeros(num_days)
    energy_vol[0] = 2.0
    for t in range(1, num_days):
        energy_vol[t] = 0.7 * energy_vol[t-1] + 0.3 * (geo_conflict[t-1] / 10.0) + np.random.normal(0, 0.4)
    energy_vol = np.maximum(0.5, energy_vol)
    
    # Finance / VIX (reacts to energy and systemic factor with 2-day lag)
    vix = np.zeros(num_days)
    vix[0] = 16.0
    for t in range(2, num_days):
        vix[t] = 0.6 * vix[t-1] + 0.2 * energy_vol[t-1] + 3.5 * f_t[t] + np.random.normal(0, 0.8)
    vix = np.maximum(10.0, vix)
    
    # Economics (High-yield spread)
    hy_spread = np.maximum(2.0, 3.5 + 0.15 * vix + np.random.normal(0, 0.2, num_days))
    
    # Technology / AI velocity
    tech_velocity = np.maximum(0, 5.0 + 2.0 * f_t + np.random.normal(0, 1.5, num_days))
    
    # Climate anomaly
    climate_anomaly = np.random.normal(0.8, 0.3, num_days) + 0.1 * np.sin(np.linspace(0, 8, num_days))
    
    # Assemble into DataFrame
    df = pd.DataFrame({
        "date": dates,
        "geo_conflict": geo_conflict,
        "geo_news_salience": geo_news_salience,
        "energy_vol": energy_vol,
        "vix": vix,
        "hy_spread": hy_spread,
        "tech_velocity": tech_velocity,
        "climate_anomaly": climate_anomaly
    })
    
    # Convert to PointInTimeRecord list
    records = []
    domain_map = {
        "geo_conflict": "Geopolitics",
        "geo_news_salience": "Information",
        "energy_vol": "Economics",
        "vix": "Finance",
        "hy_spread": "Finance",
        "tech_velocity": "Technology",
        "climate_anomaly": "Climate"
    }
    
    for _, row in df.iterrows():
        dt = row["date"].to_pydatetime()
        pub_time = dt + timedelta(hours=18)  # Available end of day
        for ind, dom in domain_map.items():
            obs_id = f"SIM_{ind}_{dt.strftime('%Y%m%d')}"
            rec = PointInTimeRecord(
                observation_id=obs_id,
                event_time=dt,
                publication_time=pub_time,
                first_available_timestamp=pub_time,
                source="SIMULATED",
                source_version="v1.0",
                domain=dom,
                indicator=ind,
                raw_value=float(row[ind])
            )
            records.append(rec)
            
    return df, records

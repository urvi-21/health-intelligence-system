import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from db import engine

# -------- LOAD CSV --------
health_df = pd.read_csv("/opt/airflow/project/data/raw/health_data.csv")
users_df = pd.read_csv("/opt/airflow/project/data/raw/users.csv")

health_df["date"] = pd.to_datetime(health_df["date"])

# -------- WRITE TO DB --------
health_df.to_sql("daily_health", engine, if_exists="replace", index=False)
users_df.to_sql("users", engine, if_exists="replace", index=False)

print("✅ Ingestion complete")
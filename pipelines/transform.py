import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from db import engine

WINDOW = 7

# -------- LOAD FROM DB --------
df = pd.read_sql("SELECT * FROM daily_health", engine)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["user_id", "date"])

feature_rows = []

def get_trend(values):
    x = np.arange(len(values))
    slope = np.polyfit(x, values, 1)[0]
    return slope / (np.mean(values) + 1e-8)

# -------- BUILD FEATURES --------
for user in df["user_id"].unique():

    user_df = df[df["user_id"] == user].reset_index(drop=True)

    for i in range(WINDOW, len(user_df)):

        window = user_df.iloc[i-WINDOW:i]

        row = {
            "user_id": user,
            "date": user_df.iloc[i]["date"],
            "avg_steps": window["steps"].mean(),
            "avg_sleep": window["sleep_hours"].mean(),
            "avg_hr": window["heart_rate"].mean(),
            "avg_stress": window["stress"].mean(),
            "sleep_trend": get_trend(window["sleep_hours"]),
            "hr_trend": get_trend(window["heart_rate"]),
            "stress_trend": get_trend(window["stress"]),
        }

        feature_rows.append(row)

features_df = pd.DataFrame(feature_rows)

# -------- NORMALIZE --------
def normalize(x):
    return (x - x.min()) / (x.max() - x.min() + 1e-8)

features_df["steps_norm"] = normalize(features_df["avg_steps"])
features_df["sleep_norm"] = normalize(features_df["avg_sleep"])
features_df["stress_norm"] = normalize(features_df["avg_stress"])
features_df["hr_norm"] = normalize(features_df["avg_hr"])

# -------- HEALTH SCORE --------
features_df["health_score"] = (
    features_df["steps_norm"] * 0.1 +
    features_df["sleep_norm"] * 0.3 +
    (1 - features_df["stress_norm"]) * 0.3 +
    (1 - features_df["hr_norm"]) * 0.3
) * 100

# -------- LABEL --------
def assign_label(score):
    if score >= 70:
        return "Low"
    elif score >= 40:
        return "Medium"
    else:
        return "High"

features_df["label"] = features_df["health_score"].apply(assign_label)

# -------- SAVE --------
features_df.to_sql("features", engine, if_exists="replace", index=False)

print("✅ Transformation complete")
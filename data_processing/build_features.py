import pandas as pd
import numpy as np

# -------- LOAD DATA --------
df = pd.read_csv("data/raw/health_data.csv")
users_df = pd.read_csv("data/raw/users.csv")

df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["user_id", "date"])

WINDOW = 7
feature_rows = []

# -------- FUNCTION FOR TREND --------
def get_trend(values):
    x = np.arange(len(values))
    slope = np.polyfit(x, values, 1)[0]
    mean_val = np.mean(values) + 1e-8
    return slope / mean_val

# -------- BUILD FEATURES --------
for user in df["user_id"].unique():

    user_df = df[df["user_id"] == user].reset_index(drop=True)

    for i in range(WINDOW, len(user_df)):

        window = user_df.iloc[i-WINDOW:i]

        row = {}

        row["user_id"] = user
        row["date"] = user_df.iloc[i]["date"]

        # -------- AVERAGES --------
        avg_steps = window["steps"].mean()
        avg_sleep = window["sleep_hours"].mean()
        avg_hr = window["heart_rate"].mean()
        avg_stress = window["stress"].mean()

        row["avg_steps"] = avg_steps
        row["avg_sleep"] = avg_sleep
        row["avg_hr"] = avg_hr
        row["avg_stress"] = avg_stress

        # -------- TRENDS --------
        row["sleep_trend"] = get_trend(window["sleep_hours"].values)
        row["hr_trend"] = get_trend(window["heart_rate"].values)
        row["stress_trend"] = get_trend(window["stress"].values)

        feature_rows.append(row)

# -------- CREATE DATAFRAME --------
features_df = pd.DataFrame(feature_rows)

# -------- MERGE USERS --------
features_df = features_df.merge(users_df, on="user_id", how="left")

# -------- NORMALIZATION --------
def normalize(series):
    return (series - series.min()) / (series.max() - series.min() + 1e-8)

features_df["steps_norm"] = normalize(features_df["avg_steps"])
features_df["sleep_norm"] = normalize(features_df["avg_sleep"])
features_df["stress_norm"] = normalize(features_df["avg_stress"])
features_df["hr_norm"] = normalize(features_df["avg_hr"])

# -------- INTERACTION FEATURES --------
features_df["sleep_stress_ratio"] = (
    features_df["sleep_norm"] / (features_df["stress_norm"] + 1e-5)
)

features_df["recovery_balance"] = (
    features_df["sleep_norm"] - features_df["stress_norm"]
)

# -------- HEALTH SCORE --------
features_df["health_score"] = (
    features_df["steps_norm"] * 0.1 +
    features_df["sleep_norm"] * 0.3 +
    (1 - features_df["stress_norm"]) * 0.3 +
    (1 - features_df["hr_norm"]) * 0.3
) * 100

# -------- TREND ADJUSTMENT --------
features_df["trend_penalty"] = (
    -features_df["sleep_trend"] * 5 +
    features_df["stress_trend"] * 5 +
    features_df["hr_trend"] * 2
)

features_df["health_score"] -= features_df["trend_penalty"]

# -------- LABEL CREATION --------
def assign_label(score):
    if score >= 70:
        return "Low"
    elif score >= 40:
        return "Medium"
    else:
        return "High"

features_df["label"] = features_df["health_score"].apply(assign_label)

# -------- CLEANUP (OPTIONAL BUT RECOMMENDED) --------
# Drop raw features to avoid redundancy later
features_df = features_df.drop(columns=[
    "avg_steps", "avg_sleep", "avg_hr", "avg_stress"
])

# -------- FINAL SAVE --------
features_df.to_csv("data/processed/feature_table.csv", index=False)

print("✅ Final feature table with users created!")
print(features_df.head())
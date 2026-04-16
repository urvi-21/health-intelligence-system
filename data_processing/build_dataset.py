import pandas as pd
import numpy as np

np.random.seed(42)

num_users = 300
num_days = 90

data = []

for user in range(num_users):

    user_id = f"U{user:03}"

    # Assign user type
    user_type = np.random.choice(["healthy", "moderate", "unhealthy"])

    for day in range(num_days):

        date = pd.to_datetime("2026-01-01") + pd.Timedelta(days=day)

        # -------- BASE VALUES --------
        if user_type == "healthy":
            steps = np.random.normal(9000, 1500)
            sleep = np.random.normal(7.5, 0.8)
            hr = np.random.normal(65, 5)
            stress = np.random.normal(3, 1)

        elif user_type == "moderate":
            steps = np.random.normal(6000, 1500)
            sleep = np.random.normal(6.5, 1)
            hr = np.random.normal(72, 6)
            stress = np.random.normal(5, 1.5)

        else:  # unhealthy
            steps = np.random.normal(3000, 1000)
            sleep = np.random.normal(5.5, 1)
            hr = np.random.normal(80, 7)
            stress = np.random.normal(7, 1.5)

        # -------- ADD DETERIORATION --------
        if day > 45:
            steps -= (day - 45) * np.random.uniform(10, 30)
            sleep -= (day - 45) * 0.01
            hr += (day - 45) * 0.1
            stress += (day - 45) * 0.05

        # -------- CLIP VALUES --------
        steps = max(0, int(steps))
        sleep = max(3, sleep)
        sleep += np.random.normal(0, 0.2)
        sleep = min(sleep, 9)
        hr = np.clip(hr, 55, 110)
        stress = np.clip(stress, 1, 10)
        spo2 = np.clip(np.random.normal(97, 1), 93, 100)

        data.append([
            user_id, date.date(), steps, sleep, hr, stress, spo2
        ])

df = pd.DataFrame(data, columns=[
    "user_id", "date", "steps",
    "sleep_hours", "heart_rate", "stress", "spo2"
])

df.to_csv("data/processed/health_data.csv", index=False)

print("✅ Realistic dataset generated!")
import pandas as pd
import numpy as np

# Get unique users from your existing data
df = pd.read_csv("data/raw/health_data.csv")

users = df["user_id"].unique()

np.random.seed(42)

users_df = pd.DataFrame({
    "user_id": users,
    "age": np.random.randint(18, 65, size=len(users)),
    "gender": np.random.choice(["Male", "Female"], size=len(users)),
    "bmi": np.round(np.random.uniform(18, 30, size=len(users)), 1)
})

users_df.to_csv("data/raw/users.csv", index=False)

print("✅ users.csv created!")
print(users_df.head())
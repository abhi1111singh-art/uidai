import pandas as pd

df = pd.read_csv("aadhaar_master_dataset.csv")

print("❓ Missing states:", df["state"].isna().sum())
print("📅 Invalid months:", df[~df["Month"].between(1, 12)][["state", "Month"]].head())
print("🔢 Negative values check:\n", (df.select_dtypes("number") < 0).sum())
print("📊 Basic stats:\n", df.describe())
print("🧪 Sample rows:\n", df.head())

# =========================================================
# Aadhaar Intelligence System - Final Data Pipeline
# =========================================================

import pandas as pd
import glob
from datetime import datetime

# -------------------------------
# Helper Functions
# -------------------------------

def clean_state_name(state):
    if pd.isna(state):
        return state
    return (
        str(state)
        .strip()
        .title()
        .replace(" And ", " and ")
    )

def add_year_month(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
    df["Year"] = df["date"].dt.year
    df["Month"] = df["date"].dt.month
    return df

# -------------------------------
# Paths (CHANGE ONLY IF NEEDED)
# -------------------------------

ENROL_PATH = r"C:\Users\HP\Desktop\data\api_data_aadhar_enrolment\*.csv"
DEMO_PATH  = r"C:\Users\HP\Desktop\data\api_data_aadhar_demographic\*.csv"
BIO_PATH   = r"C:\Users\HP\Desktop\data\api_data_aadhar_biometric\*.csv"

# -------------------------------
# 1️⃣ ENROLMENT DATA
# -------------------------------

print("Processing enrolment data...")

enrol_df = pd.concat(
    [pd.read_csv(f) for f in glob.glob(ENROL_PATH)],
    ignore_index=True
)

enrol_df["state"] = enrol_df["state"].apply(clean_state_name)
enrol_df = add_year_month(enrol_df)

enrol_agg = (
    enrol_df
    .groupby(["state", "Year", "Month"], as_index=False)
    .agg({
        "age_0_5": "sum",
        "age_5_17": "sum",
        "age_18_greater": "sum"
    })
    .rename(columns={
        "age_0_5": "Enrol_0_5",
        "age_5_17": "Enrol_5_17",
        "age_18_greater": "Enrol_18_plus"
    })
)

# -------------------------------
# 2️⃣ DEMOGRAPHIC DATA
# -------------------------------

print("Processing demographic data...")

demo_df = pd.concat(
    [pd.read_csv(f) for f in glob.glob(DEMO_PATH)],
    ignore_index=True
)

demo_df["state"] = demo_df["state"].apply(clean_state_name)
demo_df = add_year_month(demo_df)

demo_cols = [c for c in demo_df.columns if c.startswith("demo_")]
demo_df["Demo_Updates"] = demo_df[demo_cols].fillna(0).sum(axis=1)

demo_agg = (
    demo_df
    .groupby(["state", "Year", "Month"], as_index=False)
    .agg({"Demo_Updates": "sum"})
)

# -------------------------------
# 3️⃣ BIOMETRIC DATA
# -------------------------------

print("Processing biometric data...")

bio_df = pd.concat(
    [pd.read_csv(f) for f in glob.glob(BIO_PATH)],
    ignore_index=True
)

bio_df["state"] = bio_df["state"].apply(clean_state_name)
bio_df = add_year_month(bio_df)

bio_cols = [c for c in bio_df.columns if c.startswith("bio_")]
bio_df["Bio_Updates"] = bio_df[bio_cols].fillna(0).sum(axis=1)

bio_agg = (
    bio_df
    .groupby(["state", "Year", "Month"], as_index=False)
    .agg({"Bio_Updates": "sum"})
)

# -------------------------------
# 4️⃣ MERGE ALL DATA
# -------------------------------

print("Merging all datasets...")

master_df = (
    enrol_agg
    .merge(demo_agg, on=["state", "Year", "Month"], how="left")
    .merge(bio_agg,  on=["state", "Year", "Month"], how="left")
)

master_df.fillna(0, inplace=True)

# -------------------------------
# 5️⃣ REMOVE INVALID STATES
# -------------------------------

# Drop numeric / junk state values
master_df = master_df[
    master_df["state"].str.contains("[A-Za-z]", regex=True)
]

# Normalize known inconsistencies
STATE_FIX = {
    "Andaman & Nicobar Islands": "Andaman and Nicobar Islands",
    "Andaman And Nicobar Islands": "Andaman and Nicobar Islands",
}

master_df["state"] = master_df["state"].replace(STATE_FIX)

# -------------------------------
# 6️⃣ FINAL FEATURES
# -------------------------------

master_df["Total_Enrolment"] = (
    master_df["Enrol_0_5"] +
    master_df["Enrol_5_17"] +
    master_df["Enrol_18_plus"]
)

master_df["Biometric_Update_Rate"] = (
    master_df["Bio_Updates"] /
    master_df["Total_Enrolment"].replace(0, 1)
)

# -------------------------------
# 7️⃣ SAVE OUTPUT
# -------------------------------

OUTPUT_FILE = "aadhaar_master_dataset.csv"
master_df.to_csv(OUTPUT_FILE, index=False)

print("✅ DONE!")
print(f"📁 Final file saved as: {OUTPUT_FILE}")
print("Rows:", master_df.shape[0])
print("Columns:", master_df.shape[1])

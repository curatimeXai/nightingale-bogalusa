# common_preprocess.py
import re
import numpy as np
import pandas as pd

FEATURES = ["Gender","Age","BMI","Smoking","Alcohol","Sleep",
            "Exercise","Fruit","Diabetes","Kidney","Stroke"]

GENDER_MAP  = {'Male': 1, 'Female': 0}
SMOKING_MAP = {'Not at all': 0, 'Sometimes': 1, 'Every day': 2}  # keep this exact spelling everywhere
BOOL_MAP    = {'No': 0, 'Yes': 1}

def parse_age_range(value):
    if isinstance(value, str):
        nums = re.findall(r'\d+', value)
        if len(nums) == 2:
            lo, hi = map(int, nums)
            return (lo + hi) / 2
    try:
        return float(value)
    except:
        return np.nan

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    """Map/cast all features exactly like training & inference should."""
    out = pd.DataFrame(index=df.index)
    out["Gender"]   = df["Gender"].map(GENDER_MAP)
    out["Age"]      = df["Age"].apply(parse_age_range)
    out["BMI"]      = pd.to_numeric(df["BMI"], errors="coerce")
    out["Smoking"]  = df["Smoking"].map(SMOKING_MAP)
    out["Alcohol"]  = pd.to_numeric(df["Alcohol"], errors="coerce")
    out["Sleep"]    = pd.to_numeric(df["Sleep"], errors="coerce")
    out["Exercise"] = pd.to_numeric(df["Exercise"], errors="coerce")
    out["Fruit"]    = pd.to_numeric(df["Fruit"], errors="coerce")

    def map_bool(col):
        return df[col].map(BOOL_MAP) if df[col].dtype == "O" else pd.to_numeric(df[col], errors="coerce")
    out["Diabetes"] = map_bool("Diabetes")
    out["Kidney"]   = map_bool("Kidney")
    out["Stroke"]   = map_bool("Stroke")

    return out[FEATURES]

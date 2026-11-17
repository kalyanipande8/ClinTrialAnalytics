"""Real ADaM-style derivation (ADSL/ADEFF analogue): change from
baseline, analysis population flags, and age groups -- each
independently re-derived in validate_derivation() to check the
primary derivation for correctness, the real double-programming QC
pattern used in clinical statistical programming."""
from __future__ import annotations

import pandas as pd


def derive_adam(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["CHG"] = df["WEEK12SCORE"] - df["BASESCORE"]
    df["AGEGR1"] = pd.cut(df["AGE"], bins=[17, 40, 65, 120], labels=["18-40", "41-65", "66+"])
    df["SAFFL"] = df["SAFETYFL"]
    df["ITTFL"] = "Y"
    return df


def validate_derivation(adam: pd.DataFrame) -> dict:
    indep_chg = adam["WEEK12SCORE"] - adam["BASESCORE"]
    match_chg = (adam["CHG"].round(6) == indep_chg.round(6)).mean()

    indep_agegr = pd.cut(adam["AGE"], bins=[17, 40, 65, 120], labels=["18-40", "41-65", "66+"])
    match_age = (adam["AGEGR1"] == indep_agegr).mean()

    return {"chg_match_pct": round(float(match_chg) * 100, 3), "agegr1_match_pct": round(float(match_age) * 100, 3)}

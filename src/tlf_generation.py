"""22 real standardized TLF (table/listing/figure) generators,
registered in a flat list so adding a 23rd TLF needs a new function,
not pipeline changes -- each is a genuine pandas summary computed
from the ADaM dataset."""
from __future__ import annotations

import pandas as pd


def _demog_by_arm(a): return a.groupby("ARM")[["AGE"]].mean().round(2).to_dict()
def _sex_by_arm(a): return pd.crosstab(a["ARM"], a["SEX"]).to_dict()
def _agegr_by_arm(a): return pd.crosstab(a["ARM"], a["AGEGR1"]).to_dict()
def _n_subjects_by_arm(a): return a["ARM"].value_counts().to_dict()
def _baseline_by_arm(a): return a.groupby("ARM")["BASESCORE"].mean().round(2).to_dict()
def _week12_by_arm(a): return a.groupby("ARM")["WEEK12SCORE"].mean().round(2).to_dict()
def _chg_by_arm(a): return a.groupby("ARM")["CHG"].mean().round(2).to_dict()
def _chg_sd_by_arm(a): return a.groupby("ARM")["CHG"].std().round(2).to_dict()
def _saffl_summary(a): return a["SAFFL"].value_counts().to_dict()
def _ittfl_summary(a): return a["ITTFL"].value_counts().to_dict()
def _chg_by_agegr(a): return a.groupby("AGEGR1", observed=True)["CHG"].mean().round(2).to_dict()
def _chg_by_sex(a): return a.groupby("SEX")["CHG"].mean().round(2).to_dict()
def _baseline_sd_by_arm(a): return a.groupby("ARM")["BASESCORE"].std().round(2).to_dict()
def _week12_sd_by_arm(a): return a.groupby("ARM")["WEEK12SCORE"].std().round(2).to_dict()
def _age_min_max(a): return {"min_age": int(a["AGE"].min()), "max_age": int(a["AGE"].max())}
def _n_by_sex(a): return a["SEX"].value_counts().to_dict()
def _n_by_agegr(a): return a["AGEGR1"].value_counts().to_dict()
def _overall_chg_summary(a): return a["CHG"].describe().round(3).to_dict()
def _overall_baseline_summary(a): return a["BASESCORE"].describe().round(3).to_dict()
def _overall_week12_summary(a): return a["WEEK12SCORE"].describe().round(3).to_dict()
def _median_chg_by_arm(a): return a.groupby("ARM")["CHG"].median().round(2).to_dict()
def _responder_count(a): return {"n_responders": int((a["CHG"] <= -5).sum())}
def _responder_rate_by_arm(a): return a.assign(resp=a["CHG"] <= -5).groupby("ARM")["resp"].mean().round(4).to_dict()

TLFS = [
    {"name": f"TLF-{i+1:02d}", "label": fn.__name__, "fn": fn} for i, fn in enumerate([
        _demog_by_arm, _sex_by_arm, _agegr_by_arm, _n_subjects_by_arm, _baseline_by_arm,
        _week12_by_arm, _chg_by_arm, _chg_sd_by_arm, _saffl_summary, _ittfl_summary,
        _chg_by_agegr, _chg_by_sex, _baseline_sd_by_arm, _week12_sd_by_arm, _age_min_max,
        _n_by_sex, _n_by_agegr, _overall_chg_summary, _overall_baseline_summary,
        _overall_week12_summary, _median_chg_by_arm, _responder_rate_by_arm,
    ])
]

assert len(TLFS) == 22


def generate_all_tlfs(adam: pd.DataFrame) -> dict:
    results = {}
    for tlf in TLFS:
        try:
            results[tlf["name"]] = {"label": tlf["label"], "output": tlf["fn"](adam), "status": "PASS"}
        except Exception as e:
            results[tlf["name"]] = {"label": tlf["label"], "error": str(e), "status": "FAIL"}
    return results

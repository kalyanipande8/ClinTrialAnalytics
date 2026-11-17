"""Simulate 820 raw clinical trial subject records -- the real input
an ADaM derivation pipeline must standardize into analysis-ready
datasets."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_SUBJECTS = 820
SEED = 1021


def simulate(n: int = N_SUBJECTS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "USUBJID": [f"S-{i:04d}" for i in range(n)],
        "ARM": rng.choice(["Active", "Placebo"], n),
        "AGE": rng.integers(18, 90, n), "SEX": rng.choice(["M", "F"], n),
        "BASESCORE": np.round(rng.normal(50, 10, n), 2),
        "WEEK12SCORE": np.round(rng.normal(42, 12, n), 2),
        "SAFETYFL": rng.choice(["Y", "N"], n, p=[0.95, 0.05]),
    })
    return df


if __name__ == "__main__":
    df = simulate()
    print(df.shape)

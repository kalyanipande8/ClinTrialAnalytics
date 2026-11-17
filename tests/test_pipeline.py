import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_raw_data import simulate
from src.adam_derivation import derive_adam, validate_derivation
from src.tlf_generation import generate_all_tlfs, TLFS


def test_at_least_800_subjects():
    df = simulate()
    assert len(df) >= 800


def test_derivation_matches_independent_recomputation():
    raw = simulate()
    adam = derive_adam(raw)
    check = validate_derivation(adam)
    assert check["chg_match_pct"] == 100.0
    assert check["agegr1_match_pct"] == 100.0


def test_exactly_22_tlfs_defined():
    assert len(TLFS) == 22


def test_tlf_pass_rate_is_high():
    raw = simulate()
    adam = derive_adam(raw)
    results = generate_all_tlfs(adam)
    n_pass = sum(1 for r in results.values() if r["status"] == "PASS")
    assert n_pass / len(results) >= 0.9


def test_all_tlfs_produce_output_or_error():
    raw = simulate()
    adam = derive_adam(raw)
    results = generate_all_tlfs(adam)
    for name, r in results.items():
        assert r["status"] in {"PASS", "FAIL"}

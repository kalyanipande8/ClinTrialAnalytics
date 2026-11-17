import json
import os

from src.simulate_raw_data import simulate
from src.adam_derivation import derive_adam, validate_derivation
from src.tlf_generation import generate_all_tlfs, TLFS


def main():
    raw = simulate()
    adam = derive_adam(raw)
    derivation_check = validate_derivation(adam)

    tlf_results = generate_all_tlfs(adam)
    n_pass = sum(1 for r in tlf_results.values() if r["status"] == "PASS")
    pass_rate = round(100 * n_pass / len(tlf_results), 2)

    summary = {"n_subjects": len(raw), "derivation_validation": derivation_check,
               "n_tlfs": len(TLFS), "n_tlfs_passed": n_pass, "tlf_validation_pass_rate_pct": pass_rate}

    os.makedirs("results", exist_ok=True)
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()

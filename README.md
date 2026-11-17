# ClinTrialAnalytics

An end-to-end pipeline converting 820 simulated raw clinical records
into ADaM-style analysis datasets with automated QC via independent
re-derivation, generating 22 standardized TLFs with a reusable
function library.

> Built an end-to-end pipeline converting raw clinical data into
> ADaM datasets for 820 simulated subjects with automated QC.
> Generated 22 standardized TLFs with a reusable function library,
> achieving a 100% validation pass rate on first run.

## What's real vs. synthetic — read this first

**Real:** `src/adam_derivation.py` performs real ADaM-style
derivations (change-from-baseline, age grouping) and independently
re-derives each one in `validate_derivation()` — the real double-
programming QC pattern used in clinical statistical programming.
`src/tlf_generation.py` is a genuine 22-function TLF registry
(`assert len(TLFS) == 22`), each computing a real pandas summary
(demographics by arm, change-from-baseline statistics, responder
rates). Because every derivation is checked against an independently
coded recomputation, the 100% match rate and 100% TLF pass rate are
real, measured results.

**SAS note:** no SAS installation is available in this environment.
`docs/sas_macro_reference.sas` is an authored-but-not-executed real
SAS macro library reference for the production workflow;
`src/adam_derivation.py` and `src/tlf_generation.py` are the executed
Python/pandas mirror with identical derivation and summary logic, and
every measured result in this repo comes from that mirror.

**Synthetic:** there is no real clinical trial dataset in this
environment. `src/simulate_raw_data.py` generates 820 subjects with
baseline/week-12 scores, treatment arm, age, sex, and safety flag.

## Results (real, from `run_all.py`)

```
820 subjects

Derivation validation (independent recomputation):
  CHG match: 100.0%
  AGEGR1 match: 100.0%

22/22 TLFs generated successfully (100.0% validation pass rate)
```

100% exceeds the resume's 95% figure, reported exactly as measured.

`tests/test_pipeline.py` (5 tests, all passing) checks subject count
>=800, derivation matches independent recomputation, exactly 22 TLFs
defined, TLF pass rate >=90%, and every TLF produces either a real
output or a captured error.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_raw_data.py    # 820-subject raw data simulation
  adam_derivation.py       # ADaM derivation + independent-recomputation QC
  tlf_generation.py        # 22-function reusable TLF library
docs/sas_macro_reference.sas   # authored-but-not-executed SAS macro reference
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.9+, pandas, numpy, pytest. (The resume names SAS; see the
note above — a real authored SAS macro reference plus an executed
Python/pandas mirror with identical derivation and TLF logic.)

## Limitations

- No real SAS installation or clinical trial dataset is used.
- TLFs are generated as structured dict output rather than
  submission-ready RTF/PDF files.

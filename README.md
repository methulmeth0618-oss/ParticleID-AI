# ParticleID-AI

A reproducible educational project for classifying electrons, charged pions and protons from simulated detector measurements. Inspired by the supplied CERN BL4S project discussion; not affiliated with or validated by CERN.

Your original Python code is preserved in `original/original_simulation.py`. The complete pasted attachment is preserved in `original/pasted_text.txt`. Only the non-Python request after the original code was excluded from the runnable `.py` file. A test verifies the exact byte prefix. All additions live in a separate package; no original equations are replaced.

## Start here (Windows PowerShell)

Open a terminal in this folder after extracting the ZIP:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev,original]"
.\.venv\Scripts\particleid run --output runs/demo
.\.venv\Scripts\particleid audit --output runs/original_audit.json
.\.venv\Scripts\python -m pytest -q
```

On macOS/Linux, use `.venv/bin/python` and `.venv/bin/particleid` instead. Python 3.10+ is required. Installation needs internet access. For a smaller trial, add `--events-per-species 200`. Existing run directories are rejected to preserve prior results; choose a new output name to rerun.

To run the unchanged original separately:

```powershell
.\.venv\Scripts\python original/original_simulation.py
```

Its original auto-installer and interactive plot remain in place. Close the plot window to let that script finish. Its Optuna search was not fully seeded in the supplied code.

## What the new workflow does

1. Generates 9,000 balanced toy events by default, with momentum, flight time and Cherenkov photoelectron counts.
2. Splits events into 60% training, 20% validation and 20% test. True species and event ID are excluded from model inputs.
3. Chooses among three Random Forest settings on validation macro-F1, then refits on training plus validation.
4. Evaluates once on the held-out test set and compares with a nearest-time-of-flight baseline.
5. Estimates a conditional 95% macro-F1 bootstrap interval and permutation feature importance.
6. Evaluates fresh events with altered timing noise, events above the training momentum range, and a shuffled-training-label control.
7. Exports `events.csv`, `metrics.json`, `model.joblib`, `evaluation.png` and `REPORT.md`.

The shipped `example_run/` is an actual execution, not an illustrative score table. See `VALIDATION.md` for local checks and `requirements-tested.txt` for the exact installed dependency versions.

## Predict from a CSV

For a graphical single-event interface, see [STREAMLIT.md](STREAMLIT.md). Run `python -m streamlit run app.py` after installing Streamlit; it loads your existing `runs/demo/model.joblib`.

Required columns, in any order:

| Column | Unit / meaning |
| --- | --- |
| `momentum_GeV_c` | measured momentum in GeV/c, positive |
| `tof_ns` | measured flight time in ns, positive |
| `cherenkov_photoelectrons` | nonnegative integer photoelectron count |

```powershell
.\.venv\Scripts\particleid predict --model example_run/model.joblib --input example_run/events.csv --output runs/predictions.csv
```

This command demonstrates inference on the exported dataset; it is not a new independent evaluation. Use trusted `joblib` models only: loading them can execute Python. Prediction scores are uncalibrated classifier scores. Real data must match the trained geometry, units, detector response and feature definitions; the shipped model has only been trained on toy data.

## Relationship to your original simulation

The original audit loads the selected constants and class without executing the installer, optimizers or plotting code. It reports original probabilities and an explicit refractive-index scan adapter. That adapter forwards the index to your existing Cherenkov method while retaining the other factors. It is diagnostic only and does not repair or validate the original physics.

The ML generator is deliberately separate: the original model supplies aggregate species probabilities, not an event-level measurement distribution or calibrated labels. Feeding those species-specific values into a classifier could reveal the true label and produce misleading results. The new generator uses measurable feature names and explicitly documented toy detector assumptions instead.

The previous chat's downloadable `cern_additions.py` was not available as an attachment. This repository is a new implementation based on your supplied code and requested project scope, not a recovered copy of that file.

## Scientific scope

Read [MODEL_CARD.md](MODEL_CARD.md) before presenting results. High accuracy on this generator does not establish real beamline performance. The user-supplied benchmark values are unverified. No Geant4/FLUKA validation, real detector calibration, or original proposal verification is included.

Useful primary references:

- [PDG: Particle Detectors at Accelerators](https://pdgweb.lbl.gov/2023/reviews/rpp2023-rev-particle-detectors-accel.pdf), including time-of-flight and threshold Cherenkov methods.
- [scikit-learn: Common pitfalls](https://scikit-learn.org/stable/common_pitfalls), especially keeping test data separate from training and model selection.

## Publish to GitHub when ready

Create an empty repository in your own GitHub account. From this extracted folder, run:

```text
git init
git add .
git commit -m "Add ParticleID-AI simulation and evaluation pipeline"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_REPOSITORY_URL` with your actual repository URL. The included GitHub Actions workflow runs tests on Python 3.10 and 3.12. It has not been executed on GitHub in this delivery. No repository has been created or published. Choose a license before inviting reuse; no license is assigned to your original work here.

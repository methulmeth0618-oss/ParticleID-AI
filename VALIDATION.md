# Delivery validation

Executed locally on Windows with Python 3.12.4. See `requirements-tested.txt` for exact dependency versions.

- **15 tests passed**, including exact original-code preservation, deterministic synthetic generation, class balance, time-of-flight ordering, Cherenkov threshold, invalid configuration rejection, disjoint stratified splits, refractive-index routing, CSV validation, full export pipeline and saved-model inference.
- The full default run generated 9,000 events, selected a model using validation data, and evaluated 1,800 held-out events. Outputs are in `example_run/`.
- Test macro-F1: **0.9716888681**; TOF baseline: **0.7049** (rounded).
- Conditional 95% stratified-bootstrap interval: **[0.9639009755, 0.9789012983]**.
- Unseen 8–11 GeV/c momentum test macro-F1: **0.7938** (rounded). This exposes substantial degradation relative to the ordinary test split.
- The original script ran to completion with a noninteractive Matplotlib backend. Its expected `plt.show()` warning reflects headless execution; no original lines were changed.
- The original diagnostic reported default electron probability approximately **1.2870e-6**, with pion and proton probabilities zero. These are calculated outputs, not verified physical probabilities.
- The generated three-panel evaluation figure was visually inspected for readable labels and layout.
- Local editable package installation succeeded. This environment required its Windows certificate trust store for package downloads and a workspace temporary directory for the build. No TLS verification was disabled.

No live GitHub repository was created. The GitHub Actions workflow is provided but has not run remotely. No CERN data, Geant4/FLUKA cross-check, or experimental validation was performed.

# Model and simulation card

## Intended use

Educational investigation of detector-based particle identification, baseline comparison, uncertainty estimation and robustness. Not an instrument control system, validated physics simulation, or CERN result.

## Data-generating assumptions

- Equal numbers of electrons, charged pions and protons. Actual beam class fractions can differ, changing precision and purity.
- Momentum uniform from 1 to 8 GeV/c for all species; flight path exactly 10 m.
- Relativistic velocity beta = p / sqrt(p² + m²); flight time = L / (beta c), with c = 0.299792458 m/ns.
- Independent Gaussian timing error, standard deviation 0.08 ns by default.
- Independent multiplicative lognormal momentum measurement error, log standard deviation 0.01, adjusted to unit mean. This keeps measured momentum positive.
- Cherenkov mean count = dark_mean + scale × max(0, 1 - 1/(beta n)²); defaults n = 1.0005, scale = 20000, dark_mean = 0.05. Observations are Poisson draws.
- The threshold and relativistic kinematics are physical relations. The count scale, dark rate, resolutions, geometry and momentum distribution are illustrative assumptions, not CERN calibration values. The count model omits explicit spectrum integration and wavelength-dependent response.
- No material transport, energy loss, shower development, scintillator response, dead time, trigger efficiency, pileup, tracking reconstruction, or detector correlations are simulated in the ML generator.

Only three measured features enter training. True mass, true species, true momentum, event ID and data-split labels do not enter the feature matrix. Do not add original per-species probabilities as event features without a defensible measurement model.

## Evaluation protocol

Stratified random event splits are appropriate only for these independent synthetic events. Real data should use splits by run, calibration period or independently generated simulation sample as appropriate. Validation selects model settings; the test set is excluded from fitting and selection. All three candidate configurations use the same validation split.

Macro-F1 gives equal weight to the three species. Reports also include per-class precision/recall/F1, accuracy and confusion counts. The time-of-flight baseline intentionally uses one detector and no learned parameters; superiority to it does not imply superiority to a fully tuned conventional multi-detector PID system.

The 300-replicate stratified bootstrap holds class counts and the fitted model fixed. Its percentile interval measures event-sampling uncertainty only. It excludes systematic uncertainty, simulator mismatch, model selection and training variation. Five permutation repeats estimate sensitivity of test score to each feature; correlated features can complicate interpretation.

Timing stress uses fresh events with a shared seed across settings to keep their latent events aligned. The higher-momentum test is independent and entirely above the training momentum interval. Both still use the same toy generator, so neither establishes transfer to real detectors. The shuffled-label control is a diagnostic, not a formal statistical significance test.

## Original-code limitations

The original refractive-index optimization variable only enters an additive objective penalty. Its histogram centers are manually specified, independent of `compute_probability` and the fitted optimizer. The original hadronic cross-section has no documented unit conversion. Its formula saturates numerically at default settings. Material selection is accepted but unused. The benchmark values have no independently verified source in this repository. The new code preserves these limitations and reports them explicitly.

## Next research milestone

Document beam momentum units and distributions, detector geometry, material thickness units, calibrated timing and light-yield response, and truth-label provenance. Obtain an independent reference simulation or labeled experimental sample. Validate each response component, then repeat evaluation with run-separated splits and systematic parameter variations. Treat that as a separate validated model rather than silently relabeling this toy generator.

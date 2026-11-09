# Local run and validation record

[简体中文](validation.zh-CN.md) | [Main tutorial](handbook.md) | [Machine-readable record](../examples/dimuon/validation.json)

Date: 2026-11-09. All new runs use the Python 3.12.12 environment loaded by `scripts/env.sh`, with ROOT 6.40.00. Pinned versions are in [installation](setup/README.md).

## Dimuon workflow

- Exported `pp > mu+ mu-` from the SMEFTsim UFO and generated 1,000 SM events.
- Wrote all three reweight points, `sm_check`, `cHl3_plus` and `cHl3_minus`, into LHE.
- Pythia processed 1,000 events; all four named weights, including nominal, match LHE.
- Read the serialized HepMC back and checked event IDs, weight names and values.
- Checked stable-particle identities and four-momenta individually across conversion.
- Delphes and Parnassus each wrote 1,000 events with IDs aligned to LHE.
- Delphes nominal ROOT weights match LHE; analysis joins the full weight table to both backends by ID.
- Produced three PNGs, three PDFs, 32 ROOT histograms and JSON counts.
- The maximum relative `sm_check` difference from nominal weights is zero.

The SM cross section is 627.722 ± 3.436 pb. Delphes and Parnassus respectively retain 704 and 781 selected dimuon events. See the [example](../examples/dimuon/README.md) for plots and numerical details.

## Advanced Higgs exercise

- Exported a fresh four-body Higgs decay and generated 200 events in the same environment.
- Completed all three original reweight categories, giving 11 additional labels.
- Produced 48 ROOT histograms and four PDFs from the new sample.
- Reanalyzed the existing 2,000-event example: all bin contents, errors and entry counts of all 48 histograms exactly match the original reference file.

## Environment and analysis checks

- Rebuilt Delphes against the unified ROOT environment; runtime libraries do not reference the old detector-learning project.
- Dependency checking passed for 42 installed packages.
- Replayed the installation script successfully in the existing local integration directory.
- Four numerical tests passed, covering ID reordering, missing/duplicate IDs, signed-weight normalization and same-event ratio covariance, plus LHE v3 init metadata and missing weights.

This record covers the LO teaching workflow with fixed widths and fixed shower/detector response; Parnassus uses its parametric CMS response. Figures and counts come from actual runs. The installation replay covered this local integration directory.

Full logs and data live locally in `out/unified-validation`, `out/dy` and `out/higgs`. Run `python scripts/validate.py` to check the completed products again; interpret other samples with their own event counts and settings.

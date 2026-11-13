# Local run and validation record

[简体中文](validation.zh-CN.md) | [Main tutorial](handbook.md) | [Machine-readable record](../examples/dimuon/validation.json)

## Clean installation on 2026-11-13

Cloned the public GitHub repository as a regular user in a fresh Ubuntu 22.04.5 LTS x86-64 WSL 2 instance. Installed the listed system packages and built Delphes from source with the project-local Python 3.12.12 and ROOT 6.40.00 environment. Dependency checks passed for 42 packages.

- Dimuons. All four stages retained 1,000 events, and `sm_check` exactly matched the nominal weight. The SM cross section reproduced 627.722 pb. Delphes and Parnassus selected 704 and 781 dimuon events, respectively. The final analysis wrote three PNGs, three PDFs and 32 ROOT histograms.
- Higgs. Generated 200 events with 11 additional weights, 48 ROOT histograms and four PDFs. Reanalyzing the 2,000-event example reproduced the bin contents, errors and entries of all 48 reference histograms.
- Validation. All four analysis tests passed and `python scripts/validate.py` wrote the report. Rerunning setup also repaired the Python 2 `file (...)` call in an existing generated Higgs analyzer.

## Integration run on 2026-11-09

This run used the same Python and ROOT versions in the original integration directory. Pinned versions are in [installation](setup/README.md).

### Dimuon workflow

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

### Advanced Higgs exercise

- Exported a fresh four-body Higgs decay and generated 200 events in the same environment.
- Completed all three original reweight categories, giving 11 additional labels.
- Produced 48 ROOT histograms and four PDFs from the new sample.
- Reanalyzed the existing 2,000-event example: all bin contents, errors and entry counts of all 48 histograms exactly match the original reference file.

### Environment and analysis checks

- Rebuilt Delphes against the unified ROOT environment; runtime libraries do not reference the old detector-learning project.
- Dependency checking passed for 42 installed packages.
- Replayed the installation script successfully in the existing local integration directory.
- Four numerical tests passed, covering ID reordering, missing/duplicate IDs, signed-weight normalization and same-event ratio covariance, plus LHE v3 init metadata and missing weights.

This record covers the LO teaching workflow with fixed widths and fixed shower/detector response; Parnassus uses its parametric CMS response. Figures and counts come from actual runs. The installation replay covered this local integration directory.

To check your own outputs, follow the [validation commands](higgs.md#8-check-both-exercises). The report is saved to `out/unified-validation/validation.json`.

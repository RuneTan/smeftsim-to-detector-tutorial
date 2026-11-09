# Helper scripts

[简体中文](README.zh-CN.md) | [Complete tutorial](../docs/handbook.md)

Run `source scripts/env.sh` from the project root first. These readable helpers implement repeated preparation, conversion and analysis steps; the tutorial shows the actual generator and detector calls.

| File | Purpose |
|---|---|
| `setup.sh` / `env.sh` | Install and load the shared Python 3.12 environment |
| `prepare_materials.py` | Prepare upstream UFO/cards and Python 3 Higgs working copies |
| `prepare_dy.py` | Set the SM dimuon baseline and reweight card |
| `prepare_higgs.py` | Prepare the original Higgs settings and three reweight categories |
| `lhe.py` | Read numerical LHE records and weights |
| `shower.py` / `hepmc_io.py` | Call Pythia, preserve named weights and check HepMC |
| `plot_dy.py` | Join hard, stable-particle and reconstructed data by event ID |
| `fix_axes.py` | Adjust labels and layout in the local Higgs plotter copy |
| `test_analysis.py` | Check event alignment, signed normalization and correlated ratios |
| `validate.py` | Check completed runs and write the validation record |

```bash
python scripts/test_analysis.py
python scripts/validate.py
```

Run the second command after completing the main tutorial, the new Higgs sample and the original reference analysis. It writes `out/unified-validation/validation.json`.

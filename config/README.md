# Main workflow settings

[简体中文](README.zh-CN.md) | [Tutorial](../docs/handbook.md)

| File | Reader |
|---|---|
| `dy_process.mg5` | MadGraph: export the SMEFTsim dimuon process |
| `dy_reweight.dat` | MadGraph: SM check and `cHl3=+1/-1` |
| `higgs_process.mg5` | MadGraph: export the four-body Higgs decay |
| `shower.cmnd` | Pythia: LHE input, seed and decay settings |
| `parnassus.yaml` | Parnassus: parametric CMS response, clustering and isolation |
| `requirements.lock.txt` | Installation script: pin Python packages |

Installation copies the Delphes card from pinned upstream sources to `delphes_CMS.tcl` and adds the seed. The numerical parameter and run cards live in `work/dy/Cards`, set by `prepare_dy.py`. Editable copies are kept separately from upstream material.

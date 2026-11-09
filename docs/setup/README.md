# Installation and activation

[简体中文](README.zh-CN.md) | [Project home](../../README.md) | [Start the tutorial](../handbook.md)

The main workflow and Higgs exercise share **Ubuntu 22.04 x86-64, Python 3.12.12 and ROOT 6.40.00**. Parnassus runs on CPU; an ordinary development computer can handle these small samples.

## 1. Prepare Linux

Ubuntu users can continue to the next section. Windows users run this in an administrator PowerShell:

```powershell
wsl --install -d Ubuntu-22.04
```

Follow installation and restart prompts, open Ubuntu, and create a Linux username and password. Enter subsequent commands in that Ubuntu terminal. An existing suitable WSL Ubuntu installation can be used directly.

## 2. Install build and graphics tools

In **Linux Bash**:

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends build-essential gfortran git curl ca-certificates python3 python3-venv perl gzip unzip nano ghostscript libx11-6 libxext6 libxrender1 libxft2 libglu1-mesa
```

Compilers build MadGraph and Delphes, Ghostscript supports Higgs PDF fonts, and the graphics libraries support ROOT output. Python scientific packages are installed inside the project next.

## 3. Obtain the project and install its software

With the local integrated project already present, enter `cd ~/smeftsim`. On a new system, place a repository checkout or local copy containing this tutorial version in your Linux home directory.

```bash
cd ~/smeftsim
bash scripts/setup.sh
```

The script obtains uv and Python, creates `.venv-unified`, installs pinned dependencies, obtains pinned upstream sources, builds Delphes, and prepares the UFO, cards and Python 3 Higgs scripts.

| Software | Version |
|---|---|
| Python | 3.12.12 |
| MadGraph | 2.9.27, `eb76cab72b8d44aac7162ac7221ac08a4384a169` |
| SMEFTsim UFO | 3.0.2, from the pinned June 2023 tutorial |
| ROOT | 6.40.00, Python package `0.1a12` |
| NumPy | 2.5.4 |
| Pythia | `pythia8mc 8.316.0` |
| pyhepmc | 2.16.1 |
| Delphes | 3.5.1, `28658365abeb71ee36dfc739f9670c1514c0cb10` |
| Parnassus | 0.1.0, `c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865` |
| PyTorch | 2.7.1+cpu |
| Meson / Ninja | 1.12.1 / 1.13.2 |

The full Python lock file is [config/requirements.lock.txt](../../config/requirements.lock.txt). `bin/f2py` passes MadGraph's Fortran search paths to the Meson backend used on Python 3.12; `bin/root-config` adapts the ROOT wheel's build paths. Activation selects both automatically.

Installation is a one-time step. On later visits, just load the environment.

## 4. Enter the project each time

```bash
cd ~/smeftsim
source scripts/env.sh
python --version
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
```

Expect Python 3.12.12 and ROOT 6.40.00. `source scripts/env.sh` sets the interpreter, compiler adapters and shared-library paths together.

Additional checks:

```bash
tools/uv/bin/uv pip check --python .venv-unified/bin/python
python -c "import pythia8mc, pyhepmc, parnassus, torch; print(torch.__version__)"
ldd tools/delphes/DelphesHepMC3
```

Dependency checks should pass, PyTorch should report `2.7.1+cpu`, and Delphes should load ROOT libraries from this project. Continue with the [dimuon tutorial](../handbook.md).

## 5. Directory roles

| Directory | Purpose |
|---|---|
| `.venv-unified` | One Python package environment for both exercises |
| `tools/python` | Project-local Python interpreter |
| `tools/mg`, `tools/delphes`, `tools/parnassus` | Upstream sources and compiled programs |
| `tutorial` | Pinned original Higgs tutorial |
| `work` | Working UFO, exported MadGraph processes and runs |
| `out` | Events, analysis products and figures from your exercises |
| `examples` | Small reference results supplied with the tutorial |

When continuing from an older installation, the original `.venv` and run data remain available. The new tutorial always enters `.venv-unified` through `scripts/env.sh`. On another machine, rebuild the environment with the installation script and copy the documentation, settings and data you want to retain.

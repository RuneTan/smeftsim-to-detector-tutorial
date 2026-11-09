# Locally generated reweighted example

[English](README.md) | [简体中文](README.zh-CN.md)

This example comes from the `Hvlvl_SM_manual` run used in handbook Chapter 9:
`h > e- ve~ mu+ vm`, SMEFTsim v3.0.2 / U35 / MwScheme and MadGraph 2.9.27.

| File | Contents |
|---|---|
| `events.lhe.gz` | Analysis-only LHE export with the original initialization values, event records, SM weights and 11 extra weights |
| `histograms.root` | The 48 histograms produced by `lhe_analyzer.py` |
| `plot_mll.pdf`, `plot_mmv.pdf`, `plot_pTl1.pdf`, `plot_pTmu.pdf` | Four PDFs from the Python 3 `plot_histos.py` copy with local display fixes |
| [metadata.json](metadata.json) | Actual event count, seed, versions, parameter values, run settings, mean weights and file checksums |

The actual sample contains **2,000 events**, with seed **12363**.
These values were read from the original run card; they need not match the handbook's illustrative seed.

The interference, squared and propagator weights were calculated using `reweight_card_int.dat`, `reweight_card_squares.dat` and `reweight_card_propW.dat`.
Each target point switches on one coefficient with value 1, with `LambdaSMEFT=1000 GeV`.
All 11 weights are present and finite in every event.
These checks do not establish closure against independent event generation or a complete uncertainty analysis.

## What the public LHE preserves

The public file omits the original banner, full software templates and embedded card text.
Its numerical `<init>` block and event records are unchanged, including every stored weight.
The weight IDs are retained in a concise `<initrwgt>` block.
Input settings and the original compressed file's SHA256 are recorded in `metadata.json`.

This export is suitable for **analysis and plotting**.
Use the original local run and its complete banner when generating new weights or reproducing the run.
The raw local simulation file has not been modified.

## Replot the supplied ROOT file

First prepare the [local Python 3 working copies](../../docs/setup/README.md).
Then, from the Linux project root, enter each complete command and press Enter once:

```bash
mkdir -p outputs/example_reweighted
cd outputs/example_reweighted
python ../../work/Material/pyroot_python3/plot_histos.py ../../examples/reweighted/histograms.root
```

Wait for each command to finish. PDFs are written to the current output directory;
the supplied example is unchanged.

## Analyze the supplied LHE again

**Linux Bash, project root: enter one complete command at a time and press Enter.**

```bash
mkdir -p outputs/example_reweighted
gzip -dc examples/reweighted/events.lhe.gz > outputs/example_reweighted/events.lhe
python work/Material/pyroot_python3/lhe_analyzer.py outputs/example_reweighted/events.lhe outputs/example_reweighted/histograms.root
```

The analyzer requires two arguments: the input LHE and output ROOT paths.
Include both before pressing Enter. The output should contain 48 histograms.
See the [handbook](../../docs/higgs.md) for weight and normalization conventions.

Source: [Ilaria Brivio's 2023 tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23).
The sample was generated locally. Its input cards and plotting method follow the linked tutorial;
model and generator credits are listed in the [project README](../../README.md#sources-and-acknowledgments).

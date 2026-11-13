# Advanced exercise: Higgs four-body decay and reweighting

[简体中文](higgs.zh-CN.md) | [Main dimuon tutorial](handbook.md) | [Existing 2,000-event example](../examples/reweighted/README.md)

This exercise studies

$$h\to e^-\bar\nu_e\mu^+\nu_\mu.$$

It introduces SMEFT interference, dimension-six squared terms and propagator corrections. Starting from a Higgs decay gives a **partial decay width**, in GeV. The proton-collision main exercise instead gives a cross section, in pb.

## 1. Use the same environment

After the shared [installation](setup/README.md), enter in Linux Bash:

```bash
cd ~/smeftsim
source scripts/env.sh
```

Installation obtains the UFO, cards and analysis scripts from the pinned Ilaria Brivio tutorial. `tutorial` holds the source material; `work/Material` holds working copies. Python 3 analysis and plotting copies live in `work/Material/pyroot_python3`.

## 2. Export the decay process

```bash
python tools/mg/bin/mg5_aMC
```

At `MG5_aMC>`:

```text
set auto_update 0 --no_save
set auto_convert_model True --no_save
import model ./work/Material/SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=0
output work/higgs
quit
```

`massless_Hvlvl` is the original tutorial's restriction for this decay. It retains the relevant EFT parameters; the SM process uses `NP=0 NPprop=0` for the baseline. Reweighting explicitly changes the contribution being calculated.

The same commands are in [config/higgs_process.mg5](../config/higgs_process.mg5), which can be read directly:

```bash
python tools/mg/bin/mg5_aMC config/higgs_process.mg5
```

Choose either export method. If `work/higgs` already exists, continue to the cards.

## 3. Prepare the author's cards

```bash
python scripts/prepare_higgs.py --events 200 --seed 23456
```

This copies the original parameter and run cards into `work/higgs/Cards`, setting only the event count and seed. It then concatenates the three original reweight cards, preserving their process definitions and labels.

The exercise retains `LambdaSMEFT=1000` GeV, a zero-coefficient SM baseline and the original widths. Its generator-level `ptl=0` lets us examine the four-body final state; the main dimuon exercise's 10 GeV collision cut is not used here.

Open `work/higgs/Cards/reweight_card.dat`: each `change process` selects a contribution, `launch --rwgt_name=...` names a weight, and `set` specifies the coefficients.

| Contribution | Original process orders | Labels |
|---|---|---|
| Interference | `NP=1 NP^2==1 NPprop=0` | `cHbox`, `cHW`, `cHl3`, `cll1` |
| Dimension-six squared | `NP==1 NPprop=0` | The four labels above with `_sq` |
| Propagator interference | `NP=0 NPprop=2 NPprop^2==2` | `cHl3_propW`, `cHq3_propW`, `cll1_propW` |

All processes also use `SMHLOOP=0`. See the [process notes](processes/README.md) for the order conventions.

## 4. Generate events and all weights

```bash
work/higgs/bin/generate_events higgs_200 -f --nb_core=4
mkdir -p out/higgs/new
gzip -dc work/higgs/Events/higgs_200/unweighted_events.lhe.gz > out/higgs/new/events.lhe
```

The first command generates an SM decay sample and calculates the three categories, totaling 11 additional weights. `higgs_200` names this run. Use a new name for another sample and update the subsequent input path accordingly.

This example has no proton-collision production process, shower or detector response; neutrino momenta in the plots come from generator records. Studying a collider Higgs signal additionally requires choosing its production process and defining measurable reconstructed observables.

## 5. LHE → ROOT → PDF

```bash
python work/Material/pyroot_python3/lhe_analyzer.py out/higgs/new/events.lhe out/higgs/new/histograms.root
cd out/higgs/new
python ../../../work/Material/pyroot_python3/plot_histos.py histograms.root
cd ../../..
```

The analyzer reads four-momenta and weights, producing **48 histograms**: four variables × (SM + 11 additional weights). The plotter writes four PDFs:

| File | Variable |
|---|---|
| `plot_mll.pdf` | $m_{e\mu}$ |
| `plot_mmv.pdf` | $m_{\mu\nu_\mu}$ |
| `plot_pTl1.pdf` | The larger charged-lepton pT |
| `plot_pTmu.pdf` | Muon pT |

The vertical axis is the bin's partial-width contribution $\Gamma_{\rm bin}$ [GeV], before division by bin width. The original plotter adds selected contributions to SM and displays their ratios underneath. Existing examples and variable explanations are in the [figure notes](figures/README.md).

## 6. Interpret the weights

The Higgs card's `cHl3` label is the **isolated interference contribution** and can be negative; it is not the complete `cHl3=1` target weight. The main tutorial's `cHl3_plus` is a complete target point. Interpret labels together with their cards.

To combine SM, interference, propagator and squared contributions, first add them for each event:

$$w_i=w_{{\rm SM},i}+w_{{\rm linear},i}+w_{{\rm prop},i}+w_{{\rm square},i}.$$

Sum these weights in bins and divide by the event count. Divide by bin width as well for a differential width. Calculate combined uncertainties from the per-event sums to retain their correlations. The original plotter supplies central-value curves.

## 7. Reproduce the existing 2,000-event example

The previous example remains available and runs in the same Python 3.12 environment:

```bash
mkdir -p out/higgs/reference
gzip -dc examples/reweighted/events.lhe.gz > out/higgs/reference/events.lhe
python work/Material/pyroot_python3/lhe_analyzer.py out/higgs/reference/events.lhe out/higgs/reference/histograms.root
cd out/higgs/reference
python ../../../work/Material/pyroot_python3/plot_histos.py histograms.root
cd ../../..
```

Integration validation generated a new 200-event sample and compared all 48 histograms of the existing 2,000-event example bin by bin. See the [validation record](validation.md).

## 8. Check both exercises

After the dimuon tutorial through the Parnassus comparison and both Higgs runs above, run these from the project root with the environment loaded.

```bash
python scripts/test_analysis.py
python scripts/validate.py
```

The first command runs four analysis tests. The second checks the documented event counts, weights and output files, compares the 48 reference Higgs histograms and writes `out/unified-validation/validation.json`.

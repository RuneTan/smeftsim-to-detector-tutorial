# UFO parameter reference

[English](README.md) | [简体中文](README.zh-CN.md)

This directory contains explanations and a static parameter reference for SMEFTsim v3.0.2. Restriction and input-card values come from `restrict_massless_Hvlvl.dat` and `param_card_Hvlvl.dat` in [Ilaria Brivio's June 2023 SMEFTsim tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23).

| File | Contents |
|---|---|
| [model_parameter_reference.md](model_parameter_reference.md) | Parameters by block, model defaults, restriction values, and values in `param_card_Hvlvl.dat` |
| [model_parameters.json](model_parameters.json) | Complete machine-readable parameter declarations and formulas |

These files describe static declarations. They are not an evaluated MadGraph model and do not replace a run's banner.
The parameter declarations in the index come from SMEFTsim, which is licensed under MIT. See
[SMEFTsim-MIT.txt](../../licenses/SMEFTsim-MIT.txt). The references retain their source and version information.

## 1. Which parameters does a UFO contain, and which should you set?

A UFO describes a model in a format the generator can read. Its files cover more than parameter tables:

| File | Main contents |
|---|---|
| `particles.py` | Particle names, mass/width references, spin, charge, color representation, and related properties |
| `parameters.py` | External input values and formulas for internal parameters derived from them |
| `couplings.py`, `vertices.py`, `lorentz.py` | Coupling expressions, particles connected by each vertex, and the vertex's Lorentz structure |
| `coupling_orders.py` | Definitions and limits for labels such as `NP` and `NPprop` |
| `propagators.py` | Custom propagators, including those for dummy fields |
| `decays.py` | Exported decay information for supported width-calculation functions |
| `restrict_*.dat` | Parameter values that simplify and fix the model at import time |

### Start by distinguishing external and internal parameters

The original tutorial UFO v3.0.2 defines 201 parameters in `parameters.py`: 118 `external` and 83 `internal`.
These are counts **before importing a restriction**. They are neither the number of parameters to adjust for this decay nor the number of independent EFT operators.
See [model_parameter_reference.md](model_parameter_reference.md) for every parameter's name, default, tutorial restriction value, and value listed in `param_card_Hvlvl.dat`.
Long formulas and machine-readable declarations are available in
[model_parameters.json](model_parameters.json).

| Category | Contents in this UFO | How to use it |
|---|---|---|
| `SMEFT`, `SMEFTcpv` | 60 ordinary components and 25 CP-violating components | Wilson coefficients are research or fit parameters; the SM does not uniquely predict their values |
| `SMEFTcutoff` | `LambdaSMEFT` | Set and record it explicitly together with the coefficients; it is 1,000 GeV in this example |
| `SMINPUTS` | `MW`, `Gf`, `aS` | Set electroweak inputs and the strong coupling; `MZ` is in the `MASS` block and is also an electroweak input |
| `MASS` | 11 mass inputs | Set kinematic masses; the restriction may fix light-particle masses to zero |
| `YUKAWA` | 9 dimensionful Yukawa inputs (in mass units), such as `ymb` and `ymt` | Model formulas convert these to Yukawa couplings; the inputs themselves are not dimensionless Yukawa couplings |
| `CKMBLOCK` | 4 CKM parameters | The tutorial restriction removes mixing and fixes the corresponding settings |
| `DECAY` | `WT`, `WZ`, `WW`, `WH` | Baseline total widths of the top quark, Z, W, and Higgs; distinct from the four-lepton partial width calculated here |
| `SWITCHES` | `linearPropCorrections` | A switch for propagator treatment; the tutorial restriction fixes it to 1 |
| `internal` | Charge, weak mixing angle, vacuum expectation value, CKM matrix elements, input shifts, width shifts, and related quantities | Calculated from model formulas and usually not set independently |

For example, internal parameters in the current `MwScheme` include
$\hat v=(\sqrt2 G_F)^{-1/2}$, $g_s=\sqrt{4\pi\alpha_s}$,
and $\Delta G_F=(2cHl3-cll1)\hat v^2/\Lambda^2$.
Changing an input or Wilson coefficient changes the related internal parameters through these formulas.
`aEW` is internal in this UFO, while the parameter with the same name can be an external input in `alphaScheme`.
Keep default values, internal formulas, and independently adjustable inputs distinct.

### Which values should you check now?

Initially retain the SM inputs and widths in `param_card_Hvlvl.dat` to reproduce the reference results. For each exercise, mainly check:

1. The model, flavor assumptions, input scheme, restriction, and [the process-order choices](../processes/README.md#3-coupling-order-options-select-amplitudes-then-terms-in-their-square).
2. The Wilson coefficients being studied and the values of the other retained coefficients; set them to zero for the SM starting point.
3. `LambdaSMEFT=1000` and the coefficient units.
4. The event count, random seed, cuts, and beam settings in `run_card.dat`. These are run settings rather than UFO model parameters.

The ordinary EFT inputs retained by this restriction are `cHbox`, `cHW`, `cHl3`, `cHq3`, and `cll1`.
Although `cHq3` is a quark operator coefficient, it can affect this leptonic process through a shift in the W total width.
`cHWB` is zero in this restriction. A weight with that name and a zero value in the reweighted file does not mean the corresponding vertices can be freely restored.

**Three sources underlie the default values:**

- **Measurements or reference theory calculations:** SM masses, couplings, and widths follow measurements or theoretical references adopted when the model was released.
  The parameter appendix in the manual lists sources individually; several use PDG 2020. The default $m_W=80.387$ GeV cites the Tevatron combination available at the time.
  Higgs and top widths follow the cited theoretical calculations. These values define the older tutorial's benchmark; they are not claimed to be today's latest values.
- **Theoretical definitions or calculations:** The model specifies charges and group representations. Internal couplings and input shifts follow from the Lagrangian and input scheme.
  These quantities do not each have an independently chosen empirical default.
- **Computational assumptions and learning benchmarks:** Zero Wilson coefficients define the SM starting point; they do not establish that experiments have proven every coefficient to be zero.
  $\Lambda=1$ TeV is a parameterization benchmark, rather than evidence of a new particle at 1 TeV.
  Zero light-particle masses are an approximation in this tutorial, and the propagator switch chooses a calculation method.

In particular, `cHbox=0.2`, `cHW=0.3`, `cHl3=0.5`, `cHq3=0.6`, and `cll1=0.7` in the restriction
retain and distinguish vertices; they are not fit results. `param_card_Hvlvl.dat` subsequently sets these five coefficients to zero for the SM starting point.
Import the restriction first, apply the parameter card, and finally check the resulting settings in each run's banner.
Use parameter cards for configuration instead of directly editing the original UFO's `parameters.py`.
See the [Parameter definitions appendix in the practical guide](https://arxiv.org/html/2012.11343v3) for definitions and sources.

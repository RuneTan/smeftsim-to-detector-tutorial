# Models, processes and coupling orders

[English](README.md) | [简体中文](README.zh-CN.md)

This guide explains the model, restriction and order syntax used in the [advanced Higgs exercise](../higgs.md).
Enter process commands directly in MadGraph. Parameter, run and reweight cards are obtained from the pinned tutorial and used in the local working directory.

## 1. Why this example uses this model

See [Flavor](../physics/README.md#5-flavor-how-new-interactions-distinguish-fermion-generations) and [Scheme](../physics/README.md#6-scheme-which-measurements-determine-the-electroweak-parameters) in the physics guide for the meaning of these choices. This exercise uses:

```text
SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl
```

| Name component | Meaning | Effect of the choice |
|---|---|---|
| `U35` | A $U(3)^5$ flavor-symmetry assumption | Constrains the relationships between coefficients for different generations |
| `MwScheme` | Uses $m_W,m_Z,G_F$ as electroweak inputs | Determines which quantities are inputs and which parameter relations contain EFT corrections |
| `UFO` | An event-generator model format | MadGraph reads parameters, vertices, and related information from it |
| `massless_Hvlvl` | The process-specific restriction supplied with this tutorial | Simplifies settings such as light-particle masses while retaining the EFT vertices needed for the exercise |

The alternative `alphaScheme` uses $\alpha_{\rm em},m_Z,G_F$. Changing schemes requires more than changing a filename: observables, parameter relations, and EFT input shifts must be handled consistently. For research, choose the flavor model and input scheme according to the physics question, and document the model assumptions.

## 2. A restriction is different from a parameter card

A restriction simplifies the model **when it is imported**. If a coefficient is restricted to zero at this stage, its vertices may be removed. Increasing the coefficient later in the exported parameter card cannot restore those vertices.

`restrict_massless_Hvlvl.dat` uses some nonzero coefficients to retain the vertices needed for this example. Those import-time values are not the physical point you ultimately intend to generate. After exporting the process, copy `param_card_Hvlvl.dat` to its `Cards/param_card.dat`, then set the desired coefficients. This parameter card sets the adjustable EFT coefficients in the example to zero, providing an SM starting point.

The tutorial UFO uses Python 2 import syntax. The process cards allow MadGraph to convert the **working copy** to Python 3 syntax. The original model in `tutorial` is retained; the local working copy has been converted, imported, and used successfully to generate new events.

## 3. Coupling-order options: select amplitudes, then terms in their square

The following is a **syntax example for MadGraph's internal commands**. Read it here; do not execute it in Bash. If you start MadGraph from the project root `~/smeftsim`, enter each line at the `MG5_aMC>` prompt and press Enter. See [Generate events and all weights](../higgs.md#4-generate-events-and-all-weights) for the actual generation steps.

```text
import model ./work/Material/SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=0
```

`h` is the initial Higgs, `>` indicates the reaction direction, `ve~` is the electron antineutrino, and `vm` is the muon neutrino. Then use `display diagrams` to inspect the diagrams, or `output directory_name` to export the process code. A successful `output` command has not yet generated events; integration and event generation happen in the subsequent `launch` stage.

### First level: how many EFT insertions are allowed in an amplitude?

`NP` is a counting label assigned to couplings in the model. Ordinary dimension-six vertices and dimension-six input-parameter corrections carry the corresponding NP order; SM terms have `NP=0`. This order is distinct from a Wilson coefficient's value: `NP=1` does not mean `cHl3=1`. It does not mean a one-loop calculation either; this example still uses tree-level matrix elements.

Ignoring propagator corrections for the moment, write the amplitude with at most one ordinary EFT insertion as

$$
\mathcal M=\mathcal M_0+\mathcal M_6,
\qquad \mathcal M_6=\sum_i\frac{c_i}{\Lambda^2}\mathcal A_i.
$$

$\mathcal M_0$ is the SM amplitude. $\mathcal M_6$ already includes the Wilson coefficients and $1/\Lambda^2$. Allowing two EFT insertions would introduce additional amplitudes; this tutorial excludes them by setting the upper bound to 1.

| Syntax | Meaning in the MadGraph 2.9 tree-level syntax used in this tutorial |
|---|---|
| `NP=0` | Allow only amplitudes with ordinary NP order zero |
| `NP=1` or `NP<=1` | Set an upper bound of 1: allow the SM amplitude and amplitudes with one ordinary EFT insertion |
| `NP==1` | Require an order of exactly 1: select amplitudes with one ordinary EFT insertion; in this example the rate contains their squared contribution |

Distinguish the single equals sign from the double equals sign. Here, `=` sets an upper bound, whereas `==` selects an exact order. These statements apply to this generator version and its tree-level processes; check before applying them to the NLO syntax of another version.

### Second level: which term in the squared amplitude is retained?

The rate depends on the squared amplitude:

$$
|\mathcal M_0+\mathcal M_6|^2
=\underbrace{|\mathcal M_0|^2}_{\text{SM: total NP order 0}}
+\underbrace{2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)}_{\text{interference: total NP order 1}}
+\underbrace{|\mathcal M_6|^2}_{\text{dimension-six squared: total NP order 2}}.
$$

`NP^2` is MadGraph's syntax for an order in the **squared amplitude**. It adds the NP orders from the two sides of the product: SM × SM gives $0+0=0$, SM × EFT gives $0+1=1$, and EFT × EFT gives $1+1=2$. **It does not mathematically square the integer NP order.**

Each row below also includes `SMHLOOP=0 NPprop=0`, excluding explicit propagator corrections for now:

| Order options | Contribution calculated | Includes the SM baseline? |
|---|---|---|
| `NP=0` | $\lvert\mathcal M_0\rvert^2$ | Yes |
| `NP=1` | $\lvert\mathcal M_0\rvert^2+2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)+\lvert\mathcal M_6\rvert^2$ | Yes |
| `NP=1 NP^2<=1` | $\lvert\mathcal M_0\rvert^2+2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)$ | Yes |
| `NP=1 NP^2==1` | $2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)$; only the interference correction | No |
| `NP==1`, or `NP=1 NP^2==2` | $\lvert\mathcal M_6\rvert^2$; only the dimension-six squared contribution | No |

Thus, “one insertion” in `NP==1` refers to the amplitude. To calculate a rate, that amplitude is still multiplied by its complex conjugate. For one coefficient, $|\mathcal M_6|^2=(c/\Lambda^2)^2|\mathcal A|^2$, so this is the term quadratic in that coefficient. It contains no SM amplitude and therefore no SM–EFT interference. If several coefficients are nonzero, this square also contains cross terms between different dimension-six amplitudes.

For an algebraic illustration only, take real numbers $\mathcal M_0=2$ and $\mathcal M_6=0.3$. The SM term is 4, the interference is 1.2, and the squared term is 0.09. `NP==1` gives 0.09; the SM plus the ordinary linear correction gives 5.2; the sum of all three terms is 5.29. These are illustrative numbers, not local physics results.

`SMHLOOP` labels certain SM loop-generated effective Higgs couplings in the model. `SMHLOOP=0` disables those vertices; it is not a general switch for computing or excluding all loop diagrams. `QCD` and `QED` are other coupling-order labels. Here `QED` also includes structures involving weak and Yukawa couplings, so it should not be interpreted simply as a count of photon vertices. More specific labels, such as `NPcHl3` and `NPcHW`, can select an operator's contribution.

### Dummy vertices: auxiliary fields for first-order propagator corrections

A propagator describes how an internal particle connects two vertices. If SMEFT changes its mass or width, its propagator changes too. A first-order expansion of a propagator $P(m,\Gamma)$ can be written schematically as

$$
P(m_0+\delta m,\Gamma_0+\delta\Gamma)
\simeq P_{\rm SM}
+\delta m\left.\frac{\partial P}{\partial m}\right|_0
+\delta\Gamma\left.\frac{\partial P}{\partial\Gamma}\right|_0
\equiv P_{\rm SM}+\Delta P.
$$

$m_0,\Gamma_0$ are the baseline mass and width; $\delta m,\delta\Gamma$ are the shifts induced by Wilson coefficients. To supply $\Delta P$ to the generator, SMEFTsim introduces **dummy auxiliary fields**, such as `W1`, `Z1`, `H1`, and `t1`, with custom propagators representing this correction. They are not additional physical W, Z, Higgs, or top particles.

The model copies the corresponding SM vertices and replaces the ordinary field with a dummy field. Such a vertex is called a **dummy vertex**. An internal W line in this example can be illustrated as

```text
Ordinary term:    left vertex -------- ordinary W propagator -------- right vertex
Correction term: left dummy vertex -------- W1 carrying ΔP -------- right dummy vertex
                     NPprop=1                                         NPprop=1
```

The two ends of this auxiliary internal line each contribute one label, so the correction amplitude has total `NPprop` order 2. In general, a vertex's `NPprop` order equals its number of dummy legs; this example has one internal line connecting two endpoints. **An order label of 2 does not mean two EFT insertions, or corrections to two different propagators.**

Denote the ordinary SM amplitude by $\mathcal M_0$ and this propagator-correction amplitude by $\mathcal M_P$. Their interference is $2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_P)$, with squared-amplitude order $0+2=2$ in `NPprop^2`. Despite this label of 2, $\mathcal M_P$ is still linear in the Wilson coefficients, and the interference is still a $1/\Lambda^2$ correction. Auxiliary-field labels follow an implementation convention; they are not directly the powers of the EFT scale.

This example therefore uses

```text
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=2 NPprop^2==2
```

`NP=0` excludes ordinary EFT vertices and input-parameter insertions; propagator corrections use the separate `NPprop` mechanism. `NPprop=2` sets the upper bound at amplitude level, allowing the ordinary SM amplitude and an amplitude with one auxiliary propagator. `NPprop^2==2` then selects only their interference. It retains neither the SM baseline nor $|\mathcal M_P|^2$.

This feature also requires the model to allow dummy couplings and set `linearPropCorrections` to a nonzero value. **Both are already configured in this tutorial:** `coupling_orders.py` sets `NPprop.expansion_order=99`, and `restrict_massless_Hvlvl.dat` fixes `linearPropCorrections=1` when the model is imported. The parameter card therefore does not list this switch separately; you do not need to add a `SWITCHES` block. Other SMEFTsim UFO variants may default to 0, so copying this process command alone does not establish that the feature is enabled.

### Four contributions in the original tutorial

The table retains the original tutorial's sample names to distinguish the contributions. The current [advanced Higgs exercise](../higgs.md) computes several reweighting points from one SM baseline sample; it does not require generating these four directories separately.

| Original sample name | Order options | Content |
|---|---|---|
| `Hvlvl_SM` | `SMHLOOP=0 NP=0 NPprop=0` | SM baseline |
| `Hvlvl_SMEFT` | `SMHLOOP=0 NP==1 NPprop=0` | Ordinary dimension-six amplitude squared |
| `Hvlvl_SMEFT_linear` | `SMHLOOP=0 NP=1 NP^2==1 NPprop=0` | Ordinary SM–dimension-six interference |
| `Hvlvl_SMEFT_prop` | `SMHLOOP=0 NP=0 NPprop=2 NPprop^2==2` | SM–propagator-correction interference |

These are distinct contributions. To construct a linear prediction at a given parameter point, combine the SM baseline, ordinary interference, and propagator interference. If you also choose to retain the ordinary dimension-six squared term, add that contribution. The squared term does not include every contribution at $1/\Lambda^4$; see [Linear and quadratic terms](../physics/README.md#4-why-distinguish-linear-and-quadratic-terms).

Do not add `Auto` width calculations without checking the convention: when explicit propagator corrections are enabled, doing so may mix in or double-count some effects. Keep the width values and treatment specified in `param_card_Hvlvl.dat` for this exercise.

Check the syntax and implementation against the Usage in MadGraph and Propagator corrections sections of the [SMEFTsim manual](https://arxiv.org/html/2012.11343v3) and the [2023 tutorial commands](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23#running-mg-and-looking-at-diagrams).

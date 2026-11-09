# SMEFT background

[English](README.md) | [简体中文](README.zh-CN.md)

The exercise settings referenced below follow [Ilaria Brivio's June 2023 SMEFTsim tutorial](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23); the model and theory references are listed in the [project README](../../README.md#sources-and-acknowledgments).

You can begin the exercises before studying the full theory. Return to the relevant section when a model choice or a plot raises a question.

- [Warsaw basis and derivatives in field strengths](#3-what-is-the-warsaw-basis).
- [Coefficients and energy scale](#2-wilson-coefficients-the-scale-and-units); [linear and quadratic terms](#4-why-distinguish-linear-and-quadratic-terms).
- [Flavor](#5-flavor-how-new-interactions-distinguish-fermion-generations) and [electroweak input schemes](#6-scheme-which-measurements-determine-the-electroweak-parameters).
- [Differential widths and histogram-bin contents](#7-differential-widths-distributing-a-decay-channels-rate-over-kinematic-regions).

## 1. Why use an effective field theory?

The Standard Model (SM) describes the known elementary particles and their interactions. If the characteristic scale of new physics is high, an experiment may not have enough energy to produce the associated new particles directly. New physics can nevertheless cause small changes to the production rates, decay widths, and kinematic distributions of known particles.

An effective field theory (EFT) represents these low-energy effects as additional interaction terms. It lets us study measurable deviations without first choosing a specific model of high-energy new physics. **SMEFT** stands for **Standard Model Effective Field Theory**: it uses the SM fields, respects the SM gauge symmetries, and organizes corrections by operator dimension. Electroweak symmetry is normally realized linearly.

Write the Lagrangian as

$$
\mathcal L_{\mathrm{SMEFT}}
=\mathcal L_{\mathrm{SM}}
+\sum_{d>4}\sum_i \frac{c_i^{(d)}}{\Lambda^{d-4}}Q_i^{(d)}.
$$

| Symbol | Meaning | Intuitive role |
|---|---|---|
| $\mathcal L$ | Lagrangian | Determines which particles interact and how |
| $Q_i^{(d)}$ | An operator of mass dimension $d$ | An allowed additional interaction structure |
| $c_i^{(d)}$ | Wilson coefficient | Controls the strength and sign of that structure |
| $\Lambda$ | Characteristic new-physics scale | Suppresses contributions from higher-dimensional operators |

This tutorial focuses on dimension-six terms and uses dimensionless coefficients:

$$
\mathcal L=\mathcal L_{\mathrm{SM}}+\sum_i\frac{c_i}{\Lambda^2}Q_i^{(6)}.
$$

SMEFT can also contain dimension-five and other terms. The dimension-six scope of this tutorial does not cover every possible new-physics effect. As the relevant energies approach the new-physics scale, the truncated expansion needs to be reassessed. A numerical result from the software alone does not establish that the EFT is valid in that region.

## 2. Wilson coefficients, the scale, and units

The example parameter card sets `LambdaSMEFT = 1000` in GeV, corresponding to $\Lambda=1\ \mathrm{TeV}$. `cHl3 = 1` sets the dimensionless coefficient to 1; together with $1/\Lambda^2$, it controls the correction. Some papers instead call $c_i/\Lambda^2$ the Wilson coefficient and quote it in $\mathrm{TeV}^{-2}$. Before comparing publications or samples, establish the notation, units, and normalization.

The same numerical value of `cHl3` should not be assumed to describe the same physical setting under different flavor assumptions, coefficient definitions, or input schemes without the necessary conversion.

## 3. What is the Warsaw basis?

**It is an independent set of building blocks for dimension-six interactions.** First specify the fields, symmetries, and order of the expansion. Then choose an independent set of operators that can represent the interactions within that scope. The Warsaw basis is one such convention; SMEFTsim uses it to name operators and Wilson coefficients. See the [original Warsaw-basis paper](https://arxiv.org/abs/1008.4884).

Why does independence matter? As a purely illustrative example, suppose three candidate structures satisfy $Q_3=Q_1+2Q_2$. Then

$$
c_1Q_1+c_2Q_2+c_3Q_3=(c_1+c_3)Q_1+(c_2+2c_3)Q_2.
$$

There are only two independent directions. Treating all three coefficients as independent parameters would describe the same physical effects redundantly. In actual SMEFT, redundancies involve integration by parts, algebraic identities, and equivalences obtained through equations of motion or field redefinitions at the specified EFT order. Different forms of the Lagrangian can yield the same physical scattering or decay predictions. The $Q_3$ relation above is an illustration, rather than an identity between specific Warsaw operators.

When changing to another complete basis, transform both operators and coefficients; the physical predictions remain consistent. A setting with “one coefficient nonzero and all others zero” is generally basis-dependent: it can correspond to several nonzero coefficients in another basis.

**You do not need to learn the entire theory before starting.** Understand the operators relevant to this process, coefficient normalization, flavor assumptions, input scheme, interference, and EFT truncation. That is enough to give the tutorial a physical interpretation. For research, study the operators relevant to your question in greater depth. If you intend to derive Feynman rules, change bases, match a high-energy model onto SMEFT, or study renormalization-group evolution, work through gauge invariance, integration by parts, removing redundancies with equations of motion, matching, and renormalization. There is no need to memorize the whole operator table at the outset.

Start with four names:

| Coefficient | Intuitive description of the structure | What to observe in this Higgs-decay exercise |
|---|---|---|
| `cHbox` | A derivative structure acting on Higgs bilinears | Its linear contribution here mainly produces an overall rescaling |
| `cHW` | An interaction between the Higgs and weak gauge-field strengths | Momentum dependence can change the shape of a distribution |
| `cHl3` | A coupling between the Higgs weak current and the left-handed lepton weak current | Affects vertices, input-parameter relations, and W-width corrections |
| `cll1` | A four-lepton interaction with a specific flavor contraction | Affects this example through electroweak input-parameter relations |

### Where are the derivatives?

Consider

$$
Q_{HW}=(H^\dagger H)W^I_{\mu\nu}W^{I\mu\nu}.
$$

$H$ is the Higgs doublet. Distinguish the gauge field $W^I_\mu$ from the **field strength** $W^I_{\mu\nu}$ constructed from it. With the positive-sign convention for the covariant derivative used in the SMEFTsim manual, the field strength is

$$
W^I_{\mu\nu}
=\partial_\mu W^I_\nu-\partial_\nu W^I_\mu
-g_2\epsilon^{IJK}W^J_\mu W^K_\nu.
$$

| Symbol | Meaning |
|---|---|
| $\mu,\nu$ | Spacetime indices |
| $I,J,K=1,2,3$ | $SU(2)_L$ gauge-group indices; they are not fermion-generation indices |
| $g_2$ | Weak gauge coupling; also denoted by $g_W$ in the original manual |
| $\epsilon^{IJK}$ | Antisymmetric tensor; the final term represents the self-interactions of a non-Abelian gauge field |

The derivatives are already contained in the shorthand $W^I_{\mu\nu}$. A different sign convention for the covariant derivative changes the sign of the final term accordingly; use the conventions consistently throughout. The fact that the field strength contains derivatives is unchanged. See the [Basics and notation section of the SMEFTsim manual](https://arxiv.org/html/2012.11343v3).

In natural units, $H$ and $W_\mu$ each have mass dimension 1, as does a derivative. Thus $W_{\mu\nu}$ has dimension 2 and $Q_{HW}$ has dimension $2+2+2=6$.

To see how this affects a Higgs decay, write $H=(0,(v+h)/\sqrt2)^T$ in unitary gauge, so $H^\dagger H=(v^2+2vh+h^2)/2$. Here $v$ is the Higgs vacuum expectation value and $h$ the physical Higgs field. The interaction includes

$$
\frac{c_{HW}}{\Lambda^2}Q_{HW}
\supset \frac{c_{HW}v}{\Lambda^2}hW^I_{\mu\nu}W^{I\mu\nu}.
$$

A derivative acting on a plane wave gives $\partial_\mu e^{-ip\cdot x}=-ip_\mu e^{-ip\cdot x}$. Momentum factors therefore appear in the vertex, including tensor structures of the form $p_1\!\cdot p_2\,g^{\mu\nu}-p_1^\nu p_2^\mu$, where $p_1,p_2$ are the two gauge-boson momenta. These structures can affect different kinematic regions differently, changing the distribution's shape. This expansion only illustrates the origin of that dependence; an actual calculation must also treat kinetic-term normalization and input-parameter shifts consistently.

Consult the SMEFTsim manual for the precise flavor contractions and normalizations. In particular, do not treat `cll` and `cll1` as the same parameter.

## 4. Why distinguish linear and quadratic terms?

Schematically, the amplitude is

$$
\mathcal M=\mathcal M_{\mathrm{SM}}+\sum_i\frac{c_i}{\Lambda^2}\mathcal M_i^{(6)}+\cdots.
$$

Squaring gives the SM term, interference between the SM and dimension-six amplitudes, and the square of the dimension-six amplitude:

```math
|\mathcal M|^2=|\mathcal M_{\mathrm{SM}}|^2
+2\sum_i\frac{c_i}{\Lambda^2}\mathrm{Re}(\mathcal M_{\mathrm{SM}}^{\ast}\mathcal M_i^{(6)})
+\sum_{ij}\frac{c_i c_j}{\Lambda^4}\mathcal M_i^{(6)}\mathcal M_j^{(6)\ast}+\cdots.
```

The interference term can be negative because it is a correction, rather than a separate positive probability. Retaining the dimension-six squared term alone does not give a complete expansion through $1/\Lambda^4$: interference between the SM and dimension-eight amplitudes can also occur at that order. Whether to retain only linear terms or also quadratic terms is therefore a physical choice that must be documented.

## 5. Flavor: how new interactions distinguish fermion generations

**The flavor choice specifies the structure of Wilson coefficients in generation space.** The SM has three generations of fermions: for example, charged leptons $e,\mu,\tau$, up-type quarks $u,c,t$, and down-type quarks $d,s,b$. Operators involving fermions generally carry generation indices. Their coefficients can be matrices or higher-rank tensors, rather than single numbers.

For a left-handed lepton operator, write

$$
Q_{Hl,pr}^{(3)}
=(H^\dagger i\overleftrightarrow D^{\,I}_\mu H)
(\bar l_p\tau^I\gamma^\mu l_r),
\qquad p,r=1,2,3.
$$

$l_p$ is the left-handed lepton doublet of generation $p$, and $\tau^I$ are the Pauli matrices. The first bracket is the Higgs weak current and the second the lepton weak current. Diagonal coefficients control individual generations; off-diagonal structures can introduce lepton-flavor change. This is the defining structure of a Warsaw operator. The flavor model determines the specific input-parameter names and allowed components.

In the tutorial's `U35` model, the coefficient matrix is restricted to

$$
[c_{Hl}^{(3)}]_{pr}=c_{Hl3}\,\delta_{pr}.
$$

$\delta_{pr}$ is 1 when $p=r$ and 0 otherwise. Thus `cHl3` controls this interaction for all three generations simultaneously; you cannot use it to change only the electron coupling while leaving the muon coupling unchanged. This does not require the three generations to have equal masses. Other operators may involve Yukawa factors or multiple independent flavor contractions, so this simple relation should not be applied to every operator.

### What the five choices allow

The table summarizes the SMEFTsim 3 implementations. See [section 3 of the practical guide](https://arxiv.org/html/2012.11343v3#S3) for precise definitions.

| Choice | Main assumption | Physical freedom and use |
|---|---|---|
| `general` | No additional restriction from the flavor symmetries below; retains allowed generation-index structures, subject to operator constraints such as Hermiticity | Allows nonuniversal generation-dependent couplings, flavor change, and arbitrary allowed flavor structures; has the most parameters |
| `U35` | Uses $U(3)^5$ flavor symmetry, with Yukawa matrices as sources of breaking; retains the leading allowed structure for each operator | Many current interactions are generation-universal, while chirality-flipping structures depend on Yukawa matrices; useful for learning with fewer parameters |
| `MFV` | Minimal Flavor Violation: SM Yukawa matrices organize flavor breaking; specified higher Yukawa insertions are retained compared with `U35` | Allows correlated nonuniversality and flavor change determined by Yukawa/CKM structures, rather than arbitrary independent flavor changes; this implementation introduces no new source of CP violation and uses a finite Yukawa expansion |
| `top` | Uses $U(2)^3$ for quarks, treating the first two generations together and the third independently; uses $U(1)_{l+e}^3$ for leptons | Allows separate study of top/bottom and light-quark effects; electron, muon, and tau couplings may differ, while individual lepton numbers are preserved |
| `topU3l` | Uses the same quark assumptions as `top`, with stronger $U(3)_l\times U(3)_e$ lepton constraints and leading Yukawa structures | The third quark generation remains independent; there are fewer lepton parameters, and the relevant current couplings are generation-universal |

The “five” in `U35` refers to five fermion multiplets: left-handed quarks $q$, right-handed up-type quarks $u$, right-handed down-type quarks $d$, left-handed leptons $l$, and right-handed charged leptons $e$. Each multiplet has its own $U(3)$ rotation in generation space. SM Yukawa matrices mean that masses and mixing do not respect this symmetry exactly. Treating Yukawa matrices as **spurions** means formally assigning them transformation rules and using them to organize flavor-symmetry breaking systematically.

The difference between `U35` and `MFV` depends on which Yukawa structures are retained. Do not reduce it to “no flavor change” versus “arbitrary flavor change.” Also, SMEFTsim's `top` and `topU3l` implementations set the CKM matrix to the identity, neglecting quark mixing. Check this approximation if your question depends on CKM effects or flavor change.

**What should you choose for this exercise?** Use the tutorial's `U35` choice first, so the parameter definitions match the reference results. If you later want to test whether electron and muon couplings differ, the `U35` parameter `cHl3` does not provide that freedom. Choose an appropriate flavor structure and check the coefficient conversion. A more general model is not automatically more suitable; the choice should express your research hypothesis.

## 6. Scheme: which measurements determine the electroweak parameters?

**Here, “scheme” means an electroweak input scheme.** The electroweak Lagrangian parameters $g_1,g_2,v$ must be determined from measurements: $g_1$ is the hypercharge gauge coupling, $g_2$ the weak gauge coupling, and $v$ the Higgs vacuum expectation value. Other parameters, such as the Higgs mass, have their own inputs; this section focuses on these three electroweak parameters.

At SM tree level, their relations to common observables are

$$
m_W=\frac{g_2v}{2},\qquad
m_Z=\frac{v}{2}\sqrt{g_1^2+g_2^2},\qquad
G_F=\frac{1}{\sqrt2 v^2},\qquad
\alpha_{\rm em}=\frac{e^2}{4\pi},\quad
e=\frac{g_1g_2}{\sqrt{g_1^2+g_2^2}}.
$$

$m_W,m_Z$ are the W and Z masses, $G_F$ the Fermi constant extracted from muon decay, and $\alpha_{\rm em}$ the electromagnetic fine-structure constant. Four quantities are related to three parameters. Choose three as inputs and predict the remaining one; in SMEFT, the relations include Wilson-coefficient corrections.

| Scheme | Fixed electroweak inputs | Quantity predicted through theoretical relations | How to interpret the SMEFT effects |
|---|---|---|---|
| `alphaScheme` | $\alpha_{\rm em},m_Z,G_F$ | $m_W$ | Coefficient-dependent corrections can shift the predicted W mass |
| `MwScheme` | $m_W,m_Z,G_F$ | $\alpha_{\rm em}$ | The W mass remains fixed as an input; the corresponding effects appear through other parameters, vertices, and observables |

Check the precise input definitions, numerical values, and electromagnetic-coupling scale in the parameter card and manual. Do not mix tree-level relations indiscriminately with precision SM relations that include loop corrections. See [section 4 of the SMEFTsim manual](https://arxiv.org/html/2012.11343v3#S4) for definitions and derivations.

### Why does `cHl3` affect input-parameter relations?

Muon decay determines $G_F$, and `cHl3` and certain four-lepton coefficients modify that decay. Schematically, the SMEFT relation is

$$
G_F=\frac{1}{\sqrt2 v_T^2}(1+\Delta G_F).
$$

$v_T$ is the Higgs vacuum expectation value in SMEFT, and $\Delta G_F$ is a dimensionless correction built from Wilson coefficients. Both input schemes treat the measured $G_F$ as an input. Changing the relevant coefficients therefore changes the inferred $v_T$ and related parameters. This can affect another process even when that process has no explicit four-lepton contact vertex. In the tutorial's `U35` model, `cHl3` and `cll1` enter this input correction. Include this effect together with the operator's direct changes to the decay vertices.

**How should you compare schemes?** The two schemes are different parameterizations of the same theory. Predictions should agree to the calculated accuracy when the inputs describe the same physical point, the parameters are converted consistently, and the perturbative/EFT orders match. Fixing two separate sets of experimental central values and simply copying coefficient values between them may not compare the same physical point. Finite-order truncation and omitted higher-order corrections can also produce differences. Fixing $m_W$ in `MwScheme` does not eliminate SMEFT corrections to W interactions or the W width.

Thus, **the basis supplies coordinates; the flavor choice restricts allowed flavor structures; the input scheme specifies the measurements used to determine parameters.** This exercise uses `U35 + MwScheme` to match the reference calculation, rather than to claim that this combination suits every study. The `massless_Hvlvl` part of the model name is a separate, process-specific restriction; see the [process-card guide](../../docs/processes/README.md).

## 7. Differential widths: distributing a decay channel's rate over kinematic regions

### Total width, partial width, and branching ratio

A width $\Gamma$ describes how quickly a particle decays. In the parent's rest frame, under the usual exponential-decay approximation, the survival probability is $P_{\rm survive}(t)=e^{-\Gamma_{\rm tot}t/\hbar}$. A larger total width means a shorter mean lifetime: $\tau=\hbar/\Gamma_{\rm tot}$. In natural units, $\hbar=1$ and $\tau=1/\Gamma_{\rm tot}$; restore $\hbar$ when expressing the lifetime in seconds.

| Quantity | Meaning |
|---|---|
| $\Gamma_{\rm tot}$ | The sum of partial widths for all allowed decay channels; determines the parent's lifetime |
| $\Gamma_f$ | The partial width for decay into a specified final state $f$; here $h\to e^-\bar\nu_e\mu^+\nu_\mu$ |
| $\mathrm{BR}_f=\Gamma_f/\Gamma_{\rm tot}$ | Probability that a decay ends in this final state: the branching ratio |

The locally obtained value of approximately $1.01\times10^{-5}\ \mathrm{GeV}$ is the partial width of this four-lepton channel. It is not the Higgs total width and cannot by itself be used to calculate the Higgs lifetime.

### Why use a differential width?

Even within one final state, events have different electron energies, pair invariant masses, and angles. For a kinematic variable $X$, **$d\Gamma_f/dX$ describes how the partial width is distributed across regions of $X$.** For example, with $X=m_{e\mu}$, it tells us how much decay rate each electron–muon invariant-mass range contributes.

$$
\Delta\Gamma_f[a,b]=\int_a^b\frac{d\Gamma_f}{dX}\,dX,
\qquad
\Gamma_f=\int_{\text{full range}}\frac{d\Gamma_f}{dX}\,dX.
$$

The **area** under a segment of the curve is that region's partial width; the full area is the channel's partial width $\Gamma_f$. The height at a point is a density, not a probability. The notation $d\Gamma_f/dX$ does not mean differentiating a fixed total width with respect to $X$. It denotes the contribution in a small interval, $d\Gamma_f\simeq(d\Gamma_f/dX)\,dX$. Equivalently, define the cumulative partial width up to $X=x$, then differentiate it with respect to $x$ to obtain this density.

To compare only kinematic shapes conditional on this final state, normalize it as

$$
p(X\mid f)=\frac{1}{\Gamma_f}\frac{d\Gamma_f}{dX},
\qquad \int p(X\mid f)\,dX=1.
$$

This conditional probability density differs from a branching ratio. The former describes the distribution of $X$ after selecting the final state; the latter is the fraction of all decays that enter the final state. Two theories can have the same partial width for a channel but different shapes, or the same shape but different partial widths. The momentum structure associated with `cHW` can change the shape. Multiplying every bin by one constant changes only the overall normalization.

### Relating this to a histogram bin

For a pure-SM unweighted sample, suppose $n_k$ out of $N$ events enter bin $k$, whose width is $\Delta X_k$. Normalizing to the generator's reported $\Gamma_f$ gives

$$
\Delta\Gamma_{f,k}\simeq\Gamma_f\frac{n_k}{N},
\qquad
\left(\frac{d\Gamma_f}{dX}\right)_k
\simeq\frac{\Gamma_f n_k}{N\,\Delta X_k}.
$$

**For illustration only**, take $\Gamma_f=10^{-5}\ \mathrm{GeV}$ and suppose 200 of 2,000 events fall into a mass bin of width 5 GeV. The bin contributes $10^{-6}\ \mathrm{GeV}$, and its mean density is $2\times10^{-7}\ \mathrm{GeV}/\mathrm{GeV}$. Conditional on this final state, the region contains 10% of the events. These bin counts are illustrative, rather than local measurements.

If $X$ is in GeV, $d\Gamma_f/dX$ has units GeV/GeV, whereas the normalized shape $p(X\mid f)$ has units $\mathrm{GeV}^{-1}$. Check whether a plot shows the width per bin or a differential width after division by the bin width.

This project uses `lhe_analyzer.py`, which normalizes by the total event count and does not divide again by the bin width. The current plotted bin content is therefore the bin's partial width $\Delta\Gamma_{f,k}$. Divide by $\Delta X_k$ to obtain the bin-averaged differential width. For weighted samples, sum the weights rather than simply counting events.

### Optional: how this connects to the matrix element

For the four-body decay of the spin-zero Higgs in this example, natural units give

$$
d\Gamma_f=\frac{1}{2m_h}\sum_{\text{final-state spins}}|\mathcal M|^2\,d\Phi_4,
\qquad
d\Phi_n=(2\pi)^4\delta^{(4)}\!\left(P-\sum_i p_i\right)
\prod_{i=1}^{n}\frac{d^3\mathbf p_i}{(2\pi)^3\,2E_i}.
$$

$\mathcal M$ is the decay amplitude; $P$ the parent's four-momentum; $p_i,E_i$ the final-state four-momenta and energies; and $d\Phi_n$ the final-state phase space with four-momentum conservation. Select an interval of $X$ and integrate over the remaining kinematic degrees of freedom to obtain that interval's partial width. The expression above applies to this example's distinguishable final-state particles. Other processes may require initial-state spin averaging or identical-particle symmetry factors. See the Decays section of the [PDG Kinematics review](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf) for conventions and a general explanation.

A separate linear interference contribution $d\Gamma_{\rm int}/dX$ can be negative. It corrects the physical distribution; it is not an independent decay channel that can be normalized to a positive probability density. When reading the plots in the [Higgs LHE → ROOT → PDF exercise](../higgs.md#5-lhe--root--pdf), first establish whether a curve represents the complete prediction, the SM plus one correction, or the correction alone.

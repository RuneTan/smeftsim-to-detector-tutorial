# Third-party sources and license scope

[English](THIRD_PARTY_NOTICES.md) | [简体中文](THIRD_PARTY_NOTICES.zh-CN.md)

Checked on 2026-10-15. This file records component sources and license information;
it does not replace an upstream license.

## SMEFTsim model and parameter material

Source: [SMEFTsim](https://github.com/SMEFTsim/SMEFTsim), tutorial model v3.0.2.
The official v3.0.2 tag carries the MIT license, Copyright (c) 2020 SMEFTsim.
The full text is retained in [licenses/SMEFTsim-MIT.txt](licenses/SMEFTsim-MIT.txt).

The parameter index records model declarations, formulas and numerical card settings.
It is not a new physical model. The theory references are listed in the [project README](README.md).
The model source is obtained upstream and is not bundled here.

## Independent 2023 tutorial

Author: Ilaria Brivio.
Source: [SMEFTsim_tutorial_June23](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23),
commit `92ffde994d7c0d90554ee629cc477ee171c76b84`.

The processes, cards, restriction, analyzer and plotting method follow this tutorial.
No LICENSE file was identified in the pinned tutorial checkout.
The MIT license of the SMEFTsim model is not assumed to license the independent tutorial scripts.

Local tutorial downloads and author-derived Python files under `work/Material` are excluded from Git.
Compatibility changes consist of tab expansion, Python 2 syntax conversion, `file()` to `open()`
and the Python 3 interpreter line. The project's `scripts/fix_axes.py` additionally corrects local labels and layout and enables embedded PDF fonts, without changing histogram calculations. Preparation instructions are in the
[working-copy guide](docs/setup/README.md).

## MadGraph and ROOT

MadGraph5_aMC@NLO 2.9.27, MadTeam:
the pinned source root `LICENSE` is adapted from Illinois/NCSA.
Its unmodified text is retained in [licenses/MadGraph-NCSA.txt](licenses/MadGraph-NCSA.txt).
Vendor components may use other licenses. Generator source and binaries are not distributed here.

ROOT/PyROOT uses [LGPL 2.1 or later](https://root.cern/about/license/).
It is called in the local environment; ROOT installations and shared libraries are not bundled.

PDF font embedding uses local [Ghostscript](https://www.ghostscript.com/licensing/) (AGPL-3.0-or-later); its executable is not bundled.
Published PDFs embed subsets of [URW Base 35 fonts](https://github.com/ArtifexSoftware/urw-base35-fonts), licensed under AGPL-3.0 with an explicit document-embedding exception. The copyright, exception and license text are retained in [licenses/URW-fonts.txt](licenses/URW-fonts.txt).

## Locally generated example

`examples/reweighted` comes from 2,000 events generated and reweighted locally.
It is not a copy of the upstream reference archive.
The public LHE omits the full generator banner and embedded card templates.
Its numerical initialization block, event records and weights are preserved.
The original local run remains unchanged; its checksum and input settings are recorded in `metadata.json`.

The PDF and PNG plots use the upstream plotting method and are attributed accordingly.
This notice does not claim that the software, model or plotting algorithm was created here.
It does not imply upstream endorsement, independent closure or full research validation.

## Project-owned materials

The bilingual teaching notes are this project's contribution.
No project-wide reuse license has yet been selected.
This notice does not relicense third-party content.

## Integrated detector workflow

The dimuon workflow combines the project-owned detector-learning helpers with the SMEFTsim teaching material. Pythia 8.316, Delphes 3.5.1 and Parnassus 0.1.0 are obtained from upstream; their source trees retain their licenses and attribution. The Parnassus exercise uses its parametric CMS response. Original detector source notes are retained in [detector sources](docs/detector-sources.md). The pinned install and local f2py/ROOT adapters are described in [installation](docs/setup/README.md).

# 来源、版本与实现范围

[English](detector-sources.md)

探测器部分已整合进 [完整教程](../README.zh-CN.md)，与 SMEFTsim 的模型导入、事件生成、重加权和 ROOT 分析共用一条学习路线。

| 来源 | 本次使用 | 借鉴或用途 |
|---|---|---|
| [Pythia 8 手册](https://pythia.org/latest-manual/Frontpage.html) 与 [学习练习](https://pythia.org/download/pdf/worksheet8312.pdf) | `pythia8mc==8.316.0`，固定教程版本 | LHE 输入、ISR/FSR/MPI、强子化、衰变和事件记录 |
| [pyhepmc 文档](https://scikit-hep.org/pyhepmc/reference.html) 与 [基本 I/O](https://scikit-hep.org/pyhepmc/examples/basics.html) | 版本见依赖锁文件 | `GenEvent.from_hepevt`、GeV/mm、HepMC3 ASCII |
| [Delphes Quick Tour](https://delphes.github.io/workbook/quick-tour/) 与 [DESY 教程](https://delphes.github.io/tutorials/prefit/) | 3.5.1，commit `28658365abeb71ee36dfc739f9670c1514c0cb10` | HepMC → ROOT、CMS 卡、分支和分析 |
| [Delphes 源码](https://github.com/delphes/delphes/tree/3.5.1) | 只构建 `DelphesHepMC3`、共享库和必要字典 | 实际检查读取器事件计数，不修改源码 |
| [Parnassus](https://github.com/parnassus-hep/parnassus) | commit `c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865` | 统一 API、参数化 CMS 响应、HepMC 输入与 ROOT 输出 |
| [Parnassus 参数化说明](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/docs/parametric-mode.md) | CPU，PyTorch 2.7.1+cpu | 本练习验证的模式 |
| [Parnassus 神经模式](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/docs/neural-mode.md) | 本次未运行 | 了解参数化响应与学习式响应的区别 |
| [MadGraph](https://github.com/mg5amcnlo/mg5amcnlo/tree/v2.9.27) | 2.9.27，commit `eb76cab72b8d44aac7162ac7221ac08a4384a169` | 独立源码目录；使用本项目 Python 3.12 生成 SMEFTsim 双 muon 事件 |
| [MadGraph run 卡定义](https://github.com/mg5amcnlo/mg5amcnlo/blob/eb76cab72b8d44aac7162ac7221ac08a4384a169/madgraph/various/banner.py) | 同一固定版本，MLM 展示块默认隐藏，`ickkw=0`、`xqcut=0` | 解释 matching/merging 默认值；`ptlmax` 的负值约定另核对 `Template/LO/SubProcesses/cuts.f` 与 `setcuts.f` |
| [Parnassus CLI](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/docs/cli-reference.md) 与 [pipelines](https://github.com/parnassus-hep/parnassus/blob/c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865/docs/pipelines.md) | 同一固定版本 | 参数覆盖、batch size、聚类、隔离变量与输出分支 |
| [ROOT wheel](https://pypi.org/project/ROOT/0.1a12/) | ROOT 6.40.00，wheel `0.1a12` 的 CPython 3.12 Linux x86-64 构建 | 安装在本项目 `.venv-unified`；编译 Delphes、读取树并画图 |
| [uv Python 管理](https://docs.astral.sh/uv/guides/install-python/) | uv 0.9.28、Python 3.12.12 | 项目内 Python，不改全局安装 |

## 最小组件的取舍

统一使用本项目 Python 3.12 环境。Pythia 的 Python wheel 已随 Parnassus 安装，所以不再装 C++ Pythia；pyhepmc 提供 HepMC3，所以不再编译独立 HepMC 库。Delphes 使用自带 FastJet/Tcl，只构建必要目标。Parnassus 使用上游运行依赖，没有安装开发 extras、GPU/CUDA 包或另写探测器模型。

接口辅助文件仍是 `scripts/env.sh`、`bin/root-config`、`scripts/hepmc_io.py`。另外用一个 `scripts/plot_dy.py` 集中 ROOT 读取、切选、画图和计数，让正文聚焦包的调用与事件流。它只分析已有输出，不代替生成、shower 或探测器模拟；不增加依赖或另建绘图框架。

`scripts/hepmc_io.py` 是本项目编写的薄适配层，调用上游 API；没有复制 Parnassus 的转换算法。适配显式顶点编码，逐事件核对稳定粒子数及四动量。适配层会把 LHE 中带名称的权重写入 HepMC 事件。`scripts/shower.py` 先将 Pythia 中的额外权重与 LHE 输入核对，再读回写出的 HepMC 文件，检查事件 ID、权重名称和数值；同时写出 `weights.json`。分析时先核对这份记录与 LHE 输入是否一致，再按事件 ID 将 LHE 权重与探测器对象对应起来，不要求每个权重都存为探测器 ROOT 文件中的分支。

双 muon 主线传递四个权重：`nominal`、`sm_check`、`cHl3_plus` 和 `cHl3_minus`。它们共用同一批 shower 后的事件和探测器响应，不会为每个参数点重新运行这些阶段。这些检查验证了当前配置下权重的保留情况，并不代表所有 Pythia 多代衰变拓扑或任意过程都已得到完整验证。原事件记录仍由 LHE/Pythia 提供；研究扩展需另行检查完整历史与权重。

## 许可证与归属

组件署名、许可范围与科学引用集中列在 [第三方声明](../THIRD_PARTY_NOTICES.zh-CN.md)。具体条款以各固定版本源码及依赖内的许可文件为准。

本教学文件夹不分发这些第三方源码、安装环境或原 CMS Tcl 卡；读者从上游获取。下载的软件保留自己的 LICENSE/COPYING。`config/delphes_CMS.tcl` 只在本地从上游卡复制，并增加固定种子。

`config/parnassus.yaml` 是按上游公开配置接口填写的本次设置；图和数值由本地运行生成。模型、生成器、探测器实现和上游方法的贡献属于所列作者及项目，本教程只提供独立的操作说明和接口练习。自有文档与辅助文件尚未选择统一再使用许可证。

本次验证不等于真实 CMS 全模拟、两套 CMS 响应完全等价、神经模型 validation、一般性的 SMEFT 重加权 closure，或集群执行已完成。

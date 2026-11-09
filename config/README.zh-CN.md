# 主线配置

[English](README.md) | [教程](../docs/handbook.zh-CN.md)

| 文件 | 读取它的软件 |
|---|---|
| `dy_process.mg5` | MadGraph：SMEFTsim 双 muon 过程导出 |
| `dy_reweight.dat` | MadGraph：SM 自检与 `cHl3=+1/-1` |
| `higgs_process.mg5` | MadGraph：Higgs 四体衰变导出 |
| `shower.cmnd` | Pythia：LHE 输入、种子和衰变设置 |
| `parnassus.yaml` | Parnassus：参数化 CMS 响应、聚类和隔离 |
| `requirements.lock.txt` | 安装脚本：固定 Python 包版本 |

Delphes 卡在安装时从固定源码复制为 `delphes_CMS.tcl`，加上随机种子。实际数值参数卡和 run 卡位于导出过程的 `work/dy/Cards`，由 `prepare_dy.py` 设置。可编辑副本与原上游材料分别存放。

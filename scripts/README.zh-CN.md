# 辅助脚本

[English](README.md) | [完整教程](../docs/handbook.zh-CN.md)

在项目根目录先执行 `source scripts/env.sh`。这些文件把重复的准备、格式转换和分析写成可读脚本；生成器与探测器的实际调用见教程。

| 文件 | 用途 |
|---|---|
| `setup.sh` / `env.sh` | 安装和加载共用的 Python 3.12 环境 |
| `prepare_materials.py` | 准备上游 UFO、卡和 Higgs 的 Python 3 工作副本 |
| `prepare_dy.py` | 设置 SM 双 muon 基线和重加权卡 |
| `prepare_higgs.py` | 准备 Higgs 原教程的参数与三个类别的重加权 |
| `lhe.py` | 读取 LHE 数值、事件和权重 |
| `shower.py` / `hepmc_io.py` | 调用 Pythia、保存命名权重并核对 HepMC |
| `plot_dy.py` | 按事件编号分析硬散射、稳定粒子和重建对象 |
| `fix_axes.py` | 调整 Higgs 原绘图脚本工作副本的标签与布局 |
| `test_analysis.py` | 检查事件对应、负权重归一化和比值相关误差 |
| `validate.py` | 复核实际运行产物并写出验证记录 |

```bash
python scripts/test_analysis.py
python scripts/validate.py
```

第二条命令在主教程、Higgs 新样本及原示例分析都完成后运行；结果写入 `out/unified-validation/validation.json`。

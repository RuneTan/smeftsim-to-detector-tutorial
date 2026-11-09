# 本项目的重加权示例

[English](README.md) | [简体中文](README.zh-CN.md)

这组数据保留了先前的 `Hvlvl_SM_manual` 运行结果：
`h > e- ve~ mu+ vm`，SMEFTsim v3.0.2 / U35 / MwScheme，MadGraph 2.9.27。

当前操作步骤见 Higgs 练习中的[复现原有的 2,000 事件示例](../../docs/higgs.zh-CN.md#7-复现原有的-2000-事件示例)。

| 文件 | 做什么 |
|---|---|
| `events.lhe.gz` | 分析用 LHE 导出，保留原始初始化数值、事件、SM 权重和 11 个额外权重 |
| `histograms.root` | `lhe_analyzer.py` 生成的 48 个直方图 |
| `plot_mll.pdf`、`plot_mmv.pdf`、`plot_pTl1.pdf`、`plot_pTmu.pdf` | 调用已作本地显示修正的 Python 3 `plot_histos.py` 副本得到的四张 PDF |
| [metadata.json](metadata.json) | 实际事件数、随机种子、版本、参数、运行设置、权重均值和文件哈希 |

实际事件数是 **2,000**，实际种子是 **12363**。它们从原始 run card 读取，
不能根据 Higgs 练习的示例种子推断。

线性、平方、传播子权重分别由 `reweight_card_int.dat`、`reweight_card_squares.dat` 和 `reweight_card_propW.dat` 产生；各参数点一次只打开一个系数并设为 1，
`LambdaSMEFT=1000 GeV`。11 个权重在全部事件中存在且有限。
这些是基本数据检查，不是独立直接生成的 closure 验证，也没有完整统计误差处理。

## 公开 LHE 保留哪些内容

公开文件省略原始 banner、完整软件模板和内嵌卡片文本；数值 `<init>` 块和全部事件记录保持不变，包含每个已存储的权重。权重 ID 保留在简洁的 `<initrwgt>` 块中。输入设置和原始压缩文件的 SHA256 记录在 `metadata.json`。

这份导出用于分析和绘图。生成新权重或复现 run 时，使用本地原始 run 及其完整 banner；本地原始模拟文件没有修改。

## 使用现有 ROOT 重画

已准备好 [本地 Python 3 工作副本](../../docs/setup/README.zh-CN.md) 后，
在 Linux 项目根目录逐条输入、回车并等待：

```bash
mkdir -p outputs/example_reweighted
cd outputs/example_reweighted
python ../../work/Material/pyroot_python3/plot_histos.py ../../examples/reweighted/histograms.root
```

PDF 写到当前输出目录，示例输入保留。

## 从示例 LHE 重新分析

**Linux Bash，项目根目录；逐条回车：**

```bash
mkdir -p outputs/example_reweighted
gzip -dc examples/reweighted/events.lhe.gz > outputs/example_reweighted/events.lhe
python work/Material/pyroot_python3/lhe_analyzer.py outputs/example_reweighted/events.lhe outputs/example_reweighted/histograms.root
```

分析器要求输入 LHE 和输出 ROOT 两个参数；完整一行输入后才按回车。
输出应有 48 个直方图；权重和归一化含义见 [主手册](../../docs/higgs.zh-CN.md)。

来源：[Ilaria Brivio 的 2023 年教程](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23)。
数据在本机生成；输入卡和绘图方法采用上述教程，模型与生成器的署名见 [项目 README](../../README.zh-CN.md#来源与致谢)。

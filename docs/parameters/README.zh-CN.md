# UFO 参数资料

[English](README.md) | [简体中文](README.zh-CN.md)

本目录存放 SMEFTsim v3.0.2 的参数解释和静态参考表。Restriction 与输入卡数值来自 [Ilaria Brivio 的 2023 年 6 月 SMEFTsim 教程](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23) 中的 `restrict_massless_Hvlvl.dat` 和 `param_card_Hvlvl.dat`。

| 文件 | 内容 |
|---|---|
| [model_parameter_reference.md](model_parameter_reference.zh-CN.md) | 按 block 列出参数、模型默认值、restriction 和 `param_card_Hvlvl.dat` 的值 |
| [model_parameters.json](model_parameters.json) | 完整机器可读参数声明与公式 |

它们不是已经求值的 MadGraph 模型，也不代替一次 run 的 banner。
索引里的参数声明来自 MIT 许可的 SMEFTsim；许可见
[SMEFTsim-MIT.txt](../../licenses/SMEFTsim-MIT.txt)，出处和版本保留在资料中。

## 1. UFO 中有哪些参数，哪些需要自己设置

UFO 不只是参数表，它是生成器可以读取的模型描述：

| 文件 | 主要内容 |
|---|---|
| `particles.py` | 粒子名称、质量/宽度引用、自旋、电荷、颜色表示等 |
| `parameters.py` | 外部输入值，以及由它们推得的内部参数公式 |
| `couplings.py`、`vertices.py`、`lorentz.py` | 耦合表达式、哪些粒子连接在一个顶点、顶点的洛伦兹结构 |
| `coupling_orders.py` | `NP`、`NPprop` 等标签的定义与上限 |
| `propagators.py` | 包括 dummy 场在内的自定义传播子 |
| `decays.py` | 模型导出的衰变信息，供支持的宽度计算功能使用 |
| `restrict_*.dat` | 在导入时简化和固定模型的参数取值 |

### External 与 internal 是第一层区分

原始教程 UFO v3.0.2 的 `parameters.py` 共定义 201 项：118 个 `external`，83 个 `internal`。
这是**导入 restriction 之前**的计数，不是本衰变需要调整的参数数量，也不是独立 EFT 算子数量。
完整索引见 [model_parameter_reference.md](model_parameter_reference.zh-CN.md)，
逐项列出名称、默认值、教程 restriction 值与参数卡中的值；长公式和机器可读数据在
[model_parameters.json](model_parameters.json)。

| 类别 | 本 UFO 中的内容 | 怎样使用 |
|---|---|---|
| `SMEFT`、`SMEFTcpv` | 60 个普通分量与 25 个 CP 破坏分量 | Wilson 系数是研究或拟合参数；不是由 SM 唯一预测的数 |
| `SMEFTcutoff` | `LambdaSMEFT` | 与系数一起明确设置和记录；本例为 1,000 GeV |
| `SMINPUTS` | `MW`、`Gf`、`aS` | 固定电弱输入和强耦合；`MZ` 在 `MASS` block 中，同样是电弱输入 |
| `MASS` | 11 个质量输入 | 设置运动学质量；轻粒子的值可被 restriction 固定为零 |
| `YUKAWA` | 9 个质量维数的 Yukawa 输入，如 `ymb`、`ymt` | 经公式转成 Yukawa 耦合；它们自身不是无量纲 Yukawa 值 |
| `CKMBLOCK` | 4 个 CKM 参数 | 本教程 restriction 取消混合并固定相关设定 |
| `DECAY` | `WT`、`WZ`、`WW`、`WH` | top、Z、W、Higgs 的基线总宽度；与本例输出的四轻子部分宽度不同 |
| `SWITCHES` | `linearPropCorrections` | 传播子处理方法的开关；本教程已在 restriction 中固定为 1 |
| `internal` | 电荷、弱混合角、真空期望值、CKM 矩阵元、输入修正、宽度修正等 | 按模型公式计算，通常不独立设置 |

例如，当前 `MwScheme` 的内部参数包含
$\hat v=(\sqrt2 G_F)^{-1/2}$、$g_s=\sqrt{4\pi\alpha_s}$，
以及 $\Delta G_F=(2cHl3-cll1)\hat v^2/\Lambda^2$。
调整输入或 Wilson 系数，相关内部参数随公式改变。
`aEW` 在本 UFO 中是内部量；同名参数在 `alphaScheme` 可成为外部输入。
不能把默认值、内部公式和独立可调输入混为一谈。

### 当前需要你确认哪些值

先保持 `param_card_Hvlvl.dat` 中的 SM 输入与宽度，以便复现参考结果。每次练习主要确认：

1. 模型、flavor、scheme、restriction，以及[过程阶数选项](../processes/README.zh-CN.md#3-阶数选项先筛选振幅再筛选振幅平方)。
2. 研究的 Wilson 系数及其他保留系数的数值；SM 起点把它们设为零。
3. `LambdaSMEFT=1000` 及系数单位。
4. `run_card.dat` 中的事件数、随机种子、切选和束流等运行设置；这些不是 UFO 的模型参数。

本例 restriction 实际保留的普通 EFT 输入是 `cHbox`、`cHW`、`cHl3`、`cHq3`、`cll1`。
`cHq3` 虽是夸克算子，却能通过 W 总宽度修正影响这个轻子过程。
`cHWB` 在这个 restriction 中为零；重加权文件中出现同名的零权重，不表示相关顶点可自由恢复。

**默认值的依据分三类：**

- **实验或参考理论结果**：SM 质量、耦合和宽度来自模型发布时采用的测量或理论参考。
  手册附录的参数表逐项列了来源，多项为 PDG 2020；默认 $m_W=80.387$ GeV 引用当时的 Tevatron 组合，
  Higgs 与 top 宽度采用对应理论参考。它们是这份旧教程的基准，不宣称是今天最新的数值。
- **理论定义或计算**：电荷和群表示由模型规定；内部耦合、输入 shifts 等由拉格朗日量与输入方案推得。
  这些量不会各自独立取一个“经验默认值”。
- **计算假设与学习基准**：Wilson 系数默认零表示 SM 起点，不是实验已证明全部为零；
  $\Lambda=1$ TeV 是参数化基准，不表示已发现新粒子位于 1 TeV。
  轻粒子质量为零是本教程的近似，传播子开关是计算方法选择。

特别是 restriction 中的 `cHbox=0.2`、`cHW=0.3`、`cHl3=0.5`、`cHq3=0.6`、`cll1=0.7`，
用于保留并区分顶点，不是拟合结论。`param_card_Hvlvl.dat` 随后把这五个系数设为零，作为 SM 起点。
先导入 restriction，再使用参数卡，最后以每个 run 的 banner 核对最终设定。
不要直接修改原始 UFO 的 `parameters.py` 来替代参数卡设置。
参数定义与来源见 [实用手册的 Parameter definitions 附录](https://arxiv.org/html/2012.11343v3)。

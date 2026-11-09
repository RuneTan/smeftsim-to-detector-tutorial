# 模型、过程与阶数

[English](README.md) | [简体中文](README.zh-CN.md)

这里解释 [Higgs 进阶练习](../higgs.zh-CN.md)使用的模型、restriction 与阶数语法。
过程命令在 MadGraph 中手动输入；参数卡、run 卡和 reweight 卡从固定版本教程获取到本地工作区。

## 1. 本例为什么选这个模型

flavor 与电弱输入方案的物理含义见背景知识中的[Flavor](../physics/README.zh-CN.md#5-flavor新相互作用怎样区分不同代的费米子) 与 [Scheme](../physics/README.zh-CN.md#6-scheme用哪些测量值确定电弱参数)。
本练习固定使用：

```text
SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl
```

| 名称 | 含义 | 实际选择的影响 |
|---|---|---|
| `U35` | $U(3)^5$ 味对称假设 | 约束不同代之间的系数关系 |
| `MwScheme` | 以 $m_W,m_Z,G_F$ 为电弱输入 | 决定哪些量作为输入、哪些关系含 EFT 修正 |
| `UFO` | 生成器模型格式 | MadGraph 从这里读取参数、顶点等 |
| `massless_Hvlvl` | 本教程配套的过程 restriction | 简化轻粒子质量等设定，保留练习用的 EFT 顶点 |

另一输入方案 `alphaScheme` 使用 $\alpha_{\rm em},m_Z,G_F$。
换输入方案不是单纯改文件名：可观测量、参数关系和 EFT input shifts 的处理必须一致。
对于研究应用，应根据具体物理问题选择 flavor 与电弱输入方案，并记录相应的模型假设。

## 2. Restriction 与参数卡不同

Restriction 在**导入模型**时简化模型。若这时把某个系数限制为零，相关顶点可能被移除，
之后再在输出参数卡里把系数调大也恢复不了这些顶点。

`restrict_massless_Hvlvl.dat` 使用某些非零系数来保留本例需要的顶点。
这些导入时的数值并不是你最终想生成的物理点。
过程导出后，把 `param_card_Hvlvl.dat` 复制到输出的 `Cards/param_card.dat`，
再选择系数。这份参数卡把本例可调的 EFT 系数置零，作为 SM 起点。

教程 UFO 的导入语法来自 Python 2。过程卡已允许 MadGraph 在**工作副本**中转换为 Python 3 语法。
原始 `tutorial` 模型保留；本机工作副本已成功转换、导入并用于新事件生成。

## 3. 阶数选项：先筛选振幅，再筛选振幅平方

下面是 **MadGraph 内部命令的语法示例**。本节先阅读，不在 Bash 执行。
若从项目根目录 `~/smeftsim` 启动 MadGraph，可在 `MG5_aMC>` 中逐行输入并回车；实际生成步骤见[生成事件与全部权重](../higgs.zh-CN.md#4-生成事件与全部权重)：

```text
import model ./work/Material/SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=0
```

`h` 是初态 Higgs，`>` 表示反应方向，`ve~` 是反电子中微子，`vm` 是 muon neutrino。
接着可以 `display diagrams` 查看图；`output 目录名` 导出过程代码。
`output` 成功仍没有生成事件，实际积分和事件生成发生在后续 `launch` 阶段。

### 第一层：一个振幅中允许多少 EFT 插入

`NP` 是模型对耦合项赋予的计数标签。普通维六顶点、维六输入修正携带相应 NP 阶数，
SM 项为 `NP=0`。它与 Wilson 系数的数值不同：`NP=1` 不表示 `cHl3=1`。
它也不表示一圈计算；本例仍是树级矩阵元。

先不考虑传播子修正，把最多含一次普通 EFT 插入的振幅写为

$$
\mathcal M=\mathcal M_0+\mathcal M_6,
\qquad \mathcal M_6=\sum_i\frac{c_i}{\Lambda^2}\mathcal A_i.
$$

$\mathcal M_0$ 是 SM 振幅，$\mathcal M_6$ 已包含 Wilson 系数与 $1/\Lambda^2$。
允许两个 EFT 插入会出现另外的振幅，本教程用上限 1 排除它们。

| 写法 | 在本教程使用的 MadGraph 2.9 树级语法中的含义 |
|---|---|
| `NP=0` | 只允许普通 NP 阶数为零的振幅 |
| `NP=1` 或 `NP<=1` | 上限为 1：允许 SM 振幅以及含一次普通 EFT 插入的振幅 |
| `NP==1` | 要求恰好为 1：选取含一次普通 EFT 插入的振幅；在本例给出其平方贡献 |

尤其要区分单等号与双等号。这里 `=` 表示上限，`==` 表示精确选择。
这些规则针对本教程的生成器版本与树级过程；不要未经检查照搬到另一版本的 NLO 语法。

### 第二层：在振幅平方中保留哪一项

速率来自振幅平方，而不是直接来自振幅：

$$
|\mathcal M_0+\mathcal M_6|^2
=\underbrace{|\mathcal M_0|^2}_{\text{SM：NP 总阶数 0}}
+\underbrace{2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)}_{\text{干涉：NP 总阶数 1}}
+\underbrace{|\mathcal M_6|^2}_{\text{维六平方：NP 总阶数 2}}.
$$

`NP^2` 是 MadGraph 的“振幅平方阶数”语法。它按乘积两侧的 NP 阶数相加计数：
SM × SM 为 $0+0=0$，SM × EFT 为 $0+1=1$，EFT × EFT 为 $1+1=2$。
**这里不是把整数 NP 做数学平方。**

下面五行统一附带 `SMHLOOP=0 NPprop=0`，暂时排除显式传播子修正：

| 阶数选项 | 最后计算的贡献 | 是否含 SM 基线 |
|---|---|---|
| `NP=0` | $\lvert\mathcal M_0\rvert^2$ | 是 |
| `NP=1` | $\lvert\mathcal M_0\rvert^2+2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)+\lvert\mathcal M_6\rvert^2$ | 是 |
| `NP=1 NP^2<=1` | $\lvert\mathcal M_0\rvert^2+2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)$ | 是 |
| `NP=1 NP^2==1` | $2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_6)$，只有干涉修正 | 否 |
| `NP==1`，或 `NP=1 NP^2==2` | $\lvert\mathcal M_6\rvert^2$，只有维六平方贡献 | 否 |

因此，`NP==1` 的“一次插入”说的是振幅：计算速率时，这个振幅仍需与其复共轭相乘。
对单一系数，$|\mathcal M_6|^2=(c/\Lambda^2)^2|\mathcal A|^2$，故它是系数的平方项。
它不含 SM 振幅，也就不含 SM 与 EFT 的干涉。
若同时打开多个系数，这一平方还包含不同维六振幅之间的交叉项。

仅作代数演示：取实数 $\mathcal M_0=2$、$\mathcal M_6=0.3$，
SM 项为 4、干涉项为 1.2、平方项为 0.09。
`NP==1` 给出 0.09；SM 加普通线性修正为 5.2；三项相加为 5.29。
这些数字不是本机物理结果，只帮助区分“某一项”与“合计”。

`SMHLOOP` 是模型中部分 SM loop-generated Higgs 有效耦合的标签。
`SMHLOOP=0` 禁用这些顶点，不是一个通用的“计算所有圈图/禁用所有圈图”开关。
`QCD`、`QED` 是其他耦合计数标签；`QED` 在这里也包括弱耦合和 Yukawa 等结构，
不应只理解为光子顶点数。
`NPcHl3`、`NPcHW` 等更细的标签可以用于筛选某个算子的贡献。

### Dummy vertices：用辅助场实现传播子的一阶修正

传播子描述内部粒子怎样连接两个顶点。质量或宽度受 SMEFT 修正时，传播子也会改变。
对一个传播子 $P(m,\Gamma)$，一阶展开可以示意写为

$$
P(m_0+\delta m,\Gamma_0+\delta\Gamma)
\simeq P_{\rm SM}
+\delta m\left.\frac{\partial P}{\partial m}\right|_0
+\delta\Gamma\left.\frac{\partial P}{\partial\Gamma}\right|_0
\equiv P_{\rm SM}+\Delta P.
$$

$m_0,\Gamma_0$ 是基线质量和宽度；$\delta m,\delta\Gamma$ 是 Wilson 系数产生的修正。
为把 $\Delta P$ 交给生成器，SMEFTsim 引入 `W1`、`Z1`、`H1`、`t1` 等 **dummy 辅助场**，
让它们的自定义传播子代表这段修正。
它们不是新增的物理 W、Z、Higgs 或 top 粒子。

模型复制相应 SM 顶点，把普通场换成 dummy 场；这种顶点叫 **dummy vertex**。
对本例中一条内部 W 线，可示意为：

```text
普通贡献：   左端顶点 —— W  的普通传播子 —— 右端顶点
修正贡献：   左端辅助顶点 —— W1 的 ΔP —— 右端辅助顶点
                NPprop=1                  NPprop=1
```

这一条辅助内部线两端各贡献一个标签，所以该修正振幅的 `NPprop` 总阶数为 2。
一般说，顶点有几条 dummy 腿，就带几阶 `NPprop`；本例是一条内部线连接两个端点。
**标签为 2 不表示两个 EFT 插入，也不表示两条传播子分别被修正。**

把普通 SM 振幅记作 $\mathcal M_0$、这一传播子修正振幅记作 $\mathcal M_P$，
两者的干涉为 $2\mathrm{Re}(\mathcal M_0^{\ast}\mathcal M_P)$，
在 `NPprop^2` 中计数 $0+2=2$。
虽然这个标签是 2，$\mathcal M_P$ 对 Wilson 系数仍是一阶，干涉仍属于 $1/\Lambda^2$ 修正。
辅助场是计算实现的计数约定，不应直接当作 EFT 能标的幂次。

所以本例用

```text
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=2 NPprop^2==2
```

`NP=0` 排除普通 EFT 顶点和输入插入；传播子修正走独立的 `NPprop` 通道。
`NPprop=2` 是振幅层的上限，允许普通 SM 及一条辅助传播子；
`NPprop^2==2` 再只选取它们的干涉，不保留 SM 基线，也不保留 $|\mathcal M_P|^2$。

该功能还要求模型允许 dummy 耦合、`linearPropCorrections` 为非零。
**本教程已经准备好这两项**：`coupling_orders.py` 中 `NPprop.expansion_order=99`，
`restrict_massless_Hvlvl.dat` 把 `linearPropCorrections=1` 固定在导入模型时。
所以参数卡 `param_card_Hvlvl.dat` 不再单独列出这个开关，不需要你补一个 `SWITCHES` block。
其他 SMEFTsim UFO 版本的默认开关可能为 0，不能只复制这一条过程命令就假定已启用。

### 原始教程中的四类贡献

下表沿用原始教程的样本命名，便于区分各类贡献。当前 [Higgs 进阶练习](../higgs.zh-CN.md)从一个 SM 基线样本计算多个重加权点，并不要求分别生成这四个目录。

| 原始样本名 | 阶数选项 | 实际包含 |
|---|---|---|
| `Hvlvl_SM` | `SMHLOOP=0 NP=0 NPprop=0` | SM 基线 |
| `Hvlvl_SMEFT` | `SMHLOOP=0 NP==1 NPprop=0` | 普通维六振幅平方 |
| `Hvlvl_SMEFT_linear` | `SMHLOOP=0 NP=1 NP^2==1 NPprop=0` | 普通 SM–维六干涉 |
| `Hvlvl_SMEFT_prop` | `SMHLOOP=0 NP=0 NPprop=2 NPprop^2==2` | SM–传播子修正干涉 |

这四类贡献彼此不同。在同一参数点构造线性预测时，需要组合 SM、普通干涉和传播子干涉；
若选择额外保留普通维六平方项，则再加入相应贡献。
平方项不自动包含所有 $1/\Lambda^4$ 项，见[线性项与平方项](../physics/README.zh-CN.md#4-为什么要区分线性项和平方项)。
不要随意添加 `Auto` 宽度计算：若同时启用显式传播子修正，可能混入或重复某些效应。
本练习先保持 `param_card_Hvlvl.dat` 中的宽度数值与处理约定。
语法与实现可核对 [SMEFTsim 手册的 Usage in MadGraph 与 Propagator corrections 部分](https://arxiv.org/html/2012.11343v3)
和 [2023 年教程命令](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23#running-mg-and-looking-at-diagrams)。

# 进阶：Higgs 四体衰变与重加权

[English](higgs.md) | [双 muon 主教程](handbook.zh-CN.md) | [原有 2,000 事件示例](../examples/reweighted/README.zh-CN.md)

这个案例研究

$$h\to e^-\bar\nu_e\mu^+\nu_\mu.$$

它适合用来理解 SMEFT 的线性干涉、维六平方项和传播子修正。这里从一个 Higgs 的衰变出发，积分得到**部分衰变宽度**，单位 GeV。主教程从质子碰撞出发，得到的是截面，单位 pb。

## 1. 使用同一个环境

完成统一 [安装](setup/README.zh-CN.md) 后，在 Linux Bash 输入：

```bash
cd ~/smeftsim
source scripts/env.sh
```

安装已从 Ilaria Brivio 的固定版本原教程下载 UFO、卡和分析脚本。`tutorial` 保存来源，`work/Material` 保存可编辑的副本。分析器与绘图器的 Python 3 副本位于 `work/Material/pyroot_python3`。

## 2. 导出衰变过程

```bash
python tools/mg/bin/mg5_aMC
```

在 `MG5_aMC>` 中输入：

```text
set auto_update 0 --no_save
set auto_convert_model True --no_save
import model ./work/Material/SMEFTsim_U35_MwScheme_UFO-massless_Hvlvl
generate h > e- ve~ mu+ vm SMHLOOP=0 NP=0 NPprop=0
output work/higgs
quit
```

`massless_Hvlvl` 是原教程为此衰变准备的 restriction。它保留相关的 EFT 参数，SM 过程用 `NP=0 NPprop=0` 选出基线。重加权时会明确更换要计算的贡献。

相同命令保存在 [config/higgs_process.mg5](../config/higgs_process.mg5)，也可以一次读入：

```bash
python tools/mg/bin/mg5_aMC config/higgs_process.mg5
```

两种导出方式任选一种；已有 `work/higgs` 时继续设置卡。

## 3. 准备原教程的卡

```bash
python scripts/prepare_higgs.py --events 200 --seed 23456
```

脚本把原教程的参数卡与 run 卡复制到 `work/higgs/Cards`，仅设置本次事件数与种子；随后把三张原重加权卡串接起来，保留各自的过程定义和标签。

这里仍使用 `LambdaSMEFT=1000` GeV、零 Wilson 系数的 SM 基线和原教程宽度。衰变案例的生成层 `ptl=0`，让你观察完整的四体末态；双 muon 主线的 10 GeV 碰撞切选不用于这个案例。

可以打开 `work/higgs/Cards/reweight_card.dat` 看看：每条 `change process` 选择一种贡献，`launch --rwgt_name=...` 命名权重，后面的 `set` 指定系数。

| 贡献 | 原教程过程中的阶数选项 | 输出标签 |
|---|---|---|
| 线性干涉 | `NP=1 NP^2==1 NPprop=0` | `cHbox`、`cHW`、`cHl3`、`cll1` |
| 维六平方 | `NP==1 NPprop=0` | 上面四个标签加 `_sq` |
| 传播子干涉 | `NP=0 NPprop=2 NPprop^2==2` | `cHl3_propW`、`cHq3_propW`、`cll1_propW` |

所有过程还使用 `SMHLOOP=0`。阶数的详细解释见 [过程附录](processes/README.zh-CN.md)。

## 4. 生成事件与全部权重

```bash
work/higgs/bin/generate_events higgs_200 -f --nb_core=4
mkdir -p out/higgs/new
gzip -dc work/higgs/Events/higgs_200/unweighted_events.lhe.gz > out/higgs/new/events.lhe
```

第一条命令会生成 SM 衰变样本，再依次计算三个类别、共 11 个附加权重。`higgs_200` 是本次 run 名。重新生成另一批事件时换一个名字，并在后面的读取路径中使用它。

这里没有质子碰撞的产生过程，也没有调用 Pythia 和探测器；图中的中微子动量来自生成器记录。若以后研究碰撞中的 Higgs 信号，需要再选择它的产生过程，并在重建层定义可测量的变量。

## 5. LHE → ROOT → PDF

```bash
python work/Material/pyroot_python3/lhe_analyzer.py out/higgs/new/events.lhe out/higgs/new/histograms.root
cd out/higgs/new
python ../../../work/Material/pyroot_python3/plot_histos.py histograms.root
cd ../../..
```

分析器读取每个事件的四动量和各权重，得到 **48 个直方图**：4 个变量 ×（SM + 11 个附加权重）。绘图器产生 4 张 PDF：

| 文件 | 变量 |
|---|---|
| `plot_mll.pdf` | $m_{e\mu}$ |
| `plot_mmv.pdf` | $m_{\mu\nu_\mu}$ |
| `plot_pTl1.pdf` | 两条带电轻子中较大的 pT |
| `plot_pTmu.pdf` | muon pT |

图的纵轴是每个 bin 的部分宽度贡献 $\Gamma_{\rm bin}$ [GeV]，尚未除以 bin 宽；原绘图器把选中的贡献与 SM 相加，并在下面显示相应比值。现有图例和变量说明见 [图像附录](figures/README.zh-CN.md)。

## 6. 读懂这些权重

Higgs 卡里的 `cHl3` 标签表示**单独的线性干涉贡献**，可以为负；它不是 `cHl3=1` 的完整目标点权重。主教程的 `cHl3_plus` 则是完整目标点，两者要按各自卡片解释。

对同一个事件，若要组合 SM、线性、传播子和平方贡献，先相加：

$$w_i=w_{{\rm SM},i}+w_{{\rm linear},i}+w_{{\rm prop},i}+w_{{\rm square},i}.$$

然后按 bin 求和并除以事件数。要画微分宽度时再除以 bin 宽。组合误差应从逐事件相加后的权重计算，保留这些贡献之间的相关性。原绘图器提供中心值曲线。

## 7. 复现原有的 2,000 事件示例

仓库继续保留之前的示例，可在同一个 Python 3.12 环境中分析：

```bash
mkdir -p out/higgs/reference
gzip -dc examples/reweighted/events.lhe.gz > out/higgs/reference/events.lhe
python work/Material/pyroot_python3/lhe_analyzer.py out/higgs/reference/events.lhe out/higgs/reference/histograms.root
cd out/higgs/reference
python ../../../work/Material/pyroot_python3/plot_histos.py histograms.root
cd ../../..
```

本次整合同时重跑了新的 200 事件案例，并逐 bin 核对了原有 2,000 事件示例的 48 个直方图。详细结果见 [验证记录](validation.zh-CN.md)。

## 8. 检查两个案例的产物

跑完双 muon 教程的 Parnassus 对比和上面的两组 Higgs 分析后，在已经加载环境的项目根目录运行以下命令。

```bash
python scripts/test_analysis.py
python scripts/validate.py
```

第一条运行四项分析测试。第二条检查教程中的事件数、权重和输出文件，比较 48 个 Higgs 参考直方图，并写出 `out/unified-validation/validation.json`。

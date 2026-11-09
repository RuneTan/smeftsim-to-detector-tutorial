# 第三方来源与许可说明

[English](THIRD_PARTY_NOTICES.md) | [简体中文](THIRD_PARTY_NOTICES.zh-CN.md)

核对时间：2026-10-15。此文件记录组件来源与许可信息，不代替具体上游许可证。

## SMEFTsim 模型与参数资料

来源：[SMEFTsim](https://github.com/SMEFTsim/SMEFTsim)，教程模型 v3.0.2。
官方 v3.0.2 标签的 LICENSE 为 MIT，Copyright (c) 2020 SMEFTsim。
完整许可保存在 [licenses/SMEFTsim-MIT.txt](licenses/SMEFTsim-MIT.txt)。

本项目参数索引静态整理模型声明、公式和作者卡的数值；它不是新的物理模型。
理论依据与引用论文见 [根 README](README.zh-CN.md)。
模型源码仍从上游获取，不随本仓库发布。

## 2023 年教程

作者：Ilaria Brivio。
来源：[SMEFTsim_tutorial_June23](https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23)，
提交 `92ffde994d7c0d90554ee629cc477ee171c76b84`。

原过程、卡、restriction、分析器和绘图逻辑均按该教程学习。
固定的教程副本没有找到 LICENSE；SMEFTsim 模型项目的 MIT 许可不自动覆盖这些独立教程脚本。

本地 `tutorial`、`work/Material` 的作者材料和两个 Python 3 兼容脚本被 Git 忽略。
兼容转换包括 tab 展开、Python 2 语法转换、`file()` 到 `open()` 及解释器行更新。
本项目的 `scripts/fix_axes.py` 另行修正本地标签与布局并启用 PDF 字体嵌入，不改变直方图计算；准备方法见 [工作副本说明](docs/setup/README.zh-CN.md)。

## MadGraph 与 ROOT

MadGraph5_aMC@NLO 2.9.27，MadTeam：
固定版本源码根目录的 `LICENSE` 是改写自 Illinois/NCSA 的许可，
原文保存在 [licenses/MadGraph-NCSA.txt](licenses/MadGraph-NCSA.txt)。
vendor 组件可能有其他许可。程序源码与二进制不纳入本项目发布。

ROOT/PyROOT 采用 [LGPL 2.1 或更新版本](https://root.cern/about/license/)，
本项目只在本地环境调用，不分发 ROOT 安装或共享库。

PDF 字体嵌入使用本地 [Ghostscript](https://www.ghostscript.com/licensing/)（AGPL-3.0-or-later），不分发其可执行程序。
公开 PDF 嵌入 [URW Base 35 字体](https://github.com/ArtifexSoftware/urw-base35-fonts) 的子集，其许可为附有明确文档嵌入例外的 AGPL-3.0；版权、例外条款与许可全文保存在 [licenses/URW-fonts.txt](licenses/URW-fonts.txt)。

## 本项目生成的示例

`examples/reweighted` 是用户本地生成并重加权的 2,000 个事件，
不是上游参考包的复制。公开 LHE 保留数值初始化、事件和权重，省略完整生成器 banner 与卡片模板；本地原始文件不变。参数、运行设置、种子、版本、权重与原始及公开文件 SHA256 记录在 `metadata.json`。PDF 和 PNG 通过作者绘图方法生成并明确署名。

因此此说明不把整个示例包装成“所有内容均由本项目原创”。
不宣称原作者背书，也不宣称教学样本完成了独立 closure 或正式研究验证。

## 本项目自身许可

README、中英文操作说明和辅助入口属于本项目整理范围。
当前未选择统一发布许可证；此文件不对第三方内容重新授权。

## 整合后的探测器流程

双 muon 主线整合了本项目 detector-learning 的辅助代码与 SMEFTsim 教学材料。Pythia 8.316、Delphes 3.5.1 和 Parnassus 0.1.0 从上游获取，源码中的许可和署名随安装保留。Parnassus 案例使用参数化 CMS 响应。原探测器接口的来源记录保存在 [探测器来源](docs/detector-sources.zh-CN.md)；固定安装与本地 f2py/ROOT 适配见 [安装说明](docs/setup/README.zh-CN.md)。

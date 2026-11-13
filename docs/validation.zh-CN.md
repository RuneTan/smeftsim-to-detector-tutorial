# 本地运行与验证记录

[English](validation.md) | [主教程](handbook.zh-CN.md) | [机器可读记录](../examples/dimuon/validation.json)

## 2026-11-13 全新安装验证

在全新的 Ubuntu 22.04.5 LTS x86-64 WSL 2 实例中，以普通用户从公开 GitHub 仓库克隆教程。按说明安装系统依赖，在项目内安装 Python 3.12.12 和 ROOT 6.40.00，并从源码编译 Delphes。42 个已安装包通过依赖检查。

- 双 muon。四个阶段各保留 1,000 个事件，`sm_check` 与名义权重完全一致。复现了 627.722 pb 的 SM 截面。Delphes 和 Parnassus 分别选出 704 和 781 个双 muon 事件。最终分析生成 3 张 PNG、3 张 PDF 和 32 个 ROOT 直方图。
- Higgs。生成 200 个新事件，得到 11 个附加权重、48 个 ROOT 直方图和 4 张 PDF。重做 2,000 事件示例分析后，48 个参考直方图的 bin 内容、误差和 entries 全部一致。
- 产物检查。4 项分析测试全部通过，`python scripts/validate.py` 成功写出报告。对已有安装重跑安装脚本，也修复了生成的 Higgs 分析器里的 Python 2 `file (...)` 调用。

## 2026-11-09 本地整合验证

本次在原整合目录中使用相同的 Python 和 ROOT 版本。固定版本见 [安装说明](setup/README.zh-CN.md)。

### 双 muon 主线

- 从 SMEFTsim UFO 导出 `pp > mu+ mu-`，生成 1,000 个 SM 事件。
- `sm_check`、`cHl3_plus`、`cHl3_minus` 三个重加权点全部写入 LHE。
- Pythia 处理 1,000 个事件；四个命名权重（包括 nominal）与 LHE 一致。
- HepMC 写盘后重新读取，核对事件编号、权重名称和数值。
- 转换前后逐个核对稳定粒子的身份与四动量。
- Delphes 和 Parnassus 均输出 1,000 个事件，事件编号与 LHE 对齐。
- Delphes ROOT 中的名义权重与 LHE 一致；完整权重表按编号用于两个后端的分析。
- 输出 3 张 PNG、3 张 PDF、32 个 ROOT 直方图和 JSON 计数。
- `sm_check` 相对名义权重的最大差异为 0。

SM 截面为 627.722 ± 3.436 pb。Delphes 和 Parnassus 分别有 704、781 个事件通过双 muon 选择。图与完整数值见 [示例](../examples/dimuon/README.zh-CN.md)。

### Higgs 进阶案例

- 同一环境中重新导出 Higgs 四体衰变，生成 200 个事件。
- 原教程三个类别的重加权全部完成：11 个附加标签。
- 新样本生成 48 个 ROOT 直方图和 4 张 PDF。
- 重新分析原有 2,000 事件示例：48 个直方图的所有 bin 内容、误差和 entries 与原参考文件完全一致。

### 环境与分析检查

- Delphes 用统一环境的 ROOT 重新编译，运行时不引用旧 detector-learning 项目。
- `pip check` 检查 42 个已安装包，通过。
- 安装脚本在本机现有整合目录中重放通过。
- 4 项数值测试通过：按编号重排、缺失/重复编号识别、带负权重的归一化与同事件比值相关误差；同时覆盖 LHE v3 头部元数据和缺失权重。

本记录对应固定宽度、固定 shower/探测器响应的 LO 教学流程；Parnassus 使用参数化 CMS 响应。新的图和计数来自实际运行，安装重放的范围是本机整合目录。

要检查你自己的运行产物，请按 [验证步骤](higgs.zh-CN.md#8-检查两个案例的产物) 操作。报告写入 `out/unified-validation/validation.json`。

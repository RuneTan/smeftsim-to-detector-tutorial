# 安装与启动

[English](README.md) | [项目首页](../../README.zh-CN.md) | [开始教程](../handbook.zh-CN.md)

主线和 Higgs 案例统一使用 **Ubuntu 22.04 x86-64、Python 3.12.12 和 ROOT 6.40.00**。Parnassus 使用 CPU，普通开发电脑即可完成本教程的小样本。

## 1. 准备 Linux

已经使用 Ubuntu 的读者直接进入下一节。Windows 读者在管理员 PowerShell 中运行：

```powershell
wsl --install -d Ubuntu-22.04
```

按提示完成安装和重启，打开 Ubuntu，设置 Linux 用户名与密码。后面的命令都输入这个 Ubuntu 终端。已有合适的 WSL Ubuntu 时直接使用它。

## 2. 安装编译和图形工具

在 **Linux Bash** 中执行：

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends build-essential gfortran git curl ca-certificates python3 python3-venv perl gzip unzip nano ghostscript libx11-6 libxext6 libxrender1 libxft2 libglu1-mesa
```

编译器用于 MadGraph 和 Delphes，Ghostscript 用于 Higgs PDF 字体，图形库用于 ROOT 输出。Python 科学包随后全部安装到项目内。

## 3. 获取项目并安装软件

接下来的安装步骤用你的普通 Linux 账号执行。首次使用时把教程克隆到 Linux 主目录。这样在 WSL 中，项目会放在 Ubuntu 的文件系统上。

```bash
cd ~
git clone https://github.com/RuneTan/smeftsim-to-detector-tutorial.git smeftsim
```

已有本地整合项目时，直接进入下面的安装步骤。

```bash
cd ~/smeftsim
bash scripts/setup.sh
```

安装脚本逐项完成：获取 uv 和 Python，创建 `.venv-unified`，安装固定依赖，获取固定提交的上游软件，编译 Delphes，准备 UFO、卡和 Higgs 的 Python 3 脚本。

| 软件 | 使用版本 |
|---|---|
| Python | 3.12.12 |
| MadGraph | 2.9.27，`eb76cab72b8d44aac7162ac7221ac08a4384a169` |
| SMEFTsim UFO | 3.0.2，来自 June 2023 教程固定提交 |
| ROOT | 6.40.00，Python 包 `0.1a12` |
| NumPy | 2.5.4 |
| Pythia | `pythia8mc 8.316.0` |
| pyhepmc | 2.16.1 |
| Delphes | 3.5.1，`28658365abeb71ee36dfc739f9670c1514c0cb10` |
| Parnassus | 0.1.0，`c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865` |
| PyTorch | 2.7.1+cpu |
| Meson / Ninja | 1.12.1 / 1.13.2 |

完整 Python 依赖见 [config/requirements.lock.txt](../../config/requirements.lock.txt)。`bin/f2py` 把 MadGraph 的 Fortran 搜索路径传给 Python 3.12 使用的 Meson 编译接口；`bin/root-config` 对接 ROOT wheel 的编译路径。二者由环境入口自动使用。

看到 `Ready. Run: source scripts/env.sh` 后再继续。如果下载中断，回到项目目录重新运行 `bash scripts/setup.sh`。以后打开终端时，按下一节加载环境即可。

如果旧版安装的 Higgs 分析器报 `NameError: name 'file' is not defined`，更新教程仓库后重新运行 `bash scripts/setup.sh`，即可修复生成的分析器。

## 4. 每次进入项目

```bash
cd ~/smeftsim
source scripts/env.sh
python --version
python -c "import ROOT; print(ROOT.gROOT.GetVersion())"
```

应看到 Python 3.12.12 和 ROOT 6.40.00。`source scripts/env.sh` 同时设置 Python、编译适配器和共享库路径。

进一步检查：

```bash
tools/uv/bin/uv pip check --python .venv-unified/bin/python
python -c "import pythia8mc, pyhepmc, parnassus, torch; print(torch.__version__)"
ldd tools/delphes/DelphesHepMC3
```

依赖检查应通过，PyTorch 显示 `2.7.1+cpu`，Delphes 的 ROOT 库路径应来自这个项目。然后进入 [双 muon 教程](../handbook.zh-CN.md)。

## 5. 目录怎样分工

| 目录 | 用途 |
|---|---|
| `.venv-unified` | 两个案例共用的 Python 包环境 |
| `tools/python` | 项目内的 Python 解释器 |
| `tools/mg`、`tools/delphes`、`tools/parnassus` | 上游源码和编译程序 |
| `tutorial` | 固定提交的 Higgs 原教程 |
| `work` | 模型工作副本、MadGraph 导出的过程和 run |
| `out` | 本次练习的事件、分析和图像 |
| `examples` | 随教程提供的小型参考结果 |

从旧项目继续使用时，原 `.venv` 和旧运行结果留在原处；新教程统一从 `scripts/env.sh` 进入 `.venv-unified`。换电脑时用安装脚本重建环境，复制文档、配置和需要保留的数据即可。

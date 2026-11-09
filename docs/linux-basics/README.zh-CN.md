# 如果你不熟悉 Linux 系统

[English](README.md) | [简体中文](README.zh-CN.md)

本篇是可选的 Linux 与终端操作入门，介绍基本命令，以及本项目使用的路径、Python 提示符和 MadGraph 菜单。遇到不熟悉的输入步骤时，再查对应小节即可。

示例使用自己 Linux 主目录下的项目目录 `~/smeftsim`，适用于原生 Linux、虚拟机和 WSL；用户名无需与作者相同。

继续 SMEFTsim 练习请返回 [主手册](../handbook.zh-CN.md)；新电脑的安装配置见 [首次配置说明](../setup/README.zh-CN.md)。

## 目录

1. [Linux 基本命令](#1-linux-基本命令)
2. [看提示符，判断自己在哪里](#2-看提示符判断自己在哪里)
3. [Python 交互输入与“修改文件”要分开](#3-python-交互输入与修改文件要分开)
4. [SMEFTsim 练习中的命令](#4-smeftsim-练习中的命令)
5. [路径怎样读](#5-路径怎样读)

## 1. Linux 基本命令

以下命令在 **Linux Bash** 中使用。文件名和目录名都是示例，执行时替换为你需要操作的路径。
这张表用于查阅，不是要从上到下全部执行的步骤。

| 命令 | 用途 | 怎样理解 |
|---|---|---|
| `pwd` | 查看当前目录 | 打印当前目录的绝对路径 |
| `ls` | 列出当前目录内容 | 显示文件和目录，默认不显示隐藏项 |
| `ls -lh` | 查看详细列表 | `-l` 显示详细信息；`-h` 把大小写成 `4.0K` 等易读形式 |
| `ls -a` | 同时显示隐藏项 | 可查看以点开头的 `.venv-unified` 等目录 |
| `cd ~/smeftsim` | 进入项目目录 | `~` 表示当前 Linux 用户的主目录 |
| `cd ..` | 返回上一级目录 | `..` 表示当前目录的父目录 |
| `mkdir -p demo` | 创建目录 | `-p` 同时创建缺少的父目录；目标已存在时也可继续 |
| `touch notes.txt` | 文件不存在时创建空文件 | 文件已存在时只更新时间戳，不清空内容 |
| `cp notes.txt notes_copy.txt` | 复制文件 | 第一个参数是来源，第二个是目标；同名目标可能被覆盖 |
| `mv notes_copy.txt notes_backup.txt` | 重命名或移动文件 | 目标是目录时移入该目录；同名目标文件可能被覆盖 |
| `rm -i notes_backup.txt` | 确认后删除文件 | `-i` 会询问；输入 `y` 删除，输入 `n` 保留 |
| `cat notes.txt` | 打印文本文件内容 | 适合较短的卡片或笔记 |
| `head -n 5 notes.txt` | 查看前五行 | `-n 5` 指定显示的行数 |
| `tail -n 5 notes.txt` | 查看最后五行 | 常用来查看日志末尾 |
| `less notes.txt` | 分页阅读文本 | 方向键或空格翻阅，按 `q` 退出 |
| `ls --help` | 查看命令帮助 | 解释 `ls` 的可用选项 |

**在 Linux Bash 中做一个小练习。** 每次输入完整一条命令，回车并等待结束。
练习会在 `outputs/linux_practice` 下写入两个文本文件；重复执行会替换它们的内容。

```bash
cd ~/smeftsim
mkdir -p outputs/linux_practice
cd outputs/linux_practice
printf 'Hello Linux\n' > notes.txt
cat notes.txt
cp notes.txt notes_copy.txt
mv notes_copy.txt notes_backup.txt
ls -lh
cd ../..
```

`printf` 产生文本，`\n` 表示换行，`>` 把文本写入 `notes.txt`。
你应看到 `Hello Linux`，以及包含 `notes.txt` 和 `notes_backup.txt` 的文件列表。
最后一条命令返回项目根目录。

## 2. 看提示符，判断自己在哪里

Bash 和 PowerShell 命令都先输入**完整一条**，按 Enter 一次，等提示符返回再继续。
屏幕自动折行不等于新命令；参数、`>` 和输出路径都应在回车前输入完整。
一个代码块里的命令按顺序逐条执行。

| 终端显示的提示符 | 当前在哪里 | 应输入什么 |
|---|---|---|
| `PS C:\...>` | Windows PowerShell | `powershell` 代码块中的命令 |
| `your-user@host:~/smeftsim$` 或类似形式 | Linux Bash | `bash` 代码块中的命令 |
| `>>>` | Python 交互解释器 | 标为“Python 交互输入”的代码 |
| `...` | Python 等待未完成的语句或缩进块 | 继续当前语句；循环末尾需一个空白行 |
| `MG5_aMC>`、`MadEvent>` 或工具选择菜单 | MadGraph/MadEvent | 当前菜单要求的答案或 MadGraph 内部命令 |

这些是**终端显示的提示符**，不要把它们抄进命令。
进入 Linux 后不能直接输入 Windows 的 `C:\...` 路径；
进入 Python 的 `>>>` 后不能直接输入 Bash 的 `cd`、`ls`。

Linux 若只显示单独的 `>` 等待继续，通常是输入里有未闭合的引号或未完成语句。
按 `Ctrl+C` 取消这次未完成输入，再复制完整命令。
而命令**中间**的 `>` 是输出重定向符，是命令的一部分，必须保留。

输入 `python` 再回车，会从 Bash 切到 Python 的 `>>>`；
在 Python 输入 `exit()` 再回车，才返回 Bash。
Bash 中输入 `exit` 再回车，会退出 Ubuntu 终端；这与 `exit()` 不同。
本教程用 `source scripts/env.sh` 设置环境变量，没有调用虚拟环境的 `activate` 脚本，也没有定义 `deactivate`。要恢复到未加载教程配置的环境，关闭当前教程终端，再打开一个新终端即可。

## 3. Python 交互输入与“修改文件”要分开

- **Python 普通语句：** 在 `>>>` 输入完整一行，按回车一次；执行后应再次看到 `>>>`。
- **Python 循环：** 按行输入并回车，保留缩进。最后一行回车后还会显示 `...`；
  此时**什么都不输入，再按一次回车**，整个循环才执行。
- **修改文件：** 标为“文件内容”的代码，应放到编辑器中的指定文件里。
  回车在编辑器里只是换行，编辑完成后按 `Ctrl+S` 保存；不要放进终端执行。
- **名称、日志、示意：** `text` 表格、文件列表和图示通常只用于阅读，
  不是输入步骤；只有明确注明 MadGraph 内部命令的示例，才属于那个工具的命令。

遇到报错就停在当前步骤，核对环境、目录、完整参数和报错内容；
不要把后面的绘图命令继续输入到一个尚未完成的循环或菜单里。

## 4. SMEFTsim 练习中的命令

这些命令基于第 1 节的基本操作，用于激活环境、生成事件和分析结果。

| 写法 | 它做什么 | 回车后通常会看到什么 |
|---|---|---|
| `source scripts/env.sh` | 让当前终端使用项目的 Python 和依赖 | 通常没有输出，提示符也不变；用 `which python` 核对 |
| `which python` | 查看当前调用的是哪个 Python | 应为 `$HOME/smeftsim/.venv-unified/bin/python` 对应的绝对路径 |
| `head -n 1 文件` | 看文件第一行 | LHE 应以 `<LesHouchesEvents ...>` 开始 |
| `gzip -dc 压缩文件 > 新文件` | 解压并写入新文件；原压缩文件保留 | 成功通常没有输出，用 `ls` 检查 |
| `python 脚本.py 参数...` | 用当前环境执行指定脚本 | 脚本日志、结果或报错 |
| `./过程/bin/generate_events run名` | 运行当前目录下的生成器程序 | 工具菜单，然后是积分和生成日志 |
| `zcat 文件.gz \| sed ...` | 解压到数据流，再筛选要看的部分 | 本教程用它查看权重声明；`\|` 必须保留 |

`gzip` 的 `-d` 表示解压，`-c` 表示先把内容送到标准输出；
`>` 再把这份输出写到指定文件。`>` 会覆盖已有的同名输出文件，
因此每次练习用独立目录。
`python` 后的脚本名不计入脚本要求的参数数量：
`lhe_analyzer.py` 要“输入 LHE + 输出 ROOT”两个参数，
`plot_histos.py` 要“输入 ROOT”一个参数。

## 5. 路径怎样读

Linux 主工作目录是 `~/smeftsim`。
Bash 会将 `~` 和 `$HOME` 展开为当前 Linux 用户的主目录；用 `echo "$HOME"` 可以查看它的绝对路径。
例如，用户 `alex` 的目录可能是 `/home/alex/smeftsim`。请使用自己的主目录，无需照抄示例用户名。
`out/higgs/new/events.lhe` 是相对路径，必须从项目根目录解释；
`../../work/...` 是先回到上两级目录，再找脚本。
在 WSL 中，`/mnt/c/...` 用于访问 Windows C 盘，它不是 Linux 项目目录。

Linux 区分大小写：`Material` 与 `material` 不是同一个目录。
带单引号或双引号的路径要连引号一起复制。
如果某步要求先 `cd` 到一个目录，请先执行它并回车，不要只复制后面的脚本命令。

继续 SMEFTsim 练习请返回 [主手册](../handbook.zh-CN.md)；新电脑的安装配置见 [首次配置说明](../setup/README.zh-CN.md)。

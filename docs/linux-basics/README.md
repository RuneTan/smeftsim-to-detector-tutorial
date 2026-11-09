# If you are new to Linux

[English](README.md) | [简体中文](README.zh-CN.md)

This optional guide introduces basic Linux commands and the terminal conventions used in this project: paths, Python prompts and MadGraph menus. Read the sections you need when an input step is unfamiliar.

The examples use `~/smeftsim`, a project directory inside your own Linux home directory. They apply to native Linux, virtual machines and WSL; your username can differ.

Return to the [main handbook](../higgs.md) for the SMEFTsim exercises. For installation on a new machine, use the [setup guide](../setup/README.md).

## Contents

1. [Basic Linux commands](#1-basic-linux-commands)
2. [Use the prompt to identify your current environment](#2-use-the-prompt-to-identify-your-current-environment)
3. [Distinguish interactive Python from editing a file](#3-distinguish-interactive-python-from-editing-a-file)
4. [Commands for the SMEFTsim workflow](#4-commands-for-the-smeftsim-workflow)
5. [How to read paths](#5-how-to-read-paths)

## 1. Basic Linux commands

Use these commands in **Linux Bash**. The file and directory names are examples;
replace them with the paths you want to use. The table is a reference, not a sequence to run from top to bottom.

| Command | Purpose | How to read it |
|---|---|---|
| `pwd` | Show the current directory | Prints its absolute path |
| `ls` | List the current directory | Shows files and directories, excluding hidden names |
| `ls -lh` | Show a detailed listing | `-l` adds details; `-h` makes sizes readable, such as `4.0K` |
| `ls -a` | Include hidden names | Useful for seeing `.venv`, which starts with a dot |
| `cd ~/smeftsim` | Enter the project directory | `~` refers to your Linux home directory |
| `cd ..` | Go to the parent directory | `..` means one level up |
| `mkdir -p demo` | Create a directory | `-p` also creates missing parents and accepts an existing directory |
| `touch notes.txt` | Create an empty file if absent | If the file exists, updates its timestamps without clearing its contents |
| `cp notes.txt notes_copy.txt` | Copy a file | First argument: source; second: destination; an existing destination may be overwritten |
| `mv notes_copy.txt notes_backup.txt` | Rename or move a file | A directory destination moves it there; an existing destination file may be overwritten |
| `rm -i notes_backup.txt` | Delete a file after confirmation | `-i` asks before deletion; answer `y` to delete or `n` to keep it |
| `cat notes.txt` | Print a text file | Best for short cards or notes |
| `head -n 5 notes.txt` | Show the first five lines | `-n 5` specifies the line count |
| `tail -n 5 notes.txt` | Show the last five lines | Useful for the end of a log |
| `less notes.txt` | Browse a text file page by page | Use the arrow keys or Space to scroll; press `q` to quit |
| `ls --help` | Read command help | Explains the available options for `ls` |

**Try a short exercise in Linux Bash.** Enter one complete command at a time and wait for it to finish.
The exercise writes two text files under `outputs/linux_practice`; repeating it replaces their contents.

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

`printf` produces the text, `\n` ends the line, and `>` writes it to `notes.txt`.
You should see `Hello Linux` and a listing containing `notes.txt` and `notes_backup.txt`.
The last command returns to the project root.

## 2. Use the prompt to identify your current environment

For Bash and PowerShell commands, finish the **whole command**, press Enter once, and wait for the prompt to return.
A line wrapping on screen does not start a new command. Keep all arguments and any `>` output path before pressing Enter.
Run a block's commands one at a time, in order.

| Prompt shown by the terminal | Current environment | What to enter |
|---|---|---|
| `PS C:\...>` | Windows PowerShell | Commands in `powershell` blocks |
| `your-user@host:~/smeftsim$`, or similar | Linux Bash | Commands in `bash` blocks |
| `>>>` | Interactive Python interpreter | Code marked "interactive Python" |
| `...` | Python is waiting for an unfinished statement or indented block | Continue the statement; finish a loop with one blank line |
| `MG5_aMC>`, `MadEvent>`, or a tool-selection menu | MadGraph/MadEvent | The answer requested by the current menu, or a MadGraph command |

These are **prompts displayed by the terminal**; do not include them when typing a command.
Once you enter Linux, a Windows path such as `C:\...` cannot be used directly.
At Python's `>>>` prompt, do not enter Bash commands such as `cd` or `ls`.

If Linux displays a lone `>` and waits, your input usually contains an unclosed quote or unfinished statement.
Press `Ctrl+C` to cancel the unfinished input, then copy the complete command again.
A `>` **inside a command**, however, redirects output. It is part of the command and must stay.

Typing `python` and pressing Enter switches from Bash to Python's `>>>` prompt.
In Python, type `exit()` and press Enter to return to Bash.
In Bash, type `exit` and press Enter to leave the Ubuntu terminal; this differs from `exit()`.
`deactivate` only leaves the virtual environment, keeping the Linux terminal open.

## 3. Distinguish interactive Python from editing a file

- **Ordinary Python statements:** at `>>>`, enter one complete line and press Enter once; `>>>` should return when it finishes.
- **Python loops:** enter each line and press Enter, preserving indentation. After the last line, Python still displays `...`.
  **Type nothing and press Enter once more** to run the loop. [Handbook Section 8.6](../higgs.md#5-lhe--root--pdf) gives line-by-line instructions.
- **Editing files:** code marked "file contents" belongs in the named file, opened in an editor.
  In the editor, Enter only inserts a new line. Press `Ctrl+S` to save your changes; do not execute these contents in the terminal.
- **Names, logs, and illustrations:** `text` blocks, file listings, and diagrams are usually for reading,
  not typing. Examples explicitly identified as MadGraph commands belong inside that tool.

If an error occurs, stop at the current step and check the environment, directory, complete arguments, and error message.
Do not paste later plotting commands into an unfinished loop or menu.

## 4. Commands for the SMEFTsim workflow

These commands build on the basics in Section 1 and are used for environment activation, event generation and analysis.

| Command | What it does | What you normally see after pressing Enter |
|---|---|---|
| `source scripts/env.sh` | Makes this terminal use the project's Python and dependencies | Often `(.venv)` in the prompt; check with `which python` |
| `which python` | Shows which Python interpreter is selected | The absolute path corresponding to `$HOME/smeftsim/.venv/bin/python` |
| `head -n 1 file` | Shows the first line | An LHE file should start with `<LesHouchesEvents ...>` |
| `gzip -dc compressed_file > new_file` | Decompresses into a new file, keeping the compressed original | Usually no output on success; check with `ls` |
| `python script.py arguments...` | Runs a script with the current interpreter | Script logs, results, or an error |
| `./process/bin/generate_events run_name` | Starts the generator under the current directory | A tool menu, followed by integration and generation logs |
| `zcat file.gz \| sed ...` | Decompresses into a stream, then selects part of it | Here, the weight declarations; keep the pipe character `\|` |

For `gzip`, `-d` means decompress and `-c` sends the contents to standard output.
`>` then writes that output to the named file. It overwrites an existing file with the same name,
so use a separate output directory for each exercise.
The script filename after `python` does not count as a script argument:
`lhe_analyzer.py` needs two arguments, "input LHE + output ROOT";
`plot_histos.py` needs one, "input ROOT."

## 5. How to read paths

The main Linux working directory is `~/smeftsim`.
Bash expands `~` and `$HOME` to your current Linux user's home directory; `echo "$HOME"` shows its absolute path.
For example, user `alex` may have `/home/alex/smeftsim`. Use your own home directory rather than copying an example username.
`outputs/my_pyroot_reference/events.lhe` is a relative path, interpreted from the project root.
`../../work/...` means go up two directory levels before locating the script.
In WSL, `/mnt/c/...` accesses the Windows C drive; it is not the Linux project directory.

Linux filenames are case-sensitive: `Material` and `material` are different directories.
Copy quotes together with paths that are enclosed in single or double quotes.
If a step first asks you to `cd` into a directory, execute that command and press Enter before copying the script command.

Return to the [main handbook](../higgs.md) for the SMEFTsim exercises. For installation on a new machine, use the [setup guide](../setup/README.md).

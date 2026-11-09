# Bash startup used by the local Windows launchers.
[[ -f /etc/bash.bashrc ]] && source /etc/bash.bashrc
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/env.sh"
cd "$TUTORIAL_HOME"
PS1='(SMEFT tutorial) \u@\h:\w\$ '
printf '\nSMEFTsim tutorial — Python 3.12 environment ready.\n'
printf '中文教程: docs/handbook.zh-CN.md\nEnglish: docs/handbook.md\n\n'

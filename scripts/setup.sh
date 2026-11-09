#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
source scripts/env.sh
mkdir -p tools/uv/bin tools/bin work config out
if [[ ! -x tools/uv/bin/uv ]]; then
    curl -fL https://github.com/astral-sh/uv/releases/download/0.9.28/uv-x86_64-unknown-linux-gnu.tar.gz -o tools/uv.tar.gz
    tar -xzf tools/uv.tar.gz --strip-components=1 -C tools/uv/bin uv-x86_64-unknown-linux-gnu/uv
fi
tools/uv/bin/uv python install 3.12.12
if [[ ! -x .venv-unified/bin/python ]]; then
    tools/uv/bin/uv venv --python 3.12.12 .venv-unified
fi
tools/uv/bin/uv pip install --python .venv-unified/bin/python torch==2.7.1+cpu --index-url https://download.pytorch.org/whl/cpu
tools/uv/bin/uv pip install --python .venv-unified/bin/python -r config/requirements.lock.txt
mkdir -p tools/system-libs/debs
(
    cd tools/system-libs/debs
    apt-get download libsm6 libice6
    for archive in *.deb; do dpkg-deb -x "$archive" ..; done
)

get_source() {
    local url="$1" destination="$2" commit="$3"
    if [[ ! -d "$destination/.git" ]]; then
        git clone "$url" "$destination"
        git -C "$destination" checkout "$commit"
    fi
    [[ "$(git -C "$destination" rev-parse HEAD)" == "$commit" ]] || {
        printf 'Use the pinned commit %s in %s.\n' "$commit" "$destination" >&2
        return 1
    }
}
get_source https://github.com/mg5amcnlo/mg5amcnlo.git tools/mg eb76cab72b8d44aac7162ac7221ac08a4384a169
get_source https://github.com/IlariaBrivio/SMEFTsim_tutorial_June23.git tutorial 92ffde994d7c0d90554ee629cc477ee171c76b84
get_source https://github.com/delphes/delphes.git tools/delphes 28658365abeb71ee36dfc739f9670c1514c0cb10
get_source https://github.com/parnassus-hep/parnassus.git tools/parnassus c9f8bd9e4c86879d35b5cc38860cdf8a0de9d865
tools/uv/bin/uv pip install --python .venv-unified/bin/python --no-deps ./tools/parnassus
chmod +x bin/root-config bin/f2py
make -C tools/delphes -j4 libDelphes.so DelphesHepMC3
python scripts/prepare_materials.py
tools/uv/bin/uv pip check --python .venv-unified/bin/python
python -c "import sys,ROOT,pythia8mc,parnassus; print(sys.version); print('ROOT',ROOT.gROOT.GetVersion())"
printf '\nReady. Run: source scripts/env.sh\n'

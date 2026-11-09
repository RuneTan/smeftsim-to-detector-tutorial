#!/usr/bin/env python3
"""Prepare local UFO/card copies and Python 3 versions of the author scripts."""
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    source = root/'tutorial/Material'
    target = root/'work/Material'
    target.mkdir(parents=True, exist_ok=True)
    model = 'SMEFTsim_U35_MwScheme_UFO'
    if not (target/model).exists(): shutil.copytree(source/model, target/model)
    for f in source.glob('*.dat'):
        if not (target/f.name).exists(): shutil.copy2(f, target/f.name)
    scripts = target/'pyroot_python3'
    scripts.mkdir(exist_ok=True)
    for name in ['lhe_analyzer.py', 'plot_histos.py']:
        f = scripts/name
        if not f.exists():
            f.write_text((source/name).read_text().expandtabs(8))
            subprocess.run([sys.executable,'-m','lib2to3','-w','-n',str(f)], check=True)
            s = f.read_text().replace('file(', 'open(')
            f.write_text(s.replace('#!/usr/bin/env python\n', '#!/usr/bin/env python3\n',1))
    subprocess.run([sys.executable,str(root/'scripts/fix_axes.py')],check=True)
    card = root/'config/delphes_CMS.tcl'
    if not card.exists():
        card.write_text('set RandomSeed 31415\n'+(root/'tools/delphes/cards/delphes_card_CMS.tcl').read_text())
    print('UFO, cards, Higgs analysis scripts and the seeded Delphes card are ready.')


if __name__ == '__main__': main()

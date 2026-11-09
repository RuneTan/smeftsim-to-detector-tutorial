#!/usr/bin/env python3
"""Set the numerical cards for a zero-Wilson-coefficient DY baseline."""
import argparse
import re
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--process', type=Path, default=Path('work/dy'))
    parser.add_argument('--events', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=12345)
    args = parser.parse_args()
    if args.events < 1 or not 0 < args.seed < 30081:
        parser.error('Use a positive event count and a seed between 1 and 30080.')
    cards = args.process / 'Cards'
    param = cards / 'param_card.dat'
    lines = param.read_text().splitlines()
    block = ''
    nzero = 0
    for i, line in enumerate(lines):
        match = re.match(r'\s*block\s+(\S+)', line, re.I)
        if match:
            block = match[1].lower()
        elif line.lstrip().lower().startswith('decay '):
            block = ''
        elif block in ('smeft', 'smeftcpv') and re.match(r'\s*\d+\s+', line):
            lines[i] = re.sub(r'^(\s*\d+\s+)\S+', r'\g<1>0.000000e+00', line)
            nzero += 1
    if not nzero:
        raise RuntimeError('No SMEFT parameters found. Export the SMEFTsim process first.')
    param.write_text('\n'.join(lines) + '\n')
    settings = {'nevents': args.events, 'iseed': args.seed, 'ebeam1': 6500,
                'ebeam2': 6500, 'lpp1': 1, 'lpp2': 1, 'ptl': 10,
                'ptlmax': -1, 'etal': 2.5, 'mmll': 60, 'mmllmax': 120,
                'pdlabel': "'nn23lo1'", 'lhaid': 247000, 'use_syst': 'False'}
    run = cards / 'run_card.dat'
    source = run.read_text()
    for key, value in settings.items():
        pattern = rf'(?m)^\s*[^!\n=]+\s*=\s*{key}\b'
        source, count = re.subn(pattern, f' {value} = {key}', source)
        if count != 1:
            raise RuntimeError(f'Expected one {key} setting, found {count}.')
    run.write_text(source)
    shutil.copy2(Path(__file__).resolve().parents[1] / 'config/dy_reweight.dat',
                 cards / 'reweight_card.dat')
    print(f'{nzero} Wilson coefficients set to zero; {args.events} events; seed {args.seed}.')
    print('Cards ready. Generate the SM sample, then run the reweight card.')


if __name__ == '__main__':
    main()

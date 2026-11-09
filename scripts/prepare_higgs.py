#!/usr/bin/env python3
"""Prepare a fresh Higgs exercise from the locally downloaded author cards."""
import argparse
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--process', type=Path, default=Path('work/higgs'))
    parser.add_argument('--events', type=int, default=200)
    parser.add_argument('--seed', type=int, default=23456)
    args = parser.parse_args()
    if args.events < 1 or not 0 < args.seed < 30081:
        parser.error('Use positive events and a seed between 1 and 30080.')
    root = Path(__file__).resolve().parents[1]
    material = root / 'tutorial/Material'
    cards = args.process / 'Cards'
    (cards/'param_card.dat').write_text((material/'param_card_Hvlvl.dat').read_text())
    run = (material/'run_card_Hvlvl.dat').read_text()
    for key, value in {'nevents':args.events, 'iseed':args.seed}.items():
        run, count = re.subn(rf'(?m)^\s*[^!\n=]+\s*=\s*{key}\b', f' {value} = {key}', run)
        if count != 1: raise ValueError(f'Could not set {key} in the author card.')
    (cards/'run_card.dat').write_text(run)
    reweight = 'change mode LO\nchange helicity False\n'
    for name in ['reweight_card_int.dat','reweight_card_squares.dat','reweight_card_propW.dat']:
        reweight += '\n' + (material/name).read_text()
    (cards/'reweight_card.dat').write_text(reweight)
    print(f'Higgs cards ready: {args.events} events and all 11 author weight definitions.')


if __name__ == '__main__': main()

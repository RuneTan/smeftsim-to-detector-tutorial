#!/usr/bin/env python3
"""Shower a complete LHE sample, preserving named weights and event IDs."""
import argparse
import json
from pathlib import Path

import numpy as np
import pyhepmc
import pythia8mc

from hepmc_io import to_hepmc
from lhe import read_lhe, sha256


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lhe', type=Path, default=Path('out/dy/hard.lhe'))
    parser.add_argument('--card', type=Path, default=Path('config/shower.cmnd'))
    parser.add_argument('--out', type=Path, default=Path('out/dy/showered.hepmc'))
    parser.add_argument('--weights', type=Path, default=Path('out/dy/weights.json'))
    args = parser.parse_args()
    sample = read_lhe(args.lhe)
    if args.out.exists() or args.weights.exists():
        parser.error('Choose new output names for a new shower run.')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.weights.parent.mkdir(parents=True, exist_ok=True)
    pythia = pythia8mc.Pythia()
    if not pythia.readFile(str(args.card)):
        raise RuntimeError('Could not read the shower card.')
    if not pythia.readString('Beams:LHEF = ' + str(args.lhe.resolve())) or not pythia.init():
        raise RuntimeError('Pythia initialization failed.')
    run = pyhepmc.GenRunInfo()
    run.weight_names = sample['labels']
    temporary = args.out.with_suffix(args.out.suffix + '.partial')
    with pyhepmc.open(str(temporary), 'w', format='hepmc3') as writer:
        for source in sample['events']:
            number = source['event_id']
            if not pythia.next():
                raise RuntimeError(f'Pythia failed on input event {number}.')
            info = pythia.infoPython()
            if info.nSelected() != number + 1:
                raise RuntimeError('Pythia skipped an input event; event IDs would no longer match.')
            for label in sample['labels'][1:]:
                if not np.isclose(info.getWeightsDetailedValue(label), source['weights'][label], rtol=1e-10, atol=1e-12):
                    raise RuntimeError(f'LHE/Pythia weight mismatch at event {number}: {label}')
            writer.write(to_hepmc(pythia, number, source['weights'], run))
    # Read the actual serialized file, including its named weights.
    count = 0
    with pyhepmc.open(str(temporary)) as reader:
        for count, event in enumerate(reader, 1):
            source = sample['events'][count - 1]
            if event.event_number != source['event_id'] or event.weight_names != sample['labels']:
                raise RuntimeError('HepMC event ID or weight labels changed on disk.')
            if not np.allclose(event.weights, list(source['weights'][k] for k in sample['labels']), rtol=1e-12, atol=1e-12):
                raise RuntimeError('HepMC weights changed on disk.')
    if count != len(sample['events']):
        raise RuntimeError('HepMC event count differs from the LHE input.')
    temporary.replace(args.out)
    record = {
        'events': [{'event_id': e['event_id'], 'weights': e['weights']} for e in sample['events']],
        'labels': sample['labels'], 'n_events': count,
        'normalisation': 'MadGraph event_norm=average; sum selected weights / all generated events',
        'cross_section_pb': sample['cross_section_pb'],
        'lhe_sha256': sample['source_sha256'], 'hepmc_sha256': sha256(args.out),
        'card_sha256': sha256(args.card),
        'checks': ['Pythia selected all input events in order', 'Pythia detailed weights match LHE',
                   'stable particle identities and four-momenta preserved',
                   'serialized HepMC IDs, weight names and values match LHE']}
    args.weights.write_text(json.dumps(record, indent=2) + '\n')
    pythia.stat()
    print(f'{count} events and {len(sample["labels"])} named weights saved to {args.out}.')


if __name__ == '__main__':
    main()

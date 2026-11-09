"""Read the numerical event records of a MadGraph LHE file."""
import gzip
import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def read_lhe(path):
    path = Path(path)
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt') as handle:
        text = handle.read()
    init = re.search(r'<init>\s*(.*?)\s*</init>', text, re.S)
    if init is None:
        raise ValueError('Missing LHE init block.')
    init_lines = [s.split() for s in init[1].splitlines() if s.strip() and not s.lstrip().startswith('#')]
    n_processes = int(init_lines[0][9])
    cross_section = sum(float(row[0]) for row in init_lines[1:n_processes + 1])
    labels = ['nominal'] + re.findall(r'<weight\s+id=[\'"]([^\'"]+)', text)
    if len(set(labels)) != len(labels):
        raise ValueError('Duplicate weight labels.')
    events = []
    for block in re.findall(r'<event>\s*(.*?)\s*</event>', text, re.S):
        lines = [s for s in block.splitlines() if s.strip() and not s.lstrip().startswith('#')]
        header = lines[0].split()
        n = int(header[0])
        particles = []
        for row in lines[1:n + 1]:
            fields = row.split()
            particles.append({'pid': int(fields[0]), 'status': int(fields[1]),
                              'p4': [float(v) for v in fields[6:10]]})
        weights = {'nominal': float(header[2])}
        weights.update({node.attrib['id']: float(node.text)
                        for node in ET.fromstring('<event>' + block + '</event>').findall('rwgt/wgt')})
        if set(weights) != set(labels):
            raise ValueError(f'Event {len(events)} has a different set of weights.')
        if not np.isfinite(list(weights.values())).all():
            raise ValueError(f'Event {len(events)} has nonfinite weights.')
        events.append({'event_id': len(events), 'particles': particles, 'weights': weights})
    if not events:
        raise ValueError('No LHE events found.')
    nominal_mean = np.mean([e['weights']['nominal'] for e in events])
    if not np.isclose(nominal_mean, cross_section, rtol=1e-5, atol=1e-12):
        raise ValueError('This analysis expects MadGraph event_norm=average: mean nominal weight = cross section.')
    return {'labels': labels, 'cross_section_pb': cross_section, 'events': events,
            'source_sha256': sha256(path)}

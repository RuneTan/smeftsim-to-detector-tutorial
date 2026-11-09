#!/usr/bin/env python3
"""Check the completed local exercises and write a compact validation record."""
import gzip
import importlib.metadata as metadata
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import ROOT
import uproot

from lhe import read_lhe, sha256


def require(condition, message):
    if not condition: raise RuntimeError(message)


def compare_histograms(a, b):
    fa, fb = ROOT.TFile.Open(str(a)), ROOT.TFile.Open(str(b))
    names = sorted(k.GetName() for k in fa.GetListOfKeys())
    require(names == sorted(k.GetName() for k in fb.GetListOfKeys()), 'Different ROOT histogram keys.')
    for name in names:
        x, y = fa.Get(name), fb.Get(name)
        require(x.GetNbinsX()==y.GetNbinsX(), f'{name}: bin count differs.')
        require(x.GetEntries()==y.GetEntries(), f'{name}: entries differ.')
        for i in range(x.GetNbinsX()+2):
            require(x.GetBinContent(i)==y.GetBinContent(i) and x.GetBinError(i)==y.GetBinError(i),
                    f'{name}: content/error differs in bin {i}.')
    fa.Close();fb.Close()
    return len(names)


def main():
    root = Path(__file__).resolve().parents[1]
    ROOT.gROOT.SetBatch(True)
    sample = read_lhe(root/'out/dy/hard.lhe')
    report = json.loads((root/'out/dy/plots/summary.json').read_text())
    weights = json.loads((root/'out/dy/weights.json').read_text())
    require(len(sample['events'])==weights['n_events']==report['generated_events']==1000,
            'Expected the completed 1,000-event main exercise.')
    require(all(v['events']==1000 for v in report['stages'].values()), 'A processing stage lost events.')
    require(report['sm_reweight_max_relative_difference'] < 1e-9, 'SM reweight mismatch.')
    dt = uproot.open(root/'out/dy/delphes.root')['Delphes']
    stored = np.array([row[0] for row in dt['Event.Weight'].array().to_list()])
    nominal = np.array([e['weights']['nominal'] for e in sample['events']])
    require(np.allclose(stored,nominal,rtol=1e-6,atol=1e-6), 'Delphes nominal weights differ.')
    for name in ['dimuon_mass','muon_pt','eft_dimuon_mass']:
        for ext in ['png','pdf']:
            f=root/'out/dy/plots'/f'{name}.{ext}'
            require(f.is_file() and f.stat().st_size>1000, f'Missing figure {f}.')
    equal = compare_histograms(root/'examples/reweighted/histograms.root', root/'out/higgs/reference/histograms.root')
    require(equal==48, 'Expected all 48 original Higgs histograms.')
    htext=(root/'out/higgs/new/events.lhe').read_text()
    hlabels=re.findall(r'<weight\s+id=[\'"]([^\'"]+)',htext)
    require(htext.count('<event>')==200 and len(hlabels)==11, 'New Higgs sample is incomplete.')
    for name in ['mll','mmv','pTl1','pTmu']:
        require((root/'out/higgs/new'/f'plot_{name}.pdf').stat().st_size>1000,'Missing Higgs PDF.')
    with uproot.open(root/'out/higgs/new/histograms.root') as f:
        require(len(f.keys())==48,'Expected 48 new Higgs histograms.')
    ldd=subprocess.run(['ldd',str(root/'tools/delphes/DelphesHepMC3')],capture_output=True,text=True,check=True).stdout
    require('not found' not in ldd and '/detector-learning/' not in ldd, 'Delphes library paths are not self-contained.')
    require(all(str(root/'.venv-unified') in line for line in ldd.splitlines() if '/ROOT/' in line),
            'ROOT libraries are not from the unified environment.')
    packages={name:metadata.version(name) for name in ['numpy','ROOT','pythia8mc','pyhepmc','torch','parnassus','meson','ninja']}
    result={'date':'2026-11-09','python':sys.version.split()[0], 'ROOT_core':ROOT.gROOT.GetVersion(),
            'packages':packages,'dimuon':report,
            'transfer_checks':weights['checks']+['Delphes nominal ROOT weights match LHE',
                'both detector event-ID sets match LHE', 'Delphes links project-local ROOT'],
            'higgs':{'new_events':200,'additional_weights':hlabels,'new_histograms':48,
                     'new_pdf_figures':4,'reference_events':2000,'reference_histograms_exactly_equal':equal},
            'figure_sha256':{f.name:sha256(f) for f in (root/'out/dy/plots').glob('*.png')},
            'scope':'Local LO tutorial, fixed shower/response and widths; parametric Parnassus CMS response.'}
    destination=root/'out/unified-validation/validation.json'
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'dimuon_events':1000,'higgs_events':200,'reference_histograms_exactly_equal':equal,
                      'python':sys.version.split()[0], 'record':str(destination)},indent=2))


if __name__ == '__main__': main()

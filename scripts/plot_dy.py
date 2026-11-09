#!/usr/bin/env python3
"""Plot the same weighted DY sample before and after shower/detector response."""
import argparse
import json
import math
from pathlib import Path

import awkward as ak
import numpy as np
import pyhepmc
import ROOT
import uproot

from lhe import read_lhe, sha256


def observables(muons):
    """muons are (pT, eta, phi, mass); select, then pair the two leading ones."""
    selected = sorted((m for m in muons if m[0] > 10 and abs(m[1]) < 2.4), reverse=True)
    mass = []
    if len(selected) >= 2:
        vectors = []
        for pt, eta, phi, m in selected[:2]:
            px, py, pz = pt * math.cos(phi), pt * math.sin(phi), pt * math.sinh(eta)
            vectors.append(np.array([math.sqrt(m*m + px*px + py*py + pz*pz), px, py, pz]))
        total = vectors[0] + vectors[1]
        mass = [math.sqrt(max(0., total[0]**2 - np.dot(total[1:], total[1:])))]
    return {'mass': mass, 'pt': [m[0] for m in selected]}


def from_p4(p4):
    px, py, pz, energy = p4
    pt = math.hypot(px, py)
    return (pt, math.asinh(pz / pt) if pt else math.copysign(1e10, pz),
            math.atan2(py, px), math.sqrt(max(0., energy*energy - px*px - py*py - pz*pz)))


def align_by_id(ids, rows, expected):
    if len(ids) != len(rows) or len(set(ids)) != len(ids) or set(ids) != set(expected):
        raise ValueError('Event IDs must match the LHE sample exactly, with no missing or duplicate events.')
    lookup = dict(zip(ids, rows))
    return [lookup[i] for i in expected]


def detector_rows(path, backend, expected):
    with uproot.open(path) as handle:
        if backend == 'Delphes':
            tree = handle['Delphes']
            ids = ak.to_list(ak.flatten(tree['Event.Number'].array()))
            prefix = 'Muon'
        else:
            tree = handle['Parnassus']
            ids = tree['Event.EventNumber'].array(library='np').tolist()
            prefix = 'Muons'
        fields = {k: ak.to_list(tree[f'{prefix}.{k}'].array()) for k in ['PT', 'Eta', 'Phi']}
        if backend == 'Parnassus':
            fields['IsolationVar'] = ak.to_list(tree['Muons.IsolationVar'].array())
        rows = []
        for i in range(len(ids)):
            muons = [(pt, eta, phi, 0.105658) for j, (pt, eta, phi) in enumerate(
                zip(fields['PT'][i], fields['Eta'][i], fields['Phi'][i]))
                if backend != 'Parnassus' or fields['IsolationVar'][i][j] < 0.25]
            rows.append(observables(muons))
    return align_by_id(ids, rows, expected)


def event_bins(rows, quantity, edges):
    """One row per event, retaining the covariance between its muon entries."""
    return np.asarray([np.histogram(row[quantity], bins=edges)[0] for row in rows], dtype=float)


def weighted_hist(name, contributions, weights, edges, xlabel, ylabel):
    n = len(weights)
    h = ROOT.TH1D(name, f';{xlabel};{ylabel}', len(edges)-1, np.asarray(edges, dtype='d'))
    h.SetDirectory(0)
    values = contributions * weights[:, None]
    widths = np.diff(edges)
    totals = values.sum(axis=0) / n / widths
    errors = np.sqrt((values*values).sum(axis=0)) / n / widths
    for i, (v, e) in enumerate(zip(totals, errors), 1):
        h.SetBinContent(i, v)
        h.SetBinError(i, e)
    return h


def ratio_values(contributions, target, base):
    a, b = contributions * target[:, None], contributions * base[:, None]
    suma, sumb = a.sum(axis=0), b.sum(axis=0)
    valid = sumb != 0
    ratio = np.zeros_like(suma)
    ratio[valid] = suma[valid] / sumb[valid]
    error = np.zeros_like(suma)
    error[valid] = np.sqrt(((a[:, valid] - ratio[valid]*b[:, valid])**2).sum(axis=0)) / abs(sumb[valid])
    return ratio, error, valid


def style(hist, colour):
    hist.SetLineColor(colour)
    hist.SetMarkerColor(colour)
    hist.SetLineWidth(2)
    hist.GetXaxis().SetTitleSize(0.043)
    hist.GetYaxis().SetTitleSize(0.043)
    hist.GetYaxis().SetTitleOffset(1.45)


def overlay(histograms, labels, colours, out, title):
    canvas = ROOT.TCanvas('canvas_' + out.name, title, 1000, 720)
    canvas.SetLeftMargin(.15)
    canvas.SetBottomMargin(.13)
    top = max(h.GetMaximum() for h in histograms)
    bottom = min(0., min(h.GetMinimum() for h in histograms))
    legend = ROOT.TLegend(.61, .66, .89, .88)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    for i, (h, label, colour) in enumerate(zip(histograms, labels, colours)):
        style(h, colour)
        h.SetMaximum(top * 1.35)
        h.SetMinimum(bottom * 1.2)
        h.Draw('hist' if i == 0 else 'hist same')
        legend.AddEntry(h, label, 'l')
    legend.Draw()
    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextSize(.032)
    text.DrawLatex(.17, .91, title)
    for ext in ['png', 'pdf']:
        canvas.SaveAs(str(out.with_suffix('.' + ext)))
        if not out.with_suffix('.' + ext).is_file():
            raise RuntimeError(f'ROOT did not write {out.with_suffix("." + ext)}.')
    canvas.Close()


def eft_plot(histograms, labels, colours, contributions, weights, edges, out, stage):
    canvas = ROOT.TCanvas('eft', 'EFT at reconstructed level', 1000, 850)
    upper = ROOT.TPad('upper', '', 0, .31, 1, 1)
    lower = ROOT.TPad('lower', '', 0, 0, 1, .31)
    upper.SetLeftMargin(.15); upper.SetBottomMargin(.025)
    lower.SetLeftMargin(.15); lower.SetBottomMargin(.29); lower.SetTopMargin(.025)
    upper.Draw(); lower.Draw(); upper.cd()
    legend = ROOT.TLegend(.58, .62, .90, .88)
    legend.SetBorderSize(0); legend.SetFillStyle(0)
    legend.SetTextSize(.042)
    peak = max(h.GetBinContent(i) for h in histograms for i in range(1,h.GetNbinsX()+1))
    for i, (h, label, colour) in enumerate(zip(histograms, labels, colours)):
        style(h, colour)
        h.GetXaxis().SetLabelSize(0); h.GetXaxis().SetTitleSize(0)
        h.SetMinimum(0); h.SetMaximum(peak*1.35)
        h.Draw('hist' if i == 0 else 'hist same')
        legend.AddEntry(h, label, 'l')
    legend.Draw()
    text = ROOT.TLatex(); text.SetNDC(); text.SetTextSize(.036)
    text.DrawLatex(.17, .92, stage + '  |  #Lambda = 1 TeV, fixed widths')
    lower.cd()
    frame = ROOT.TH1D('ratio_frame', ';m_{#mu#mu} [GeV];EFT / SM', len(edges)-1, np.asarray(edges,dtype='d'))
    ratios = [ratio_values(contributions, w, weights[0]) for w in weights[1:]]
    vals = [v for r,e,ok in ratios for v in np.r_[r[ok]-e[ok],r[ok]+e[ok]]]
    low, high = min([.8]+vals), max([1.2]+vals)
    padding = .1*(high-low)
    frame.SetMinimum(low-padding); frame.SetMaximum(high+padding)
    frame.GetXaxis().SetTitleSize(.11); frame.GetXaxis().SetLabelSize(.09)
    frame.GetYaxis().SetTitleSize(.10); frame.GetYaxis().SetLabelSize(.08)
    frame.GetYaxis().SetTitleOffset(.58); frame.GetYaxis().SetNdivisions(505)
    frame.Draw('axis')
    line = ROOT.TLine(float(edges[0]), 1., float(edges[-1]), 1.)
    line.SetLineStyle(2); line.Draw()
    graphs = []
    centres = (edges[:-1]+edges[1:])/2
    for (r,e,ok),colour in zip(ratios,colours[1:]):
        g = ROOT.TGraphErrors(int(ok.sum()), np.asarray(centres[ok],dtype='d'),
                             np.asarray(r[ok],dtype='d'), np.zeros(int(ok.sum()),dtype='d'), np.asarray(e[ok],dtype='d'))
        g.SetMarkerStyle(20); g.SetMarkerSize(.55); g.SetMarkerColor(colour); g.SetLineColor(colour)
        g.Draw('P same'); graphs.append(g)
    for ext in ['png','pdf']:
        canvas.SaveAs(str(out.with_suffix('.'+ext)))
        if not out.with_suffix('.' + ext).is_file():
            raise RuntimeError(f'ROOT did not write {out.with_suffix("." + ext)}.')
    canvas.Close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lhe', type=Path, default=Path('out/dy/hard.lhe'))
    parser.add_argument('--hepmc', type=Path, default=Path('out/dy/showered.hepmc'))
    parser.add_argument('--weights', type=Path, default=Path('out/dy/weights.json'))
    parser.add_argument('--delphes', type=Path, default=Path('out/dy/delphes.root'))
    parser.add_argument('--parnassus', type=Path)
    parser.add_argument('--out', type=Path, default=Path('out/dy/plots'))
    parser.add_argument('--lhe-only', action='store_true')
    args = parser.parse_args()
    ROOT.gROOT.SetBatch(True); ROOT.gStyle.SetOptStat(0)
    sample = read_lhe(args.lhe)
    expected = [e['event_id'] for e in sample['events']]
    weights = {label: np.array([e['weights'][label] for e in sample['events']]) for label in sample['labels']}
    stages = {'Hard process': [observables([from_p4(p['p4']) for p in e['particles']
                                         if p['status']==1 and abs(p['pid'])==13]) for e in sample['events']]}
    source_hashes = {'lhe': sample['source_sha256']}
    if not args.lhe_only:
        saved = json.loads(args.weights.read_text())
        if saved['lhe_sha256'] != sample['source_sha256'] or saved['hepmc_sha256'] != sha256(args.hepmc):
            raise ValueError('LHE/HepMC files do not match the weight record.')
        if saved['labels'] != sample['labels'] or saved['events'] != [
                {'event_id': e['event_id'], 'weights': e['weights']} for e in sample['events']]:
            raise ValueError('Saved event weights differ from LHE.')
        ids, truth = [], []
        with pyhepmc.open(str(args.hepmc)) as reader:
            for event in reader:
                ids.append(event.event_number)
                truth.append(observables([from_p4([p.momentum.px,p.momentum.py,p.momentum.pz,p.momentum.e])
                                          for p in event.particles if p.status==1 and abs(p.pid)==13]))
        stages['Stable particles'] = align_by_id(ids, truth, expected)
        stages['Delphes'] = detector_rows(args.delphes, 'Delphes', expected)
        source_hashes.update({'hepmc': saved['hepmc_sha256'], 'delphes': sha256(args.delphes)})
        if args.parnassus:
            stages['Parnassus'] = detector_rows(args.parnassus, 'Parnassus', expected)
            source_hashes['parnassus'] = sha256(args.parnassus)
    args.out.mkdir(parents=True, exist_ok=True)
    edges = {'mass': np.linspace(50,130,41), 'pt': np.linspace(0,100,41)}
    xlabels = {'mass': 'm_{#mu#mu} [GeV]', 'pt': 'Muon p_{T} [GeV]'}
    colours = [ROOT.kGray+2, ROOT.kBlack, ROOT.kAzure+1, ROOT.kOrange+7]
    all_histograms, summary, matrices = {}, {}, {}
    for stage, rows in stages.items():
        key = stage.lower().replace(' ', '_')
        matrices[stage] = {q:event_bins(rows,q,edges[q]) for q in edges}
        selected = np.array([bool(row['mass']) for row in rows])
        summary[stage] = {'events':len(rows), 'selected_muons':sum(len(r['pt']) for r in rows),
                          'selected_dimuon_events':int(selected.sum()),
                          'selected_cross_section_pb':{k:float(v[selected].sum()/len(v)) for k,v in weights.items()},
                          'weighted_pair_acceptance':{k:float(v[selected].sum()/v.sum()) for k,v in weights.items()}}
        for quantity in edges:
            for label, values in weights.items():
                name = f'{key}_{quantity}_{label}'
                ylabel = 'd#sigma/dm_{#mu#mu} [pb/GeV]' if quantity == 'mass' else 'd#sigma/dp_{T}^{#mu} [pb/GeV]'
                all_histograms[name] = weighted_hist(name, matrices[stage][quantity], values, edges[quantity],
                                                     xlabels[quantity], ylabel)
    for quantity, stem in [('mass','dimuon_mass'),('pt','muon_pt')]:
        histograms = [all_histograms[f'{s.lower().replace(" ","_")}_{quantity}_nominal'] for s in stages]
        overlay(histograms, list(stages), colours, args.out/stem, 'SMEFTsim SM baseline  |  pp, 13 TeV')
    eft_stage = 'Delphes' if 'Delphes' in stages else 'Hard process'
    eft_labels = ['nominal','cHl3_plus','cHl3_minus']
    if all(k in weights for k in eft_labels):
        histograms = [all_histograms[f'{eft_stage.lower().replace(" ","_")}_mass_{k}'] for k in eft_labels]
        eft_plot(histograms, ['SM','c_{Hl}^{(3)} = +1','c_{Hl}^{(3)} = -1'],
                 [ROOT.kBlack, ROOT.kAzure+1, ROOT.kRed+1], matrices[eft_stage]['mass'],
                 [weights[k] for k in eft_labels], edges['mass'], args.out/'eft_dimuon_mass', eft_stage)
    if 'sm_check' in weights:
        if not np.allclose(weights['sm_check'], weights['nominal'], rtol=1e-9, atol=1e-12):
            raise ValueError('SM reweight check does not reproduce nominal weights.')
    rootfile = ROOT.TFile.Open(str(args.out/'histograms.root'), 'RECREATE')
    for h in all_histograms.values(): h.Write()
    rootfile.Close()
    result = {'generated_events':len(expected), 'weight_labels':sample['labels'],
              'inclusive_cross_section_pb':{k:float(v.mean()) for k,v in weights.items()},
              'selection':'pT > 10 GeV, |eta| < 2.4; two highest-pT muons; Delphes card isolation; Parnassus IsolationVar < 0.25',
              'normalisation':'sum weights / generated events / bin width; pT counts individual muons',
              'uncertainties':'per-event sumw2; EFT/SM ratio includes same-event covariance',
              'stages':summary, 'source_sha256':source_hashes,
              'histograms':len(all_histograms),
              'sm_reweight_max_relative_difference':float(np.max(abs(weights.get('sm_check',weights['nominal'])/weights['nominal']-1)))}
    (args.out/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

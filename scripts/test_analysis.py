#!/usr/bin/env python3
"""Small numerical checks for event alignment and correlated weighted plots."""
import tempfile
import unittest
from pathlib import Path

import numpy as np
import ROOT

from lhe import read_lhe
from plot_dy import align_by_id, event_bins, ratio_values, weighted_hist


class AnalysisTests(unittest.TestCase):
    def test_event_join_uses_ids(self):
        self.assertEqual(align_by_id([2,0,1], ['c','a','b'], [0,1,2]), ['a','b','c'])
        for ids in ([0,0,2], [0,1], [0,1,4]):
            with self.assertRaises(ValueError): align_by_id(ids, list(ids), [0,1,2])

    def test_signed_weights_and_absolute_normalisation(self):
        # Three generated events: one passes twice in one bin, one has negative
        # weight, and one fails selection. Keep N=3, not the number selected.
        rows = [{'pt':[1.2,1.3]}, {'pt':[1.4]}, {'pt':[]}]
        matrix = event_bins(rows, 'pt', np.array([0.,2.,4.]))
        hist = weighted_hist('test_signed', matrix, np.array([6.,-3.,9.]),
                             np.array([0.,2.,4.]), 'x', 'y')
        self.assertAlmostEqual(hist.GetBinContent(1), 1.5)
        self.assertAlmostEqual(hist.GetBinError(1), np.sqrt(12**2+3**2)/6)
        self.assertEqual(hist.GetBinContent(2), 0.)

    def test_ratio_same_events_has_covariance(self):
        matrix = np.array([[1.,0.],[1.,0.],[0.,0.]])
        base = np.array([2.,3.,4.])
        ratio, error, valid = ratio_values(matrix, 2*base, base)
        np.testing.assert_array_equal(valid, [True,False])
        self.assertEqual(ratio[0], 2.)
        self.assertEqual(error[0], 0.)

    def test_lhe_v3_init_metadata_and_signed_reweights(self):
        text = '''<LesHouchesEvents version="3.0">
<header><initrwgt><weightgroup><weight id='linear'>interference</weight></weightgroup></initrwgt></header>
<init>
2212 2212 6500 6500 0 0 0 0 3 1
2.0 0.1 2.0 1
<generator name='MadGraph'>2.9.27</generator>
</init>
<event>
1 1 2.0 91 0.007 0.118
13 1 0 0 0 0 10 0 0 10 0 0 9
<rwgt><wgt id='linear'>-0.5</wgt></rwgt>
</event>
</LesHouchesEvents>'''
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'sample.lhe'
            path.write_text(text)
            sample = read_lhe(path)
            self.assertEqual(sample['labels'], ['nominal','linear'])
            self.assertEqual(sample['events'][0]['weights']['linear'], -.5)
            path.write_text(text.replace("<wgt id='linear'>-0.5</wgt>", ''))
            with self.assertRaises(ValueError): read_lhe(path)


if __name__ == '__main__':
    ROOT.gROOT.SetBatch(True)
    unittest.main()

"""
Task:
Descripion of script here.
"""

# Import Built-Ins
import logging
from unittest import TestCase

# Import Third-Party
import numpy as np

# Import Homebrew
from sparse_dtw import SparseDTW

# Init Logging Facilities
log = logging.getLogger(__name__)


class SPARSE_TEST(TestCase):

    def setUp(self):
        self.s = [3, 4, 5, 3, 3]
        self.q = [1, 2, 2, 1, 0]
        self.dtw = SparseDTW(self.s, self.q, res=.5)

    def test_quantize(self):
        a, b = self.dtw.quantize(self.s), self.dtw.quantize(self.q)
        check_a = np.array([0.0, 0.5, 1.0, 0.0, 0.0])
        check_b = np.array([0.5, 1.0, 1.0, 0.5, 0.0])
        self.assertTrue(np.array_equal(a, check_a))
        self.assertTrue(np.array_equal(b, check_b))

    def test_euc_dist(self):
        self.assertEqual(self.dtw.euc_distance(5,7), 4)

    def test_populate_warp(self):
        self.dtw.populate_warp()
        a = self.dtw.as_arr()
        b = np.array([[4, 0, 0, 4, 9],
                      [9, 4, 4, 9, 16],
                      [16, 9, 9, 16, 0],
                      [4, 0, 0, 4, 9],
                      [4, 0, 0, 4, 9]])
        self.assertTrue(np.array_equal(a, b))

    def test_calculate_warp_costs(self):
        self.dtw.populate_warp()
        self.dtw.calculate_warp_costs()
        a = self.dtw.as_arr()
        b = np.array([[4, 0, 0, 4, 13],
                      [13, 8, 12, 13, 20],
                      [29, 17, 17, 28, 38],
                      [33, 0, 0, 21, 30],
                      [37, 34, 35, 25, 30]])
        self.assertTrue(np.array_equal(a, b), msg="Is:\n%s\nShould be:\n%s" % (a,b))

    def test_calculate_warp_path(self):
        self.dtw.populate_warp()
        self.dtw.calculate_warp_costs()
        sparsed = self.dtw.calculate_warp_path()
        check = [((4, 4), 30), ((3, 3), 21), ((2, 2), 17), ((1, 1), 8), ((0, 0), 4)]
        check.reverse()
        self.assertTrue(sparsed == check, msg=sparsed)

if __name__ == '__main__':

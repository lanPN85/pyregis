import unittest
import numpy as np

from pyregis.engines import utils


class UtilsTest(unittest.TestCase):
    def test_kargmin(self):
        A = np.asarray([14, 7, -1, 5, 8, 44, 12, 0, -2])
        idx = utils.k_argmin(A, 4)
        self.assertListEqual([8, 2, 7, 3], list(idx))

    def test_kargmax(self):
        A = np.asarray([14, 7, -1, 5, 8, 44, 12, 0, -2])
        idx = utils.k_argmax(A, 4)
        self.assertListEqual([5, 0, 6, 4], list(idx))


if __name__ == '__main__':
    unittest.main()

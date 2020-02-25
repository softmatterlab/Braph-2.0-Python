import unittest
from braphy.stat import *
import numpy as np

class TestStatFunctions(unittest.TestCase):
    def test_fdr_1(self):
        p_values = np.array([0.0068, 0.0087, 0.0091, 0.0106, 0.0131,
                             0.0138, 0.0155, 0.0473, 0.0551, 0.0596])
        q = 0.05
        self.assertEqual(StatFunctions.false_discovery_rate(p_values, q), 0.0138)

if __name__ == '__main__':
    unittest.main()

import numpy as np
import unittest

class TestUtility(unittest.TestCase):

    def assertSequenceAlmostEqual(self, test_sequence, true_sequence, places = 7):
        self.assertEqual(len(test_sequence), len(true_sequence))

        for i in range(len(test_sequence)):
            if np.isnan(test_sequence[i]):
                self.assertTrue(np.isnan(true_sequence[i]))
            else:
                self.assertAlmostEqual(test_sequence[i], true_sequence[i], places = places)

    def assertCategorizationEqual(self, test_sequence, true_sequence):
        self.assertEqual(len(test_sequence), len(true_sequence))
        for idx, test_val in enumerate(test_sequence):
            for idx2 in range(idx, len(test_sequence)):
                test_val2 = test_sequence[idx2]
                if(idx == idx2):
                    continue
                if(test_val == test_val2):
                    if true_sequence[idx] != true_sequence[idx2]:
                        hej = 1
                    self.assertEqual(true_sequence[idx], true_sequence[idx2])
                else:
                    self.assertNotEqual(true_sequence[idx], true_sequence[idx2])


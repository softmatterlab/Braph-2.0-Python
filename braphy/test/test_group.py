import unittest
from braphy.cohort.group import Group
from braphy.workflows import *
from braphy.utility.file_utility import abs_path_from_relative
from braphy.test.test_utility import TestUtility

class TestGroup(TestUtility):
    def test_comparison_different_classes(self):
        Group1 = Group(SubjectStructural)
        Group2 = SubjectStructural()
        self.assertRaises(AssertionError, Group1.data_comparison, Group2)

    def test_comparison_different_subject_classes(self):
        Group1 = Group(SubjectStructural)
        Group2 = Group(SubjectFunctional)
        self.assertRaises(AssertionError, Group1.data_comparison, Group2)

    def test_comparison_no_subjects(self):
        Group1 = Group(SubjectStructural)
        Group2 = Group(SubjectStructural)
        self.assertRaises(AssertionError, Group1.data_comparison, Group2)

    def test_comparison(self):
        f1 = abs_path_from_relative(__file__, '../cohort/gr1_MRI.txt')
        f2 = abs_path_from_relative(__file__, '../cohort/gr2_MRI.txt')
        subjects1 = SubjectStructural.from_txt(f1, 68)
        subjects2 = SubjectStructural.from_txt(f2, 68)

        Group1 = Group(SubjectStructural, subjects=subjects1)
        Group2 = Group(SubjectStructural, subjects=subjects2)
        Group1.data_comparison(Group2, permutations = 100)

if __name__ == '__main__':
    unittest.main()

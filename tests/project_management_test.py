'''
Python module for testing file_info.FileData class.
'''
import unittest
import sys
sys.path.insert(1, '..')
import time
import os
import stability


class TestFile(unittest.TestCase):

    @classmethod
    def setUpClass(TestFile):
        print(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static_test_file.txt'))
        TestFile.fdata = stability.File(os.path.join(__file__, 'static_test_file.txt'), 'Static Test File')
        print(TestFile.fdata)

    def test_asdict(self):
        equiv_dict = self.fdata.asdict()
        self.assertTrue(type(equiv_dict) == dict)
        remade_File = stability.File.fromdict(equiv_dict)
        self.assertTrue(remade_File == self.fdata)
        self.assertTrue(remade_File.asdict() == self.fdata.asdict())



if __name__ == '__main__':
    unittest.main()

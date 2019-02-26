'''
Python module for testing file_info.FileData class.
'''
import unittest
import sys
sys.path.insert(1, '..')
import time
import os
import stability


class TestFileData(unittest.TestCase):

    @classmethod
    def setUpClass(TestFileData):
        with open('test_file.txt', 'w') as f:
            f.write('testing file\n')
            f.write('testing file second line 0.2131  01/01/2010\n')
        TestFileData.fdata = stability.FileData('test_file.txt')
        time.sleep(2)

    @classmethod
    def tearDownClass(TestFileData):
        os.remove('test_file.txt')

    def test_filepath(self):
        self.assertTrue(any('test_file' in filename for filename in os.listdir('.')))
        self.assertTrue('test_file' in self.fdata.filepath)
        self.assertTrue(self.fdata.extension == '.txt')

    def test_fileproperties(self):
        now = time.time()
        self.assertTrue(self.fdata.last_modified < now and self.fdata.last_modified > now - 10)
        self.assertTrue(0.03 < self.fdata.size < 0.08)



if __name__ == '__main__':
    unittest.main()

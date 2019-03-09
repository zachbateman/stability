'''
Python module for testing file_info.FileData class.
'''
import unittest
import sys
sys.path.insert(1, '..')
import time
import os
import stability
from pprint import pprint as pp


class TestFile(unittest.TestCase):

    @classmethod
    def setUpClass(TestFile):
        TestFile.fdata = stability.File(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static_test_file.txt'), 'Static Test File')

    def test_asdict(self):
        equiv_dict = self.fdata.asdict()
        self.assertTrue(type(equiv_dict) == dict)
        remade_File = stability.File.fromdict(equiv_dict)
        self.assertTrue(remade_File == self.fdata)
        self.assertTrue(remade_File.asdict() == self.fdata.asdict())


class TestProject(unittest.TestCase):

    @classmethod
    def setUpClass(TestProject):
        TestProject.fdata = stability.File(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Static Test File #1.txt'), 'Testing File #1')
        TestProject.fdata2 = stability.File(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Static Test File #2.txt'), 'Testing File #2')
        TestProject.project = stability.Project('Project Test A', os.path.abspath(__file__))
        TestProject.project.add_file(file_obj=TestProject.fdata)
        TestProject.project.add_file(file_obj=TestProject.fdata2)

    def test_asdict(self):
        equiv_dict = self.project.asdict()
        self.assertTrue(type(equiv_dict) == dict)
        remade_Project = stability.Project.fromdict(equiv_dict)
        self.assertTrue(remade_Project == self.project)
        self.assertTrue(remade_Project.asdict() == self.project.asdict())



if __name__ == '__main__':
    unittest.main()

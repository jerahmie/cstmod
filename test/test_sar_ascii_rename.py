#!/usr/bin/env python
import os
import re
import glob
import fnmatch
from pathlib import Path
import unittest
import sarutils

class TestSarAsciiRename(unittest.TestCase):
    """TestSarAsciiRename - unit testing for sar_ascii_rename functions.
    """
    @classmethod
    def setUpClass(cls):

        cls.test_data_dir = os.path.abspath(os.path.join(__file__, '..',
                                                         '..','Test_Data',
                                                         'Q_matrix_test'))
        """
        sarmmre = re.compile("SAR \(f=[0-9.]+\) \[AC([0-9]+)\].*.txt")
        sarmnre = re.compile("SAR \(f=[0-9.]+\) \[AC([0-9]+)_([0-9]+)\].*.txt")
        sarmnqre = re.compile("SAR \(f=[0-9.]+\) \[AC([0-9]+)_([0-9]+)Q\].*.txt")
        cls.sar_mm_unsorted = []
        cls.sar_mn_unsorted = []
        cls.sar_mnq_unsorted = []
        for file in os.listdir(cls.test_data_dir):
                if sarmmre.match(file):
                    cls.sar_mm_unsorted.append(os.path.join(cls.test_data_dir,file))
                elif sarmnre.match(file):
                    cls.sar_mn_unsorted.append(os.path.join(cls.test_data_dir,file))
                elif sarmnqre.match(file):
                    cls.sar_mnq_unsorted.append(os.path.join(cls.test_data_dir, file))
                else:
                    pass

        print('sar_mm_unsorted: ', cls.sar_mm_unsorted)
        print('sar_mn_unsorted: ', cls.sar_mn_unsorted)
        print('sar_mnq_unsorted: ', cls.sar_mnq_unsorted)
        """
        pass


    def setUp(self):
        self.filenames = ["SAR (f=447) [AC8] (10g).txt",
                          "SAR (f=447) [AC11] (10g).txt",
                          "SAR (f=477) [AC1_2Q] (10g).txt", 
                          "SAR (f=477) [AC2_10] (10g).txt", 
                          "SAR (f=477) [AC16] (10g).txt"]

        self.renamed_sars = ["SAR_Q88.txt",
                             "SAR_Q1111.txt",
                             "SAR_Q12j.txt",
                             "SAR_Q210.txt",
                             "SAR_Q1616.txt"]

        self.full_filepaths = []
        for file in self.filenames:
            full_file = os.path.join(self.test_data_dir,file)
            Path(full_file).touch(exist_ok=True)
            self.full_filepaths.append(full_file)


    def test_self(self):
        """Make sure the unit testing framework is correctly configured.
        """
        self.assertTrue(True)

    def test_extract_mqn(self):
        """Test the ability to extract m, n q from filename.
        """
        self.assertEqual(sarutils.extract_mnq(self.filenames[0]), (8, 8, ''))
        self.assertEqual(sarutils.extract_mnq(self.filenames[1]), (11, 11, ''))
        self.assertEqual(sarutils.extract_mnq(self.filenames[2]), (1, 2, 'Q'))
        self.assertEqual(sarutils.extract_mnq(self.filenames[3]), (2, 10, ''))
        self.assertEqual(sarutils.extract_mnq(self.filenames[4]), (16, 16, ''))

    def test_files_sorted(self):
        """Return a list of sorted files matching the given pattern
        """
        pass

    def test_rename_sar(self):
        for (orig, renamed) in zip(self.full_filepaths, self.renamed_sars):
            self.assertTrue(os.path.exists(orig))
            self.assertEqual(sarutils.new_sar_name(orig), 
                             os.path.join(self.test_data_dir, renamed))
 
        sar_renamed = list(map(sarutils.new_sar_name, self.full_filepaths))

        for (src, dst) in zip(self.full_filepaths, sar_renamed):
            os.rename(src,dst)

        for file in sar_renamed:
            self.assertTrue(os.path.exists(file))
        

    def tearDown(self):
        #for file in self.full_filepaths:
        #    if os.path.exists(file):
        #        os.remove(file)
        pass
    

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
import unittest
import pandas as pd
from DQMaRC import Uniqueness

class TestUniqueness(unittest.TestCase):
    
    def setUp(self):
        # Sample data for testing row uniqueness
        self.df = pd.DataFrame({
            'NHS_number':           ['112233445', '112233445', '12345', 'none', '2233445566', '2233445566'],
            'Gender':               ['Male', 'Male', 'Female', 'Female', 'Male', 'Male'],
            'Age':                  [72, 72, 181, 140, 55, 72],
            'Postcode':             ['AB1 2CD', 'AB1 2CD', 'UB7 0JP', 'UB7 0JP', 'CD2 3EF', 'CD2 3EF'],
            'ICD_10_Code':          ['Y743', 'Y743', 'Unknown', 'Unknown', 'Other', 'Other']
        })

        # Test parameters
        self.test_params = pd.DataFrame({
            'Field':        ['NHS_number', 'Gender', 'Age', 'Postcode', 'ICD_10_Code'],
            'Uniqueness_Rows': [True,       True,    False,     True,       False]
        })

        # Initialize the Uniqueness object
        self.uniqueness = Uniqueness(self.df, self.test_params)

    def test_initialisation(self):
        # Test if the Uniqueness object initializes correctly
        self.assertIsInstance(self.uniqueness, Uniqueness)
        self.assertTrue(isinstance(self.uniqueness.df, pd.DataFrame))
        self.assertTrue(isinstance(self.uniqueness.test_params, pd.DataFrame))

    def test_row_uniqueness(self):
        # Test the row uniqueness method
        self.uniqueness.test_row_uniqueness('Uniqueness_Rows')
        results = self.uniqueness.get_uniqueness_errors()
        print("DATAFRAME: \n", self.df)
        print("TEST row_uniqueness RESULTS: \n", results.transpose(), "\n")

        # Expected results: Row 0, 1, and 5 are duplicates based on 'NHS_number', 'Age', and 'Postcode'
        expected_results = pd.DataFrame({
            'row_uniqueness_|_full_row_uniqueness': [True, False, False, False, True, False]
        })

        # Compare results
        pd.testing.assert_frame_equal(results, expected_results)
        print("TEST row_uniqueness EXPECTED: \n", expected_results.transpose(), "\n")

if __name__ == '__main__':
    unittest.main()

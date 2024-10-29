import unittest
import pandas as pd
from DQMaRC import Accuracy

class TestAccuracy(unittest.TestCase):

    def setUp(self):
        # Sample data for the dataset to be tested
        self.df = pd.DataFrame({
            'NHS_number':           ['112233445', '112233445', '123456', 'none', '2233445566', '2233445566'],
            'Gender':               ['Male', 'Mail', 'Female', 'Female', 'Male', 'Male'],
            'Age':                  [71, 72, 181, 140, 55, 72],
            'Postcode':             ['AB1 2CD', 'AB1 2CD', 'UB7 0JP', 'UB7 0JP', 'CD2 3EF', 'CD2 3EF'],
            'ICD_10_Code':          ['Y743', 'Y743', 'Unknown', 'Unknown', 'Other', 'Other2']
        })

        # Sample data for the gold standard
        self.gold_standard = pd.DataFrame({
            'NHS_number':           ['112233445', '112233445', '12345', 'none', '2233445566', '2233445566'],
            'Gender':               ['Male', 'Male', 'Female', 'Female', 'Male', 'Male'],
            'Age':                  [72, 72, 181, 140, 55, 72],
            'Postcode':             ['AB1 2CD', 'AB1 2CD', 'UB7 0JP', 'UB7 0JP', 'CD2 3EF', 'CD2 3EF'],
            'ICD_10_Code':          ['Y743', 'Y743', 'Unknown', 'Unknown', 'Other', 'Other']
        })

        # Test parameters for the accuracy test
        self.test_params = pd.DataFrame({
            'Field': ['NHS_number', 'Gender', 'Age', 'Postcode', 'ICD_10_Code'],
            'Accuracy_Gold_Standard': [True, True, True, True, True]
        })

        # Initialize the Accuracy object
        self.accuracy = Accuracy(self.df, self.test_params)
        # Set the gold standard
        self.accuracy.set_gold_standard(self.gold_standard)

    def test_initialisation(self):
        # Test if the Accuracy object initializes correctly
        self.assertIsInstance(self.accuracy, Accuracy)
        self.assertTrue(isinstance(self.accuracy.df, pd.DataFrame))
        self.assertTrue(isinstance(self.accuracy.test_params, pd.DataFrame))
        self.assertTrue(isinstance(self.accuracy.gold_standard, pd.DataFrame))

    def test_set_gold_standard(self):
        # Test if the gold standard is set correctly
        self.assertTrue(self.accuracy.gold_standard.equals(self.gold_standard))

    def test_gold_standard_comparison(self):
        # Run the gold standard comparison
        self.accuracy.gold_standard_comparison('Accuracy_Gold_Standard')
        results = self.accuracy.get_results()
        print("DATAFRAME: \n", self.df)
        print("\n")
        print("Gold standard: \n", self.gold_standard)
        print("TEST Accuracy RESULTS: \n", results.transpose(), "\n")

        # Expected results where mismatches occur
        expected_results = pd.DataFrame({
            'Accuracy_Gold_Standard_|_NHS_number':  [0, 0, 1, 0, 0, 0],
            'Accuracy_Gold_Standard_|_Gender':      [0, 1, 0, 0, 0, 0],
            'Accuracy_Gold_Standard_|_Age':         [1, 0, 0, 0, 0, 0],
            'Accuracy_Gold_Standard_|_Postcode':    [0, 0, 0, 0, 0, 0],
            'Accuracy_Gold_Standard_|_ICD_10_Code': [0, 0, 0, 0, 0, 1] 
        })

        # Compare the results
        pd.testing.assert_frame_equal(
            results[['Accuracy_Gold_Standard_|_NHS_number', 
                     'Accuracy_Gold_Standard_|_Gender', 
                     'Accuracy_Gold_Standard_|_Age', 
                     'Accuracy_Gold_Standard_|_Postcode',
                     'Accuracy_Gold_Standard_|_ICD_10_Code']], 
            expected_results
        )
        print("TEST Accuracy EXPECTED: \n", expected_results.transpose(), "\n")

if __name__ == '__main__':
    unittest.main()

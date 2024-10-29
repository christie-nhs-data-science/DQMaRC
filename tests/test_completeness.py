import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from DQMaRC import Completeness

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

class TestCompleteness(unittest.TestCase):
    def setUp(self):
        # self.data = pd.read_csv('./data_unittests/toydf_subset_unittest.csv')
        # Sample data for testing
        self.df = pd.DataFrame({
            'NHS_number':           ['3417315905', '3417315905',    '12345',    'none',     '8832794853'],
            'Gender':               ['Male',        'Female',       '.',        '  ',       'unknown'],
            'Age':                  ['72',          '181',          '140',      '-15',      '55'],
            'Postcode':             ['BS5 0NQ',     'BT78 3PN',     'UB7 0JP',  'NULL',     'B63  3QX'],
            'ICD_10_Code':          ['Y743',        'Y743',         'Unknown',  '  ',       'Other'],
            'Metastatic_Indicator': ['Present',     'Absent',       'Present',  'Absent',   'Present'],
            'Tumour_M_Stage':	    ['M0',          'M0',           'M1',       'pM1a',     'M1a'],
            'Datetime_Event1':      ['13/03/2024 00:00:00','25/03/2022 00:00:00','21/03/2024 00:00:00',
                                     '12/03/2024 00:00:00','005/03/2024  00:00:00'],
            'Datetime_Logging1':    ['13/03/2024 00:11:00','25/03/2022 00:02:00','21/03/2034 00:31:00',
                                     '12/03/2024 00:08:00','005/03/2024  00:10:00']
            })

        # Test parameters
        # self.test_params = pd.read_csv('./data_unittests/test_params_unittest.csv')
        self.test_params = pd.DataFrame({
            'Field': ['NHS_number',     'Gender',       'Age',  
                      'Postcode',       'ICD_10_Code',  'Metastatic_Indicator',
                      'Tumour_M_Stage',  'Datetime_Event1',  'Datetime_Logging1'],

            'Completeness_NULL': [True, True, True, True, True, True, True, True, True],

            'Completeness_Empty': [True, True, True, True, True, True, True, True, True],

            'Completeness_Encoded': [True, True, False, True, True, False, False, False, False],

            'Completeness_Encoded_Mapping': ['none',        # NHS_number
                                             '.|unknown',   # Gender
                                             '',            # Age
                                             '',            # Postcode
                                             'Unknown|Other',     # ICD_10_Code
                                             '',            # Metastatic_Indicator 
                                             '',            # Tumour_M_Stage
                                             '',            # Datetime_EVent1
                                             ''             # Datetime_Logging1
                                             ]
        })

        # Initialise Completeness object
        self.completeness = Completeness(self.df, self.test_params)
        
    def test_initialisation(self):
        # Test if the object initialises correctly
        self.assertIsInstance(self.completeness, Completeness)
        self.assertTrue(isinstance(self.completeness.df, pd.DataFrame))
        self.assertTrue(isinstance(self.completeness.test_params, pd.DataFrame))

    def test_test_null(self):
        print(f" \n ===========\n =========== \n Running test_null \n {datetime.now()} \n =========== \n =========== \n") # debugging
        # Test the test_null method
        self.completeness.test_null('Completeness_NULL')
        results = self.completeness.run_metrics()
        results = self.completeness.get_results()
        results = results[[
            'Completeness_NULL_|_NHS_number',
            'Completeness_NULL_|_Gender',
            'Completeness_NULL_|_Age',
            'Completeness_NULL_|_Postcode',
            'Completeness_NULL_|_ICD_10_Code',
            'Completeness_NULL_|_Metastatic_Indicator',
            'Completeness_NULL_|_Tumour_M_Stage',
            'Completeness_NULL_|_Datetime_Event1',
            'Completeness_NULL_|_Datetime_Logging1'
        ]]
        print("TEST NULL RESULTS: \n", results.transpose(), "\n")
        # print("===============================\n=================================\n========================")
        # print(" \n ==================== \n Data after test_null:\n ==================== \n ", self.df) # debugging
        
        # Expected result
        # expected_null_results = pd.read_csv("toy_df_DQ_results_full.csv")
        expected_null_results = pd.DataFrame({
            'Completeness_NULL_|_NHS_number':           [0, 0, 0, 0, 0],
            'Completeness_NULL_|_Gender':               [0, 0, 0, 0, 0],
            'Completeness_NULL_|_Age':                  [0, 0, 0, 0, 0],
            'Completeness_NULL_|_Postcode':             [0, 0, 0, 1, 0],
            'Completeness_NULL_|_ICD_10_Code':          [0, 0, 0, 0, 0],
            'Completeness_NULL_|_Metastatic_Indicator': [0, 0, 0, 0, 0],
            'Completeness_NULL_|_Tumour_M_Stage':       [0, 0, 0, 0, 0],
            'Completeness_NULL_|_Datetime_Event1':      [0, 0, 0, 0, 0],
            'Completeness_NULL_|_Datetime_Logging1':    [0, 0, 0, 0, 0]
            })
        print("TEST NULL EXPECTED: \n", expected_null_results.transpose(), "\n")

        pd.testing.assert_frame_equal(results, expected_null_results)

    def test_test_empty(self):
        # Test the test_empty method
        print(f" \n ===========\n =========== \n Running test_empty \n {datetime.now()} \n =========== \n =========== \n") # debugging
        self.completeness.test_empty('Completeness_Empty')
        results = self.completeness.get_results()
        results = results[[
            'Completeness_Empty_|_NHS_number',
            'Completeness_Empty_|_Gender',
            'Completeness_Empty_|_Age',
            'Completeness_Empty_|_Postcode',
            'Completeness_Empty_|_ICD_10_Code',
            'Completeness_Empty_|_Metastatic_Indicator',
            'Completeness_Empty_|_Tumour_M_Stage',
            'Completeness_Empty_|_Datetime_Event1',
            'Completeness_Empty_|_Datetime_Logging1'
        ]]
        print("TEST EMPTY RESULTS: \n", results.transpose(), "\n")

        # print(" \n ==================== \n Data after test_empty:\n ==================== ", self.df) # debugging

        # Expected result: 'Gender' has one empty string, 'City' has one empty string
        expected_empty_results = pd.DataFrame({
            'Completeness_Empty_|_NHS_number':           [0, 0, 0, 0, 0],
            'Completeness_Empty_|_Gender':               [0, 0, 0, 1, 0],
            'Completeness_Empty_|_Age':                  [0, 0, 0, 0, 0],
            'Completeness_Empty_|_Postcode':             [0, 0, 0, 0, 0],
            'Completeness_Empty_|_ICD_10_Code':          [0, 0, 0, 1, 0],
            'Completeness_Empty_|_Metastatic_Indicator': [0, 0, 0, 0, 0],
            'Completeness_Empty_|_Tumour_M_Stage':       [0, 0, 0, 0, 0],
            'Completeness_Empty_|_Datetime_Event1':      [0, 0, 0, 0, 0],
            'Completeness_Empty_|_Datetime_Logging1':    [0, 0, 0, 0, 0]
            })
        print("TEST EMPTY EXPECTED: \n", expected_empty_results.transpose(), "\n")
        pd.testing.assert_frame_equal(results, expected_empty_results)

    def test_test_na_strings(self):
        print(f" \n ===========\n =========== \n Running test_na \n {datetime.now()} \n =========== \n =========== \n") # debugging
        # Test the test_na_strings method
        self.completeness.test_na_strings('Completeness_Encoded')
        results = self.completeness.get_results()
        results = results[[
            'Completeness_Encoded_|_NHS_number',
            'Completeness_Encoded_|_Gender',
            'Completeness_Encoded_|_Postcode',
            'Completeness_Encoded_|_ICD_10_Code'
        ]]
        print("TEST na_strings RESULTS: \n", results.transpose(), "\n")

        # print(" \n ==================== \n Data after test_na:\n ==================== ", self.df) # debugging

        # Expected result: 'Gender' has one "Not Known" value, 'City' has one "na" value
        expected_na_results = pd.DataFrame({
            'Completeness_Encoded_|_NHS_number':           [0, 0, 0, 1, 0],
            'Completeness_Encoded_|_Gender':               [0, 0, 1, 0, 1],
            'Completeness_Encoded_|_Postcode':             [0, 0, 0, 0, 0],
            'Completeness_Encoded_|_ICD_10_Code':          [0, 0, 1, 0, 1]
            })
        print("TEST na_strings EXPECTED: \n", expected_na_results.transpose(), "\n")
        pd.testing.assert_frame_equal(results, expected_na_results)

    # Debugging prints
        # print("Dataframe for testing (self.df):\n", self.df)
        # print(" \n ==================== \n TEST PARAMETERS:\n ==================== ", self.test_params)

if __name__ == '__main__':
    unittest.main()

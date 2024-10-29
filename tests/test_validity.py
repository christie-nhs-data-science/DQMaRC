import unittest
import pandas as pd
from datetime import datetime
from DQMaRC import Validity

class TestValidity(unittest.TestCase):
    def setUp(self):
        # Sample dataset for testing
        self.df = pd.DataFrame({
            'NHS_number':           ['3417315905', '3417315905',    '12345',    'none',     '8832794853'],
            'Gender':               ['Mail',        'Female',       '.',        'Femail',   'Male'],
            'Age':                  ['72',          '181',          '140',      '-15',      '55'],
            'Postcode':             ['BS5 0NQ',     'BT78 3PN',     'UB7 0JP',  'NULL',     'B63  3QX'],
            'ICD_10_Code':          ['Y743',        'Y743',         'Unknown',  'AB124c',   'Other'],
            'Metastatic_Indicator': ['Present',     'Absent',       'Present',  'Absent',   'Present'],
            'Tumour_M_Stage':	    ['M0',          'M01',           'M1',       'pM1a',     'M1a'],

            'Datetime_Event1':      ['13/03/2034 00:00:00','25/03/2022 00:00:00','21/03/2024 00:00:00',
                                     '21/03/2024 00:00:00','005/03/2024  00:00:00'],

            'Datetime_Logging1':    ['13/03/2024 00:11:00','25/03/2022 00:02:00','21/03/2034 00:31:00',
                                     '21/03/2024 00:08:00','005/03/2024  00:10:00']
            })

        # Sample test parameters for testing
        self.test_params = pd.DataFrame({
            'Field': ['NHS_number', 'Gender', 'Age', 
                      'Postcode', 'ICD_10_Code', 'Metastatic_Indicator',
                      'Tumour_M_Stage', 'Datetime_Event1', 'Datetime_Logging1'],
                      
            'Date_Format': ['', '', '', '', '', '', '', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S'],


            'Validity_Dates_Future': [False, False, False, False, 
                                      False, False, False, True, True],
            'Validity_Date_Range': [False, False, False, False, 
                                    False, False, False, True, False],
            'Validity_Date_Range_Min': [None, None, None, None, 
                                        None, None, None, 
                                        '01/01/2023 00:00:00', # Datetime_Event1
                                        None],
            'Validity_Date_Range_Max': [None, None, None, None, 
                                        None, None, None, 
                                        '31/12/2024 00:00:00', # Datetime_Event1
                                        None],
            'Validity_NHS_Number': [True, False, False, False, 
                                    False, False, False, False, False],
            'Validity_Postcode_UK': [False, False, False, True, 
                                     False, False, False, False, False],
            'Validity_Lookup_Table': [False, 
                                      True,  # Gender
                                      False, False, 
                                      True, # ICD_10_Code
                                      False, 
                                      True, # Tumour_M_Stage
                                      False, False],
            'Validity_Lookup_Type': [None, 
                                    'File', # Gender
                                    None, None, 
                                    'File', # ICD_10_Code
                                    None,
                                    'Values', # Tumour_M_Stage
                                    None, None],
            'Validity_Lookup_Codes': [None, 
                                    'LU_toydf_gender.csv', # Gender
                                    None, None, 
                                    'LU_toydf_ICD10_v5.csv', # ICD_10_Code
                                    None,
                                    'M0|M1|pM1a|M1a', # Tumour_M_Stage
                                    None, None],
            'Validity_Range': [False, False, 
                               True, # Age
                               False, False, False, False, False, False],
            'Validity_Range_Numeric': [None, None, 
                                       '0|110', # Age
                                       None, None, None, None, None, None],
            'Validity_Pattern': [False, False, False, False, 
                                 False, False, False, True, True],
            'Validity_Pattern_Regex': [None, None, None, None, None, None, None, 
                                       r'(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2})',  # Datetime_Event1
                                       r'(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2})'   # Datetime_Logging1
                                       ]
        })

        # Initialise Validity object
        self.validity = Validity(self.df, self.test_params)

    def test_initialisation(self):
        # Test if the object initializes correctly
        self.assertIsInstance(self.validity, Validity)
        self.assertTrue(isinstance(self.validity.df, pd.DataFrame))
        self.assertTrue(isinstance(self.validity.test_params, pd.DataFrame))

    def test_valid_nhs_numbers(self):
        # Test the NHS number validation
        self.validity.test_nhs_numbers('Validity_NHS_Number')
        results = self.validity.get_results()[['Validity_NHS_Number_|_NHS_number']]
        print("TEST NHS Num RESULTS: \n", results.transpose(), "\n")
        expected_results = pd.DataFrame({
            'Validity_NHS_Number_|_NHS_number': [0, 0, 1, 1, 0]
        })
        pd.testing.assert_frame_equal(results, expected_results)
        print("TEST NHS Num EXPECTED: \n", expected_results.transpose(), "\n")

    def test_postcode_validation(self):
        # Test the postcode validation
        self.validity.test_postcode('Validity_Postcode_UK')
        results = self.validity.get_results()[['Validity_Postcode_UK_|_Postcode']]
        print("TEST Postcode RESULTS: \n", results.transpose(), "\n")
        expected_results = pd.DataFrame({
            'Validity_Postcode_UK_|_Postcode': [0, 0, 0, 1, 1]
        })
        print("TEST Postcode EXPECTED: \n", expected_results.transpose(), "\n")
        pd.testing.assert_frame_equal(results, expected_results)

    def test_lookup_table(self):
        # Test lookup table validation (mocked as passed)
        self.validity.test_against_lookup_tables('Validity_Lookup_Table')
        results = self.validity.get_results()[['Validity_Lookup_Table_|_Gender', 
                                               'Validity_Lookup_Table_|_ICD_10_Code',
                                               'Validity_Lookup_Table_|_Tumour_M_Stage']]
        print("TEST Lookup RESULTS: \n", results.transpose(), "\n")
        expected_results = pd.DataFrame({
            'Validity_Lookup_Table_|_Gender': [1, 0, 1, 1, 0],
            'Validity_Lookup_Table_|_ICD_10_Code': [0, 0, 1, 1, 1],
            'Validity_Lookup_Table_|_Tumour_M_Stage': [0, 1, 0, 0, 0]
        })
        print("TEST Lookup EXPECTED: \n", expected_results.transpose(), "\n")
        pd.testing.assert_frame_equal(results, expected_results)

    def test_numeric_range(self):
        # Test the numeric range validation
        self.validity.test_ranges('Validity_Range')
        results = self.validity.get_results()[['Validity_Range_|_Age']]
        print("TEST Numeric RESULTS: \n", results.transpose(), "\n")
        expected_results = pd.DataFrame({
            'Validity_Range_|_Age': [0, 1, 1, 1, 0]
        })
        print("TEST Numeric EXPECTED: \n", expected_results.transpose(), "\n")
        pd.testing.assert_frame_equal(results, expected_results)

    def test_future_dates(self):
        # Test the future date validation
        self.validity.test_future_dates('Validity_Dates_Future')
        results = self.validity.get_results()[['Validity_Dates_Future_|_Datetime_Event1', 'Validity_Dates_Future_|_Datetime_Logging1']]
        print("TEST future_dates RESULTS: \n", results.transpose(), "\n")
        expected_results = pd.DataFrame({
            'Validity_Dates_Future_|_Datetime_Event1': [1, 0, 0, 0, 0],
            'Validity_Dates_Future_|_Datetime_Logging1': [0, 0, 1, 0, 0]
        })
        print("TEST future_dates EXPECTED: \n", expected_results.transpose(), "\n")
        pd.testing.assert_frame_equal(results, expected_results)

    def test_min_max_dates(self):
        # Test the min/max date validation
        self.validity.min_max_dates('Validity_Date_Range')
        results = self.validity.get_results()[['Validity_Date_Range_|_Datetime_Event1']]
        print("TEST min_max_dates RESULTS: \n", results.transpose(), "\n")
        expected_results = pd.DataFrame({
            'Validity_Date_Range_|_Datetime_Event1': [1, 1, 0, 0, 0]
        })
        print("TEST min_max_dates EXPECTED: \n", expected_results.transpose(), "\n")
        pd.testing.assert_frame_equal(results, expected_results)

    def test_pattern_validity(self):
        # Test the pattern validity
        self.validity.test_pattern_validity('Validity_Pattern')
        results = self.validity.get_results()[['Validity_Pattern_|_Datetime_Event1', 'Validity_Pattern_|_Datetime_Logging1']]
        print("TEST pattern RESULTS: \n", results.transpose(), "\n")
        expected_results = pd.DataFrame({
            'Validity_Pattern_|_Datetime_Event1': [0, 0, 0, 0, 1],
            'Validity_Pattern_|_Datetime_Logging1': [0, 0, 0, 0, 1]
        })
        print("TEST pattern EXPECTED: \n", expected_results.transpose(), "\n")
        pd.testing.assert_frame_equal(results, expected_results)

if __name__ == '__main__':
    unittest.main()

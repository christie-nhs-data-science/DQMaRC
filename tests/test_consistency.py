import unittest
import pandas as pd
from DQMaRC import Consistency

class TestConsistency(unittest.TestCase):
    
    def setUp(self):
        # Sample data for testing consistency
        self.df = pd.DataFrame({
            'NHS_number':           ['3417315905', '3417315905',    '12345',    'none',     '8832794853'],
            'Gender':               ['Male',        'Female',       '.',        '  ',       'unknown'],
            'Age':                  ['72',          '181',          '140',      '-15',      '55'],
            'Postcode':             ['BS5 0NQ',     'BT78 3PN',     'UB7 0JP',  'NULL',     'B63  3QX'],
            'ICD_10_Code':          ['Y743',        'Y743',         'Unknown',  '  ',       'Other'],
            'Metastatic_Indicator': ['Present',     'Absent',       'Present',  'Absent',   'Present'],
            'Tumour_M_Stage':	    ['M0',          'M0',           'M1',       'pM1a',     'M1a'],
            'Datetime_Event1':      ['14/03/2024 00:00:00','25/03/2022 00:00:00','21/03/2024 00:00:00',
                                     '12/03/2024 00:00:00','005/03/2024  00:00:00'],
            'Datetime_Logging1':    ['13/03/2024 00:11:00','24/03/2022 00:02:00','21/03/2034 00:31:00',
                                     '12/03/2024 00:08:00','005/03/2024  00:10:00']
        })

        # Test parameters for Consistency checks
        self.test_params = pd.DataFrame({
            'Field': ['NHS_number', 'Gender', 'Age', 
                      'Postcode', 'ICD_10_Code', 'Metastatic_Indicator',
                      'Tumour_M_Stage', 'Datetime_Event1', 'Datetime_Logging1'],
                      
            'Date_Format': ['', '', '', '', '', '', '', 
                            '%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S'],

            'Consistency_Compare': [False, False, False, False, 
                                    False, 
                                    True, # Metastatic_Indicator vs Tumour_M_Stage
                                    False, False, False],
            'Consistency_Compare_Field': ['', '', '', '', '', 
                                          'Tumour_M_Stage',
                                          '', '', ''],
            'Consistency_Compare_Mapping': ['', '', '', '', '', 
                                            '{"Absent": ["M0"], "Present": ["M1", "M1a", "M1b", "M1c", "M1d", "pM1", "pM1a", "pM1b", "pM1c", "pM1d"]}',
                                            '', '', ''],
            'Consistency_Date_Relations': [False, False, False, False, 
                                           False, False, False, True, True],
            'Consistency_Date_Relationship': ['', '', '', '', '', '', '', 
                                              '<', '>'],
            'Consistency_Date_Relations_Field': ['', '', '', '', '', '', '', 
                                                'Datetime_Logging1', 'Datetime_Event1']
        })

        # Initialize the Consistency object
        self.consistency = Consistency(self.df, self.test_params)

    def test_initialisation(self):
        # Test if the Consistency object initializes correctly
        self.assertIsInstance(self.consistency, Consistency)
        self.assertTrue(isinstance(self.consistency.df, pd.DataFrame))
        self.assertTrue(isinstance(self.consistency.test_params, pd.DataFrame))

    def test_one_to_one(self):
        # Test the one-to-one consistency method
        self.consistency.test_one_to_one('Consistency_Compare')
        results = self.consistency.get_results()
        print("TEST one_to_one RESULTS: \n", results.transpose(), "\n")

        # Expected results: Metastatic_Indicator should be consistent with Tumour_M_Stage
        expected_results = pd.DataFrame({
            'Consistency_Compare_|_Metastatic_Indicator': [1, 0, 0, 1, 0]
        })

        # Compare results
        pd.testing.assert_frame_equal(results[['Consistency_Compare_|_Metastatic_Indicator']], expected_results)
        print("TEST one_to_one EXPECTED: \n", expected_results.transpose(), "\n")

    def test_date_relationships(self):
        # Test the date relationships consistency method
        self.consistency.date_relationships('Consistency_Date_Relations')
        results = self.consistency.get_results()
        print("TEST date_relationships RESULTS: \n", results.transpose(), "\n")

        # Expected results for the date relationship between Datetime_Event1 and Datetime_Logging1
        expected_results = pd.DataFrame({
            'Consistency_Date_Relations_|_Datetime_Event1': [1, 1, 0, 0, 0],
            'Consistency_Date_Relations_|_Datetime_Logging1': [1, 1, 0, 0, 0]
        })
        print("TEST date_relationships EXPECTED: \n", expected_results.transpose(), "\n")

        # Compare results
        pd.testing.assert_frame_equal(results[['Consistency_Date_Relations_|_Datetime_Event1', 'Consistency_Date_Relations_|_Datetime_Logging1']], expected_results)

if __name__ == '__main__':
    unittest.main()

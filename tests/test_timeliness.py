import unittest
import pandas as pd
from DQMaRC import Timeliness

class TestTimeliness(unittest.TestCase):

    def setUp(self):
        # Sample data for testing timeliness
        self.df = pd.DataFrame({
            # 'NHS_number':           ['3417315905', '3417315905',    '12345',    'none',     '8832794853'],
            'Datetime_Event1':      ['13/03/2024 00:00:00',
                                     '25/03/2022 00:00:00',
                                     '21/03/2024 00:00:00',
                                     '12/03/2024 00:00:00',
                                     '005/03/2024  00:00:00'],
            'Datetime_Logging1':    ['13/03/2024 00:11:00',
                                     '25/03/2022 00:02:00',
                                     '21/03/2034 00:31:00',
                                     '12/03/2024 00:08:00',
                                     '005/03/2024  00:10:00']
        })

        # Test parameters for timeliness tests
        self.test_params = pd.DataFrame({
            'Field': ['Datetime_Event1', 'Datetime_Logging1'],
            'Date_Format': ['dd/mm/yyyy HH:MM:SS','dd/mm/yyyy HH:MM:SS'],
            'Timeliness_Date_Diff': [True, True],
            'Timeliness_Date_Diff_Field': ['Datetime_Logging1', 'Datetime_Event1'],
            'Timeliness_Date_Diff_Threshold': [10, 10],  # Threshold is 10 minutes
        })

        # Initialize the Timeliness object
        self.timeliness = Timeliness(self.df, self.test_params)

    def test_initialisation(self):
        # Test if the Timeliness object initializes correctly
        self.assertIsInstance(self.timeliness, Timeliness)
        self.assertTrue(isinstance(self.timeliness.df, pd.DataFrame))
        self.assertTrue(isinstance(self.timeliness.test_params, pd.DataFrame))

    def test_date_diff_calc(self):
        # Test the date difference calculation method
        self.timeliness.date_diff_calc('Timeliness_Date_Diff')
        results = self.timeliness.get_results()
        print("TEST date_diff_calc RESULTS: \n", results.transpose(), "\n")

        # Expected results: Rows that exceed the 10-minute threshold should return 1
        expected_results = pd.DataFrame({
            'Timeliness_Date_Diff_|_Datetime_Event1': [1, 0, 1, 0, 1],
            'Timeliness_Date_Diff_|_Datetime_Logging1': [0, 0, 0, 0, 1]
        })

        # Compare results
        pd.testing.assert_frame_equal(results[['Timeliness_Date_Diff_|_Datetime_Event1', 'Timeliness_Date_Diff_|_Datetime_Logging1']], expected_results)
        print("TEST date_diff_calc EXPECTED: \n", expected_results.transpose(), "\n")


if __name__ == '__main__':
    unittest.main()

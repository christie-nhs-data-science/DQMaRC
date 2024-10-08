import pandas as pd
import numpy as np
from datetime import datetime
from .Dimension import Dimension


class Timeliness(Dimension):
    """
    A subclass of Dimension focused on evaluating the timeliness aspect of data quality.
    
    This class assesses the timeliness of data by calculating the difference in time between two date columns in a dataset and comparing this difference to a predefined threshold.
    
    Attributes
    ----------
    df : pandas.DataFrame
        The dataset to be evaluated, imported via pandas' read_csv() function.
    test_params : pandas.DataFrame
        The parameters defining how tests should be conducted, including comparison column names and threshold values.
    date_format : str
        The format in which date strings in the dataset are formatted. This should match the actual format used in the dataset for accurate parsing and comparison.
    tests : dict
        A dictionary mapping test names to their relevant information and methods. Currently supports a date difference calculation test.
    
    Methods
    -------
    date_diff_calc(test)
        Calculates the time difference between two date columns for each row in the dataset, checks if this difference meets a specified threshold, and flags non-compliant rows.
        
        Parameters
        ----------
        test : dict
            The test configuration, including the comparison column name and date difference threshold.
    """

    def __init__(self, df, test_params):
        # """
        # Initialises the Timeliness object with a dataset and test parameters.
        
        # Parameters
        # ----------
        # df : pandas.DataFrame
        #     The dataset to be evaluated.
        # test_params : pandas.DataFrame
        #     The parameters defining how tests should be conducted, including comparison column names and threshold values.
        # """

        Dimension.__init__(self, df, test_params)
        self.tests = {
            'Timeliness_Date_Diff': {'method': self.date_diff_calc, 'default': False, 'arg1': 'Timeliness_Date_Diff_Field', 'arg2': 'Timeliness_Date_Diff_Threshold'
            }
        }
        
    def date_diff_calc(self, test):
        # """
        # Executes the date difference calculation test for specified columns in the dataset.
        
        # Parameters
        # ----------
        # test : dict
        #     The test configuration, including the comparison column name and date difference threshold.

        # """
        def func(col, extra_args=None):
            # Retrieve comparison column name and threshold value from test parameters
            date_compare_col = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item()
            datediff_threshold = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg2']].item()
            date_format_field1 = self.get_date_format(col)
            date_format_field2 = self.get_date_format(date_compare_col)

            def inner(x):
                try:
                    if pd.isna(date_compare_col) or pd.isna(datediff_threshold):
                        return False 
                    
                    # Parse start and end times using the predefined date format
                    start_time = pd.to_datetime(x[col], format=date_format_field1)
                    end_time = pd.to_datetime(x[date_compare_col], format=date_format_field2)
                    time_diff = end_time - start_time
                    time_diff_mins = time_diff.total_seconds() / 60
                    
                    # Check if the time difference is below the threshold (indicating an issue)
                    return not int(time_diff_mins < datediff_threshold)
                
                except Exception as e:
                    # Log any exceptions encountered during processing
                    print(f"Error processing row: {e}")
                    # Return 1 to indicate an error or non-compliance
                    return 1 

            # Apply the inner function across the dataset, row-wise
            return self.df.apply(inner, axis=1)

        self.run_metric(test, func)
        
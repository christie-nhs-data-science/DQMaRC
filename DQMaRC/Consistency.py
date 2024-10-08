import pandas as pd
import numpy as np
from functools import reduce
import json
from .Dimension import Dimension
from datetime import datetime

class Consistency(Dimension):
    """
    A subclass of Dimension focused on evaluating the consistency of data within a dataset.
    
    This class performs consistency tests to ensure that data values across different columns adhere to predefined 
    logical relationships or mappings. It supports one-to-one and one-to-many comparisons, as well as date 
    relationship validations.
    
    Attributes
    ----------
    df : pandas.DataFrame
        The dataset to be evaluated, imported via pandas' read_csv() function.
    test_params : pandas.DataFrame
        The parameters defining how tests should be conducted, including comparison columns and mappings for consistency checks.
    date_format : str
        The format used for parsing dates within the dataset. This should match the actual date format for accurate comparisons.
    tests : dict
        A dictionary mapping test names to their relevant information and methods. Supports tests for one-to-one or 
        one-to-many comparisons and date relationships.
    
    Methods
    -------
    test_one_to_one(test)
        Performs one-to-one or one-to-many comparisons between values in specified columns based on a mapping.
        
        Parameters
        ----------
        test : str
            The name of the test to be executed.

    date_relationships(test)
        Validates date relationships (e.g., greater than, less than) between two date columns.
        
        Parameters
        ----------
        test : str
            The name of the test to be executed.

    """

    def __init__(self, df, test_params):
        # """
        # Initialises the Consistency object with a dataset and test parameters.
        
        # Parameters
        # ----------
        # df : pandas.DataFrame
        #     The dataset to be evaluated.
        # test_params : pandas.DataFrame
        #     The parameters defining how tests should be conducted.
        # """

        Dimension.__init__(self, df, test_params)

        self.tests = {
            'Consistency_Compare': {
                'method': self.test_one_to_one, 
                'default': False, 
                'arg1': 'Consistency_Compare_Field', 
                'arg2': 'Consistency_Compare_Mapping'
            },
            'Consistency_Date_Relations': {
                'method': self.date_relationships, 
                'default': False, 
                'arg1': 'Consistency_Date_Relationship', 
                'arg2': 'Consistency_Date_Relations_Field'
            }
        }

    def test_one_to_one(self, test):
        # """
        # Performs one-to-one or one-to-many comparisons between column values based on a provided mapping.
        
        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed.
        # """

        # ============ NEW one-to-many comparisons method ============
        def func(col):
            comparison_col = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item()
            comparison_map_str = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg2']].item()

            if not pd.isna(comparison_map_str):
                comparison_map = json.loads(comparison_map_str) 
                
                def compare(x):
                    actual_value = str(x[col])
                    # get comparison val 
                    comparison_value = str(x[comparison_col])

                    for key, expected_values in comparison_map.items():
                        # convert key to string to match actual value 
                        key_str = str(key)
                        # expected_values is a list 
                        if not isinstance(expected_values, list):
                            expected_values = [expected_values]

                        # Check if actual_value matches key (for one-to-one mapping)
                        # or if comparison_value is in the expected_values list (for one-to-many)
                        if key_str == actual_value and comparison_value in expected_values:
                            return 0  # Match found, i.e. is correct

                    return 1 # No match found, i.e. error

                return self.df.apply(compare, axis=1)
            else:
                # if comparison_map not defined, use equality comparison from previous method
                return ~(self.df[col] == self.df[comparison_col]).astype(int)
        
        self.run_metric(test, func)

    def date_relationships(self, test):
        # """
        # Validates date relationships (e.g., greater than, less than) between two date columns.
        
        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed.
        # """

        def func(col, extra_args=None):
            comparison = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item()
            comp_col = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg2']].item()
            date_format_field1 = self.get_date_format(col)
            date_format_field2 = self.get_date_format(comp_col)

            def inner(x):
                try:
                    if comparison == '>':
                        return not (pd.to_datetime(x[col], format=date_format_field1) > pd.to_datetime(x[comp_col], format=date_format_field2))
                    elif comparison == '>=':
                        return not (pd.to_datetime(x[col], format=date_format_field1) >= pd.to_datetime(x[comp_col], format=date_format_field2))
                    elif comparison == '<':
                        return not (pd.to_datetime(x[col], format=date_format_field1) < pd.to_datetime(x[comp_col], format=date_format_field2))
                    elif comparison == '<=':
                        return not (pd.to_datetime(x[col], format=date_format_field1) <= pd.to_datetime(x[comp_col], format=date_format_field2))
                    else:
                        return False
                except (ValueError, TypeError):
                    return False

            return self.df.apply(inner, axis=1)

        self.run_metric(test, func)


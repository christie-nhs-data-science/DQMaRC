import pandas as pd
import numpy as np
from .Dimension import Dimension

class Completeness(Dimension):
    """
    A subclass of Dimension to assess the completeness aspect of data quality within a dataset.

    This class focuses on identifying and quantifying missing or incomplete data points within a given dataset.
    It uses predefined tests to determine the presence of null values, empty strings, and encoded missing values.

    Parameters
    ----------
        df : pandas.DataFrame
            The dataset to be evaluated, imported via pandas' read_csv() function.
        test_params : pandas.DataFrame
            The test parameters that are either initialised by the Data Quality (DQ) tool or uploaded via pandas' read_csv() function.
        tests : dict
            A dictionary mapping test names to their relevant information and methods. It includes tests for null values, empty strings, and encoded missing values.

    Methods
    -------
        test_null(test)
            Counts the number of NULL values in specified columns of the dataset.
            
            Parameters
            ----------
            test : dict
                The test configuration.

        test_empty(test)
            Identifies empty strings in specified columns of the dataset.
            
            Parameters
            ----------
            test : dict
                The test configuration.

        test_na_strings(test)
            Detects strings that represent missing values, as defined in the test parameters, in specified columns of the dataset.

            Parameters
            ----------
            test : dict
                The test configuration, including the encoding used to represent missing data.

    """

    def __init__(self, df, test_params):
        # """
        # Initialises the Completeness object with a dataset and test parameters.
        
        # Parameters
        # ----------
        # df : pandas.DataFrame
        #     The dataset to be evaluated.
        # test_params : pandas.DataFrame
        #     The parameters defining how tests should be conducted.
        # """
        # Initialise the parent class with the input dataset and test parameters
        Dimension.__init__(self, df, test_params)
        # Dictionary of tests specific to completeness
        self.tests = {
            'Completeness_NULL': {'method': self.test_null, 'default': True},
            'Completeness_Empty': {'method': self.test_empty, 'default': True},
            'Completeness_Encoded': {'method': self.test_na_strings, 'default': False, 'arg1': 'Completeness_Encoded_Mapping'}
            }

    def test_null(self, test):
        # """
        # Executes a test for NULL values in the dataset.
        
        # Parameters
        # ----------
        # test : dict
        #     The test configuration.
        # """

        null_strings = {"NULL", "Null", "None"}

        def func(col, extra_args=None):
            # Returns a series indicating whether each value in the column is NA
            # return self.df[col].isna()
            return self.df[col].apply(lambda x: pd.isna(x) or str(x).strip() in null_strings)

        self.run_metric(test, func)

    def test_empty(self, test):
        # """
        # Executes a test for empty strings in the dataset.
        
        # Parameters
        # ----------
        # test : dict
        #     The test configuration.
        # """

        def func(col, extra_args=None):
            """
            Returns a pandas Series indicating whether each value in the specified column, 
            after stripping any leading and trailing whitespace, is an empty string.
            
            Parameters:
            col : str
                The name of the column to check for empty strings after stripping whitespace.
            
            Returns:
            pandas.Series
                A Series where True indicates the cell was empty (after whitespace removal),
                and False indicates it contained other characters.
            """
            # Strip leading and trailing whitespace and then check if the strings are empty
            return self.df[col].astype(str).str.strip().isin([''])

        self.run_metric(test, func)

    def test_na_strings(self, test):
        # """
        # Executes a test for encoded missing values (e.g., special strings that denote missing data) in the dataset.
        
        # Parameters
        # ----------
        # test : dict
        #     The test configuration, including the encoding used to represent missing data.
        # """
        
        def func(col, extra_args=None):
            # Splits the encoded missing values string and checks if the column values are in this list
             return self.df[col].apply(lambda x: str(x)).isin(self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item().split('|')) # corrected split to single pipe
        
        self.run_metric(test, func)


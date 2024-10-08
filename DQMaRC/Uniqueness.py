import pandas as pd
import numpy as np
from .Dimension import Dimension

class Uniqueness(Dimension):
    """
    A subclass of Dimension focused on evaluating the uniqueness of data within a dataset.
    
    This class performs uniqueness tests by identifying duplicate rows based on specified columns. It can be configured to check the entire row or a subset of columns for duplicates.
    
    Attributes
    ----------
    df : pandas.DataFrame
        The dataset to be evaluated, imported via pandas' read_csv() function.
    test_params : pandas.DataFrame
        The parameters defining how tests should be conducted, including which columns to consider for checking uniqueness.
    tests : dict
        A dictionary mapping test names to their relevant information and methods. Currently supports a row uniqueness test.
    
    Methods
    -------
    test_row_uniqueness(test)
        Identifies duplicate rows in the dataset based on the specified subset of columns.

        Parameters
        ----------
        test : str
            The name of the test to be executed.

    run_metric(test, func)
        Executes the given test function and updates the results attribute with the test's outcomes.

        Parameters
        ----------
        test : str
            The name of the test to be executed.
        func : callable
            The test function to execute.

    get_uniqueness_errors()
        Returns the results of uniqueness tests performed on the dataset.

        Returns
        -------
        pandas.DataFrame
            The results of the uniqueness tests, indicating duplicated rows based on the specified columns.
    """

    def __init__(self, df, test_params):
        # """
        # Initialises the Uniqueness object with a dataset and test parameters.
        
        # Parameters
        # ----------
        # df : pandas.DataFrame
        #     The dataset to be evaluated.
        # test_params : pandas.DataFrame
        #     The parameters defining how tests should be conducted.
        
        # Methods
        # -------
        # test_row_uniqueness(test)
        #     Checks if records are unique based on selected fields.
        # run_metric(test)
        #     Overrides the inherited run_metric method to execute a uniqueness test and capture its results.
        # get_uniqueness_errors(test)
        #     A method to return the DataFrame containing the results of uniqueness tests.

        # """
        Dimension.__init__(self, df, test_params)
        # Define the row uniqueness test with its default setting
        self.tests = {
            'Uniqueness_Rows': {'method': self.test_row_uniqueness, 'default': True}
            }

    def test_row_uniqueness(self, test):
        # """
        # Tests the dataset for row uniqueness based on specified columns.

        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed.
        # """
        def func(test):
            # Extract columns to check for uniqueness from the test parameters
            cols = self.test_params[self.test_params[test]==True]['Field'].to_list()
            # Ensure only columns present in the dataset are considered
            cols = [col for col in cols if col in self.df.columns]

            # Mark all duplicated rows; first occurrence is kept by default
            self.df.duplicated(keep=False, subset=cols)

            # Specifically mark the last occurrence of duplicated rows for identification
            return self.df.duplicated(keep='last', subset=cols).reset_index(name='row_uniqueness_|_full_row_uniqueness').drop('index', axis=1)

        self.run_metric(test, func)

    def run_metric(self, test, func):
        # """
        # Overrides the inherited run_metric method to execute a uniqueness test and capture its results.

        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed.
        # func : callable
        #     The test function to execute.
        # """
        try:
            result = func(test)
            result.name = test
            error_df = pd.DataFrame(result)
        except ValueError as e:
            print('Error in ' + test)
            print(e)
            error_df = pd.DataFrame(index=self.df.index)

        try:
            self.results = pd.merge(self.results, error_df,
                                    left_index=True, right_index=True)
        except TypeError as e:
            # Handles the initial case when self.results does not exist
            self.results = error_df

    def get_uniqueness_errors(self):
        # """
        # Returns the DataFrame containing the results of uniqueness tests.

        # Returns
        # -------
        # pandas.DataFrame
        #     The results of the uniqueness tests, indicating duplicated rows based on the specified columns.
        # """
        return self.results

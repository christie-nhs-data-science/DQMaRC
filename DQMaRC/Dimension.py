import pandas as pd
import numpy as np

class Dimension:
    """
    A base class for implementing data quality dimension checks on a pandas DataFrame.

    Attributes
    ----------
        df : pandas.DataFrame
            The dataset on which data quality checks will be performed.
        test_params : pandas.DataFrame
            A DataFrame specifying parameters for the data quality tests.
        results : pandas.DataFrame
            A DataFrame to store the results of data quality checks.
        tests : dict
            A dictionary mapping test names to their respective methods and other metadata.

    Methods
    -------
        run_metric(test, func):
            Executes a specific data quality check across all relevant columns in the dataset.
            
            Parameters
            ----------
            test : str
                The name of the test being executed.
            func : function
                A function that implements the logic for the data quality check.

        run_metrics():
            Iterates over and executes all configured data quality checks.
            
        get_results():
            Returns a copy of the results DataFrame with data quality check outcomes.
            
            Returns
            -------
            pandas.DataFrame
                A copy of the DataFrame containing the results of data quality checks, converted to integer data type.

        get_tests():
            Returns the dictionary of configured tests.
            
            Returns
            -------
            dict
                A dictionary of configured data quality checks.

        get_date_format():
            Returns the user-defined date format from the test parameters input.
    """

    def __init__(self, df, test_params):
        # """
        # Initialises the Dimension with a dataset and test parameters.

        # Parameters
        # ----------
        # df : pandas.DataFrame
        #     The dataset on which data quality checks will be performed.
        # test_params : pandas.DataFrame
        #     A DataFrame specifying parameters for the data quality tests.
        # """
        self.df = df
        self.test_params = test_params
        self.results = pd.DataFrame(index=df.index)
        self.tests = {}
        self.default_date_format = "%d/%m/%Y %H:%M:%S" # default date format

    def run_metric(self, test, func):
        # print(f"RUNNING {test}...")
        # """
        # Applies a specified function across columns of the DataFrame to perform a data quality check.

        # Parameters
        # ----------
        # test : str
        #     The name of the test being executed.
        # func : function
        #     A function that implements the logic for the data quality check.
        # """
        error_df = self.df[[]]
        # print(f"Initial empty error_df: {error_df}")

        for col in self.df.columns:
            dm_row = self.test_params[self.test_params['Field'] == col]
            try:
                if dm_row[test].item() == 1:
                    result = func(col)
                    # print(f"{test} result {col}: {result}", "\n") # debugging
                    result.name = test + '_|_' + col
                    # print("result BEFORE MERGE INSIDE run_metric: \n", result)
                    error_df = pd.merge(error_df, result, left_index=True, right_index=True)
                    # print("error_df AFTER MERGE INSIDE run_metric: \n", error_df)

            except ValueError as e:
                # print(f"ValueError in column {col} during {test}: {e}")
                print(e)

        # print(f"Error DataFrame after {test}: {error_df}") # debugging

        try:
            self.results = pd.merge(self.results, error_df,
                                    left_index=True, right_index=True,
                                    suffixes=('','_dup'))
            # print(f"Updated results after merging {test}: {self.results}") # debugging

        except TypeError as e:
            # print(f"TypeError during merging in {test}: {e}") # debugging
            self.results = error_df

    def run_metrics(self):
        # """
        # Executes all configured data quality checks for each dimension.
        # """
        for name, v in self.tests.items():
            # print(f"Running test: {name}") # for debugging
            v['method'](name)

    def get_results(self):
        # """
        # Returns a deep copy of the results DataFrame with outcomes of data quality checks.

        # Returns
        # -------
        # pandas.DataFrame
        #     A copy of the DataFrame containing the results of data quality checks, converted to integer data type.
        # """
        return self.results.copy(deep=True).astype('int64')

    def get_tests(self):
        # """
        # Retrieves the dictionary of tests configured for the data quality dimension.

        # Returns
        # -------
        # dict
        #     A dictionary of configured data quality checks.
        # """
        return self.tests

    def get_date_format(self, field_name):
        # """
        # Retrieves the date format for a given field name from the test parameters.
        # If the date format is not provided or is invalid, returns the default format.
        # """
        format_series = self.test_params.loc[self.test_params['Field'] == field_name, 'Date_Format']
        if format_series.empty or pd.isnull(format_series.values[0]):
            return self.default_date_format
        else:
            # print("format series not null:", format_series.values[0])
            print("format series not null:")

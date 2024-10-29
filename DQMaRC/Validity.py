import pandas as pd
from datetime import datetime
import re
from pkg_resources import resource_filename
from .Dimension import Dimension
# from Dimension import Dimension # for shinylive version
from pathlib import Path

class Validity(Dimension):
    """
    A subclass of Dimension focused on evaluating the validity of data within a dataset.
    
    This class performs various validity checks, including verifying NHS numbers, postcodes, future dates, date ranges, and ensuring data matches against specified lookup tables or falls within given numeric ranges.
    
    Attributes
    ----------
    df : pandas.DataFrame
        The dataset to be evaluated, imported via pandas' read_csv() function.
    test_params : pandas.DataFrame
        The parameters defining how tests should be conducted, including specifics like date formats, lookup table names, and numeric ranges for validity checks.
    date_format : str
        The format used for parsing dates within the dataset. This should match the actual date format for accurate comparisons.
    tests : dict
        A dictionary mapping test names to their relevant information and methods, supporting various types of validity checks.
    
    Methods
    -------
    test_nhs_numbers(test)
        Checks if NHS numbers in the dataset are valid according to the modulus 11 algorithm.

        Parameters
        ----------
        test : str
            The name of the test to be executed.
        
        The method checks if NHS numbers conform to the modulus 11 algorithm, marking them as valid or invalid accordingly.

    test_postcode(test)
        Validates the format of postcodes in the dataset using a regular expression.

        Parameters
        ----------
        test : str
            The name of the test to be executed, indicating the column to be checked for postcode validity.
        
        Uses a regular expression to match UK postcode formats. Postcodes that do not match the pattern are flagged as invalid.

    test_against_lookup_tables(test)
        Verifies if values in the dataset match against specified lookup tables.

        Parameters
        ----------
        test : str
            The name of the test to be executed, indicating the column and the associated lookup table for validation.
        
        The lookup table is expected to be a CSV file containing valid codes or values. Values not found in the lookup table are flagged as invalid.

    test_ranges(test)
        Checks if numeric values in the dataset fall within specified ranges.

        Parameters
        ----------
        test : str
            The name of the test to be executed, indicating the column and the numeric range for validation.
        
        The valid range is specified as two numbers separated by '||'. Values outside this range are flagged as invalid.

    validate_nhs_number(nhs_number)
        A helper method to validate a single NHS number using the modulus 11 algorithm.

        Parameters
        ----------
        nhs_number : str or int
            The NHS number to validate. It can be a string or integer; any spaces or non-numeric characters will be ignored.

        Returns
        -------
        bool
            Returns True if the NHS number is valid, otherwise False.

        Notes
        -----
        The method first checks for null or empty values, then verifies the length of the number. For a valid NHS number:
        - The sum of the products of the first 9 digits and their weights, subtracted from 11, should equal the 10th digit (check digit).
        - If the result of the subtraction is 11, it is replaced with 0 to match the check digit.
        - A result of 10 indicates an invalid NHS number.

    test_future_dates(test)
        Identifies dates in the dataset that are in the future relative to the current date.

        Parameters
        ----------
        test : str
            The name of the test to be executed, indicating the column to be checked for future dates.
        
        Dates that are beyond the current datetime are considered invalid for this test.

    min_max_dates(test)
        Validates if dates in the dataset fall within a specified minimum and maximum date range.

        Parameters
        ----------
        test : str
            The name of the test to be executed, indicating the column and the date range for validation.
        
        Dates outside the specified minimum and maximum range are flagged as invalid. The range is defined by 'min_date' and 'max_date' test parameters.

    test_pattern_validity(test)
        Checks if values conform to an expected user-specified pattern.

        Parameters
        ----------
        test : str
            The name of the test to be executed. It is expected that test_params will include
            the regex pattern for validation.

    """

    def __init__(self, df, test_params):
        # """
        # Initialises the Validity object with a dataset and test parameters.
        
        # Parameters
        # ----------
        # df : pandas.DataFrame
        #     The dataset to be evaluated.
        # test_params : pandas.DataFrame
        #     The parameters defining how tests should be conducted.
        # """

        Dimension.__init__(self, df, test_params)

        # Define various tests for validity checks
        self.tests = {
            'Validity_Dates_Future': {'method': self.test_future_dates, 'default': False},
            'Validity_Date_Range': {'method': self.min_max_dates, 
                                    'default': False, 
                                    'arg1': 'Validity_Date_Range_Min', 
                                    'arg2': 'Validity_Date_Range_Max'},
            'Validity_NHS_Number': {'method': self.test_nhs_numbers, 'default': False},
            'Validity_Postcode_UK': {'method': self.test_postcode, 'default': False},
            # 'Validity_Lookup_Table': {'method': self.test_against_lookup_tables, 
            #                           'default': False, 
            #                           'arg1': 'Validity_Lookup_Table_Filename'},
            'Validity_Lookup_Table': {'method': self.test_against_lookup_tables, 
                                      'default': False, 
                                      'arg1': 'Validity_Lookup_Type',
                                      'arg2': 'Validity_Lookup_Codes'},
            'Validity_Range': {'method': self.test_ranges, 'default': False, 'arg1': 'Validity_Range_Numeric'},
            'Validity_Pattern': {'method': self.test_pattern_validity, 'default': False, 'arg1': 'Validity_Pattern_Regex'}
            }
        
    def test_nhs_numbers(self, test):
        # """
        # Validates NHS numbers in a specified column of the dataset.
        
        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed.
        
        # The method checks if NHS numbers conform to the modulus 11 algorithm, marking them as valid or invalid accordingly.
        # """
        def func(col, extra_args=None):
            return ~self.df[col].apply(self.validate_nhs_number)

        self.run_metric(test, func)

    def test_postcode(self, test):
        # """
        # Validates the format of postcodes in a specified column against a UK postcode regular expression pattern.
        
        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed, indicating the column to be checked for postcode validity.
        
        # Uses a regular expression to match UK postcode formats. Postcodes that do not match the pattern are flagged as invalid.
        # """
        def func(col, extra_args=None):
            return ~self.df[col].fillna('').apply(
                lambda x: bool(re.search('^([A-Z]{1,2}\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})$', x.upper())))

        self.run_metric(test, func)

    # def test_against_lookup_tables(self, test):
    #     # """
    #     # Verifies if values in a specified column match against a predefined lookup table of valid values.
        
    #     # Parameters
    #     # ----------
    #     # test : str
    #     #     The name of the test to be executed, indicating the column and the associated lookup table for validation.
        
    #     # The lookup table is expected to be a CSV file containing valid codes or values. Values not found in the lookup table are flagged as invalid.
    #     # """
    #     def func(col, extra_args=None):
    #         lookup_name = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item()

    #         lookup_path = resource_filename('DQMaRC', f'data/lookups/{lookup_name}')
    #         lookup = pd.read_csv(lookup_path)


    #         lookup = lookup.rename({'Code2': 'Code'}, axis=1)
    #         return ~self.df[col].apply(lambda x: str(x).strip() in set(lookup['Code'].astype(str)))

    #     self.run_metric(test, func)

    def test_against_lookup_tables(self, test):
        def func(col, extra_args=None):
            # Retrieve the lookup type and codes (if any) from test parameters
            lookup_type = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item()
            lookup_codes = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg2']].item()

            if lookup_type == 'File':
                try:
                    # First path using resource_filename
                    infile = Path(__file__).parent / f'{lookup_codes}'
                    lookup = pd.read_csv(infile)
                except FileNotFoundError:
                    # Second path using the parent directory of the script
                    lookup_path = resource_filename('DQMaRC', f'data/lookups/{lookup_codes}')
                    lookup = pd.read_csv(lookup_path)

                # Extract valid codes from the first column
                valid_codes_set = set(lookup.iloc[:, 0].astype(str).str.strip())
                
            elif lookup_type == 'Values':
                # Split comma-separated codes into a set
                valid_codes_set = set(code.strip() for code in lookup_codes.split("|"))
            else:
                raise ValueError("Lookup type must be 'File' or 'Values'")

            # Apply validation by checking if each value is in the valid codes set
            return ~self.df[col].apply(lambda x: str(x).strip() in valid_codes_set)

        self.run_metric(test, func)

    def test_ranges(self, test):
        # """
        # Checks if numeric values in a specified column fall within a defined range.
        
        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed, indicating the column and the numeric range for validation.
        
        # The valid range is specified as two numbers separated by '||'. Values outside this range are flagged as invalid.
        # """
        def func(col, extra_args=None):
            # ranges = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item().split('||')
            ranges = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item().split('|') # to make consistent
            return self.df[col].apply(lambda x: float(x) < float(ranges[0]) or float(x) > float(ranges[1]))

        self.run_metric(test, func)

    def validate_nhs_number(self, nhs_number):
        # """
        # Validates an NHS number using the modulus 11 algorithm.

        # An NHS number is valid if it is 10 digits long, passes the modulus 11 check, and the last digit (check digit) matches the calculated result. The algorithm involves multiplying each of the first 9 digits by a weight, decreasing from 10 to 2, summing these products, and applying a modulus 11 operation.

        # Parameters
        # ----------
        # nhs_number : str or int
        #     The NHS number to validate. It can be a string or integer; any spaces or non-numeric characters will be ignored.

        # Returns
        # -------
        # bool
        #     Returns True if the NHS number is valid, otherwise False.

        # Notes
        # -----
        # The method first checks for null or empty values, then verifies the length of the number. For a valid NHS number:
        # - The sum of the products of the first 9 digits and their weights, subtracted from 11, should equal the 10th digit (check digit).
        # - If the result of the subtraction is 11, it is replaced with 0 to match the check digit.
        # - A result of 10 indicates an invalid NHS number.
        # """
        if pd.isna(nhs_number) or nhs_number.strip() == '':
            return False

        # number must be 10 digits long
        try:
            nhs_number = str(int(''.join(str(int(nhs_number)).split())))
            if len(nhs_number) != 10:
                return False

            l = [int(j) * (10 - (i)) for i, j in enumerate(nhs_number[:-1])]
            result = 11 - sum(l) % 11

            if result == 11:
                result = 0
            elif result == 10:
                return False

            return result == int(nhs_number[-1])
        
        except ValueError:
            print("Invalid input NHS Number: not a valid integer")
            return False
    
    def test_future_dates(self, test):
        # """
        # Identifies and flags dates in a specified column that are in the future relative to the current datetime.
        
        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed, indicating the column to be checked for future dates.
        
        # Dates that are beyond the current datetime are considered invalid for this test.
        # """

        def func(col, extra_args=None):
            date_format_field1 = self.get_date_format(col)
            def inner(x):
                try:
                    return pd.to_datetime(x, format=date_format_field1) > datetime.now()
                except (ValueError, TypeError):
                    return False
            return self.df[col].apply(inner)

        self.run_metric(test, func)

    def min_max_dates(self, test):
        # """
        # Validates if dates in a specified column fall within a given minimum and maximum date range.
        
        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed, indicating the column and the date range for validation.
        
        # Dates outside the specified minimum and maximum range are flagged as invalid. The range is defined by 'min_date' and 'max_date' test parameters.
        # """
        def func(col, extra_args=None):
            date_format_field1 = self.get_date_format(col)
            min_date = pd.to_datetime(self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item(), format=date_format_field1)
            max_date = pd.to_datetime(self.test_params[self.test_params['Field'] == col][self.tests[test]['arg2']].item(), format=date_format_field1)

            def inner(x):
                try:
                    # return (pd.to_datetime(x, format=self.date_format) < min_date) | (pd.to_datetime(x, format=self.date_format) > max_date)
                    return (pd.to_datetime(x, format=date_format_field1) < min_date) | (pd.to_datetime(x, format=date_format_field1) > max_date)
                except (ValueError, TypeError):
                    return False
            return self.df[col].apply(inner)

        self.run_metric(test, func)

    def test_pattern_validity(self, test):
        # """
        # Validates the format of data items in specified columns against a user-defined regex pattern.

        # Parameters
        # ----------
        # test : str
        #     The name of the test to be executed. It is expected that test_params will include
        #     the regex pattern for validation.
        # """
        def func(col, extra_args=None):
            # Fetch the regex pattern from test_params
            pattern = self.test_params[self.test_params['Field'] == col][self.tests[test]['arg1']].item()

            def check_pattern(value):
                # If value is NaN, treat it as valid (return False for no error)
                if pd.isna(value):
                    return False
                else:
                    try:
                # Return True for error (non-match) and False for no error (match)
                        return not bool(re.match(pattern, value))
                    except (ValueError, TypeError):
                        return False

            # Apply the pattern check across the column and return the result
            return self.df[col].apply(check_pattern)

        # Execute the function across the DataFrame
        self.run_metric(test, func)

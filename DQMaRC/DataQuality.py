import pandas as pd
import numpy as np
from functools import reduce
from datetime import datetime
from .Completeness import Completeness
from .Uniqueness import Uniqueness
from .Validity import Validity
from .Timeliness import Timeliness
from .Consistency import Consistency
from .Accuracy import Accuracy
import os

class DataQuality:
    """
    A class to assess and manage data quality across multiple dimensions for a given dataset.
    
    The class supports operations such as initialising the data quality dimension instances, preparing and aggregating results, 
    and writing out results to CSV files. It allows for both detailed error analysis and aggregate summaries.
    
    Attributes
    ----------
        df : pandas.DataFrame
            The dataset on which data quality checks are performed.
        test_params : pandas.DataFrame, optional
            A DataFrame specifying parameters for data quality tests. If not provided, default parameters are used.
        data_info : pandas.DataFrame
            Metadata information about the dataset fields and the timestamp of data quality assessment.
        completeness, validity, uniqueness, timeliness, consistency, accuracy : Object
            Instances of data quality dimension classes for performing specific checks.


    Methods
    -------

        raw_results(reduce_counts=False):
            Compiles detailed error information across all data quality dimensions.

            Parameters
            ----------
            reduce_counts : bool, optional
                If True, reduces error counts to boolean values (error present or not). Defaults to False.

            Returns
            -------
            pandas.DataFrame
                A DataFrame containing detailed error information for each record in the dataset.

        aggregate_rows(reduce_counts=False):
            Aggregates error counts by row for a high-level summary.

            Parameters
            ----------
            reduce_counts : bool, optional
                If True, reduces error counts to boolean values before aggregation. Defaults to False.
                
            Returns
            -------
            pandas.DataFrame
                A DataFrame with aggregated error counts by row.
            
        aggregate_results(reduce_counts=False):
            Creates a field and metric level aggregate summary of errors.

            Parameters
            ----------
            reduce_counts : bool, optional
                Indicates whether to reduce error counts to binary indicators (True for any errors, False for no errors). 
                Defaults to False, preserving actual count values.

            Returns
            -------
            pandas.DataFrame
                A DataFrame with aggregated error counts for each field and metric, sorted by field names as they appear 
                in the original dataset.

        results_prep(reduce_counts):
            Prepares error results from different data quality dimensions for further processing.

            Parameters
            ----------
            reduce_counts : bool
                If True, converts error counts to binary values (1 for error present, 0 for no error). Useful for simplifying error aggregation.

            Returns
            -------
            pandas.DataFrame
                A DataFrame containing merged error data from all data quality checks, with options for reduced counts.

            Notes
            -----
            Error data from each dimension is corrected for missing values based on completeness checks before merging. 
            This ensures that errors are accurately reflected even when data is missing.

        write_out(out, output_table):
            Writes the given DataFrame to a CSV file.

            Parameters
            ----------
            out : pandas.DataFrame
                The DataFrame to be written to a CSV file.
            output_table : str
                The name of the output file (excluding the file extension).

        get_test_params():
            Returns a copy of the test parameters being used.

            Returns
            -------
            pandas.DataFrame
                A DataFrame containing the test parameters for data quality dimensions.

        get_data():
            Returns a copy of the original dataset.

            Returns
            -------
            pandas.DataFrame
                The dataset that data quality checks are being performed on.

        set_test_params(test_params):
            Sets new test parameters for data quality checks and re-initialises dimension instances.

            Parameters
            ----------
            test_params : pandas.DataFrame
                A DataFrame specifying the new parameters for data quality tests.

        get_param_template():
            Generates a template DataFrame for specifying test parameters for each data quality dimension.

            Returns
            -------
            pandas.DataFrame
                A DataFrame serving as a template for specifying data quality test parameters.

        save_user_lookup(user_lookup, file_name):
            Saves a user-defined lookup table to a specified file.

            Parameters
            ----------
            user_lookup : pandas.DataFrame
                The user-defined lookup table to save.
            file_name : str
                The name of the file (excluding the file extension) to save the lookup table as.
                
        run_all_metrics():
            Executes all configured data quality checks across the dataset.
    """

    def __init__(self, df, test_params=None):
        # """
        # Initialises the DataQuality object with a dataset and optionally specified test parameters.
        
        # Parameters
        # ----------
        # df : pandas.DataFrame
        #     The dataset to perform data quality checks on.
        # test_params : pandas.DataFrame, optional
        #     A DataFrame specifying parameters for the data quality tests. If None, default parameters are used.
        # """

        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.df = df

        if test_params is None:
            print('Warning - Using default parameters. For best results edit parameters and reload using set_test_params() method')
            self.test_params = self.get_param_template()
        else:
            self.test_params = test_params

        self.data_info = pd.DataFrame({'field': df.columns, 'date_time': self.timestamp})
        self.completeness = Completeness(self.df, self.test_params)
        self.validity = Validity(self.df, self.test_params)
        self.uniqueness = Uniqueness(self.df, self.test_params)
        self.timeliness = Timeliness(self.df, self.test_params)
        self.consistency = Consistency(self.df, self.test_params)
        self.accuracy = Accuracy(self.df, self.test_params)

    def raw_results(self, reduce_counts=False):
        # """
        # Compiles and returns detailed error information across all data quality dimensions.
        
        # Parameters
        # ----------
        # reduce_counts : bool, optional
        #     If True, reduces error counts to boolean values (error present or not). Defaults to False.
            
        # Returns
        # -------
        # pandas.DataFrame
        #     A DataFrame containing detailed error information for each record in the dataset.
        # """
        out = self.results_prep(reduce_counts)
        return out

    def aggregate_rows(self, reduce_counts=False):
        # """
        # Aggregates error counts by row, providing a high-level summary of errors for each record.
        
        # Parameters
        # ----------
        # reduce_counts : bool, optional
        #     If True, reduces error counts to boolean values before aggregation. Defaults to False.
            
        # Returns
        # -------
        # pandas.DataFrame
        #     A DataFrame with aggregated error counts by row.
        # """

        raw = self.results_prep(reduce_counts)
        cols = [x.split('_|_')[0] for x in raw.columns]
        row_agg = raw.groupby(cols, axis=1).sum()[sorted(set(cols), key=cols.index)]
        row_agg['total_count'] = row_agg[[x for x in row_agg.columns if '_count' in x]].sum(axis=1)
        return row_agg

    def aggregate_results(self, reduce_counts=False):
        # """
        # Aggregates error counts across all data quality dimensions to produce a summarised view.

        # This method computes the sum of errors for each field and metric combination, facilitating a high-level analysis 
        # of data quality issues across the dataset. The output is structured to provide clear insight into which areas 
        # of the dataset may require further investigation or remediation.

        # Parameters
        # ----------
        # reduce_counts : bool, optional
        #     Indicates whether to reduce error counts to binary indicators (True for any errors, False for no errors). 
        #     Defaults to False, preserving actual count values.

        # Returns
        # -------
        # pandas.DataFrame
        #     A DataFrame with aggregated error counts for each field and metric, sorted by field names as they appear 
        #     in the original dataset.
        # """
        raw = self.results_prep(reduce_counts)
        out = raw.sum(skipna=False).reset_index(name='count').rename({'index': 'field_metric'}, axis=1)
        index = pd.MultiIndex.from_tuples([x.split('_|_') for x in out['field_metric']], names=['metric', 'field'])
        out = pd.DataFrame({'count': out['count'].to_list()}, index=index).unstack().T.reset_index().drop('level_0', axis=1)
        out = out.sort_values(by='field', key=lambda x: x.map({col: i for i, col in enumerate(self.df.columns)}))
        out = out[['field'] + list(dict.fromkeys([x.split('_|_')[0] for x in raw.columns]))]

        return out

    def results_prep(self, reduce_counts):
        # """
        # Prepares the data quality check results by merging errors from different dimensions and optionally reducing error counts.

        # This method combines error information from completeness, validity, uniqueness, timeliness, consistency, and accuracy checks. 
        # It provides an option to reduce error counts to binary values, facilitating easier identification of records with any errors.

        # Parameters
        # ----------
        # reduce_counts : bool
        #     If True, converts error counts to binary values (1 for error present, 0 for no error). Useful for simplifying error aggregation.

        # Returns
        # -------
        # pandas.DataFrame
        #     A DataFrame containing merged error data from all data quality checks, with options for reduced counts.

        # Notes
        # -----
        # Error data from each dimension is corrected for missing values based on completeness checks before merging. 
        # This ensures that errors are accurately reflected even when data is missing.
        # """
        
        # Aggregate error counts for each dimension, optionally reducing to binary values
        def count_errors(df, dimension, reduce_counts):
            try:
                df_overall = df.T.groupby([x.split('_|_')[1] for x in df.columns]).sum().T
                if reduce_counts:
                    df_overall.astype(bool).astype('Int64')
                df_overall.columns = [dimension + '_count_|_' + x for x in df_overall.columns]
                return df_overall
            except ValueError:
                return pd.DataFrame()

# ============ to correct completeness errors for comparison fields
        # Get fields that are compared with via consistency and timeliness metrics
        def get_related_fields(test_params):
            related_fields = {}
            for index, row in test_params.iterrows():
                if row['Consistency_Compare'] == True:
                    related_fields[row['Field']] = row['Consistency_Compare_Field']
                # Check for date relations and add to related fields if TRUE
                elif row['Consistency_Date_Relations'] == True:
                    related_fields[row['Field']] = row.get('Consistency_Date_Relations_Field', None)
                # Check for date relations and add to related fields if TRUE
                elif row['Timeliness_Date_Diff'] == True:
                    related_fields[row['Field']] = row.get('Timeliness_Date_Diff_Field', None)
                else:
                    pass
            return related_fields
        
        related_fields = get_related_fields(self.test_params)

        def correct_missing(col, comp, related_fields):
            field = col.name.split('_|_')[-1]
            corrections = []
            for x, y in zip(col, comp):
                # Correct the primary field
                primary_correction = 0 if field in y else x
                
                # Check and correct the related field if necessary
                related_field = related_fields.get(field)
                related_correction = 0 if related_field and related_field in y else primary_correction
                corrections.append(related_correction)
            return corrections

# ============

        error_dict = {'completeness': self.completeness.get_results(),
                      'uniqueness': self.uniqueness.get_results(),
                      'consistency': self.consistency.get_results(),
                      'timeliness': self.timeliness.get_results(),
                      'validity': self.validity.get_results(),
                      'accuracy': self.accuracy.get_results()}

        error_dict = {dimension: pd.merge(df, count_errors(df, dimension, reduce_counts), left_index=True, right_index=True, how='left')
                      for dimension, df in error_dict.items()}

        temp_completeness = Completeness(self.df, self.test_params)
        temp_completeness.run_metrics()
        completeness_overall = count_errors(temp_completeness.get_results(), 'completeness', reduce_counts)

        combined_completeness_errors = completeness_overall.apply(
            lambda row: [x.split('_|_')[-1] for x in row.index if row[x]], axis=1)

        # Apply the corrections across dimensions with the new correct_missing function
        for dimension in error_dict:
            if dimension != 'completeness': # do not apply correction to completeness dimension
                error_df = error_dict[dimension]
                error_dict[dimension] = error_df.apply(correct_missing, comp=combined_completeness_errors, related_fields=related_fields, axis=0)
            else:
                pass

        out = reduce(lambda x, y: pd.merge(x, y, left_index=True, right_index=True), error_dict.values())
        return out

    def write_out(self, out, output_table):
        # """
        # Writes the provided DataFrame to a CSV file in the specified output directory.
        
        # Parameters
        # ----------
        # out : pandas.DataFrame
        #     The DataFrame to be written to a CSV file.
        # output_table : str
        #     The name of the output file (excluding the file extension).
        # """

        print('writing to {}...'.format(output_table))
        out['date_time_created'] = datetime.now()
        out.to_csv(os.path.dirname(__file__) + '/../outputs/{}.csv'.format(output_table), index=False, encoding='UTF-8-sig')

    def get_test_params(self):
        # """
        # Returns a deep copy of the test parameters currently set for data quality checks.

        # Returns
        # -------
        # pandas.DataFrame
        #     A DataFrame containing the test parameters for data quality dimensions.
        # """
        return self.test_params.copy(deep=True)

    def get_data(self):
        # """
        # Returns a deep copy of the dataset currently being used for data quality checks.

        # Returns
        # -------
        # pandas.DataFrame
        #     The dataset that data quality checks are being performed on.
        # """
        return self.df.copy(deep=True)

    def set_test_params(self, test_params):
        # """
        # Sets new test parameters for data quality checks and re-initialises dimension instances with these parameters.

        # Parameters
        # ----------
        # test_params : pandas.DataFrame
        #     A DataFrame specifying the new parameters for data quality tests.
        # """
        self.test_params = test_params
        # Re-initialise data quality dimension instances with the new test parameters
        self.completeness = Completeness(self.df, self.test_params)
        self.validity = Validity(self.df, self.test_params)
        self.uniqueness = Uniqueness(self.df, self.test_params)
        self.timeliness = Timeliness(self.df, self.test_params)
        self.consistency = Consistency(self.df, self.test_params)
        self.accuracy = Accuracy(self.df, self.test_params)
        print('Using uploaded test parameters')

    def get_param_template(self):
        # """
        # Generates a template DataFrame for specifying test parameters for each data quality dimension.

        # The template includes default values and placeholder columns for arguments specific to each data quality test.

        # Returns
        # -------
        # pandas.DataFrame
        #     A DataFrame serving as a template for specifying data quality test parameters.
        # """
        rows = self.df.columns
        # Initialise instances to access default test parameters
        completeness = Completeness(self.df, None)
        uniqueness = Uniqueness(self.df, None)
        consistency = Consistency(self.df, None)
        timeliness = Timeliness(self.df, None)
        validity = Validity(self.df, None)
        accuracy = Accuracy(self.df, None)

        # Aggregate default parameters from all instances
        all_tests = {**completeness.tests,
                     **uniqueness.tests,
                     **consistency.tests,
                     **timeliness.tests,
                     **validity.tests,
                     **accuracy.tests}
        cols = {}
        for k, v in all_tests.items():
            cols[k] = [v['default']] * len(rows)
            try:
                cols[v['arg1']] = [np.nan] * len(rows)
            except KeyError:
                pass
            try:
                cols[v['arg2']] = [np.nan] * len(rows)
            except KeyError:
                pass

        # Create the Date_Format column with placeholders
        cols_date_format = {'Date_Format': ["" for _ in rows]} 

        # Create the DataFrame with 'Field' and 'Date_Format' as the first two columns, followed by other parameters
        df_template = pd.DataFrame({**{'Field': rows}, **cols_date_format, **cols})

        # reorder columns explicitly
        column_order = ['Field', 'Date_Format'] + [col for col in df_template.columns if col not in ['Field', 'Date_Format']]
        df_template = df_template[column_order]

        return df_template

    def save_user_lookup(self, user_lookup, file_name):
        # """
        # Saves a user-defined lookup table to the specified file within the lookups directory.

        # Parameters
        # ----------
        # user_lookup : pandas.DataFrame
        #     The user-defined lookup table to save.
        # file_name : str
        #     The name of the file (excluding the file extension) to save the lookup table as.
        # """

        user_lookup.to_csv(os.path.dirname(__file__) + file_name, index=False, encoding='utf-8-sig')

    def run_all_metrics(self):
        # """
        # Executes all configured data quality checks across the dataset using the current test parameters.
        # """
        self.completeness.run_metrics()
        self.uniqueness.run_metrics()
        self.consistency.run_metrics()
        self.timeliness.run_metrics()
        self.validity.run_metrics()
        self.accuracy.run_metrics()

def main():
    print("Running DQMaRC application")

if __name__ == "__main__":
    main()

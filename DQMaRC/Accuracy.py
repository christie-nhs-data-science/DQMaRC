from .Dimension import Dimension
import pandas as pd

class Accuracy(Dimension):
    """
    A subclass of Dimension focused on assessing the accuracy of a dataset against a predefined gold standard.
    
    This class performs accuracy tests by comparing data in the dataset against equivalent, trusted data in the gold standard.
    
    Parameters
    ----------
        df : pandas.DataFrame
            The dataset to be evaluated, imported via pandas' read_csv() function.
        test_params : pandas.DataFrame
            The parameters defining how tests should be conducted.
        gold_standard : pandas.DataFrame
            A DataFrame that serves as the gold standard for comparison. Must be set using the set_gold_standard method before running tests.
        tests : dict
            A dictionary mapping test names to their relevant information and methods. Currently supports a gold standard comparison test.
    
    Methods
    -------
        gold_standard_comparison(test)
            Compares the dataset against the gold standard for the specified columns.
            
            Parameters
            ----------
            test : dict
                The test configuration.

        set_gold_standard(gs)
            Sets the gold standard DataFrame against which the dataset will be compared.
            
            Parameters
            ----------
            gs : pandas.DataFrame
                The DataFrame to set as the gold standard.

    """

    def __init__(self, df, test_params):
        # """
        # Initialises the Accuracy object with a dataset and test parameters.
        
        # Parameters
        # ----------
        # df : pandas.DataFrame
        #     The dataset to be evaluated.
        # test_params : pandas.DataFrame
        #     The parameters defining how tests should be conducted.
        # """

        Dimension.__init__(self, df, test_params)
        # Define the gold standard comparison test with its default settings
        self.tests = {
            # 'gold_standard': {'method': self.gold_standard_comparison, 'default': False}
            'Accuracy_Gold_Standard': {'method': self.gold_standard_comparison, 'default': False}
            }

    def gold_standard_comparison(self, test):
        # """
        # Executes the gold standard comparison test for the specified columns in the dataset.
        
        # Parameters
        # ----------
        # test : dict
        #     The test configuration.
        # """

        def func(col):
            try:
                # Attempt to compare the dataset column to the gold standard column
                try:
                    return self.df[col].fillna('') != self.gold_standard[col].fillna('')
                except ValueError:
                # Handle cases where the dataset and gold standard dimensions don't match
                    print('!Warning! Data is larger than gold standand. Data has been subsetted to gold standard shape to calulate {} accuarcy'.format(col))
                    temp_df = self.df[col].iloc[self.gold_standard[col].index]
                    return temp_df.fillna('') != self.gold_standard[col].fillna('')
            except AttributeError:
                # Handle cases where the gold standard has not been set
                print('Gold standard not set for {0}. No comparison can be made'.format(col))
                # Return a comparison to self to maintain return type consistency, though it's not meaningful
                return self.df[col].fillna('') != self.df[col].fillna('')
            
        self.run_metric(test, func)

    def set_gold_standard(self, gs):
        # """
        # Sets the DataFrame to be used as the gold standard for accuracy comparisons.
        
        # Parameters
        # ----------
        # gs : pandas.DataFrame
        #     The DataFrame to set as the gold standard.
        # """

        self.gold_standard = gs


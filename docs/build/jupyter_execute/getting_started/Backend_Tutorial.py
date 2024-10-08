#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pkg_resources import resource_filename

# Import DQMaRC
from DQMaRC import DataQuality

# Import UtilitiesDQMaRC for data quality visualisation
from DQMaRC.UtilitiesDQMaRC import (
    MetricCalculator,
    BarPlotGenerator,
    DonutChartGenerator,
    overall_quality_fx, col_good, col_bad)


# In[2]:


# Read in example data as pandas dataframe
#df = pd.read_csv('../DQMaRC/data/toydf_subset.csv')
df = pd.read_csv(resource_filename('DQMaRC', 'data/toydf_subset.csv'))
df


# In[3]:


# Initialise a DQ object by passing your data to the tool
dq = DataQuality(df)

# Retrieve default test parameter form the object. We will edit this in the next step
test_params = dq.get_test_params()

# View the test parameters template
test_params


# In[4]:


# Datetime format
test_params.loc[test_params['Field']=='Date_of_Diagnosis', 'Date_Format'] = "%d/%m/%Y"
test_params.loc[test_params['Field']=='Date_of_Birth', 'Date_Format'] = "%d/%m/%Y"
test_params.loc[test_params['Field']=='Datetime_Event1', 'Date_Format'] = "%d/%m/%Y %H:%M"
test_params.loc[test_params['Field']=='Datetime_Logging1', 'Date_Format'] = "%d/%m/%Y %H:%M"

# Another way to do this:
# test_params.at[3,'Date_Format']="%d/%m/%Y" # Date of Diagnosis
# test_params.at[4,'Date_Format']="%d/%m/%Y" # Date of Birth
# test_params.at[15,'Date_Format']="%d/%m/%Y %H:%M" # Datetime_Event1
# test_params.at[16,'Date_Format']="%d/%m/%Y %H:%M" # Datetime_Logging1


# In[5]:


# Completeness
# Set to true for all fields
test_params['Completeness_NULL'] = True # Default value
test_params['Completeness_Empty'] = True # Default value

# Set Completeness Encoding only for the "Gender" column
test_params.at[2,'Completeness_Encoded']=True
test_params.at[2,'Completeness_Encoded_Mapping']='Unknown|Not Known|na' # use pipes for multiple possible codes for missingness


# In[6]:


# Uniqueness
# Set to true for all fields
test_params['Uniqueness_rows'] = True # Default value


# In[7]:


# Consistency
# Set up consistency checks between the "Metastatic_Indicator" and "Tumour_M_Stage" columns
test_params.loc[test_params['Field']=='Metastatic_Indicator', 'Consistency_Compare'] = True
test_params.loc[test_params['Field']=='Metastatic_Indicator', 'Consistency_Compare_Field'] = 'Tumour_M_Stage'
test_params.loc[test_params['Field']=='Metastatic_Indicator', 'Consistency_Compare_Mapping'] = '{["Absent"]: ["M0"], ["Present"]: ["M1", "M1a"]}'

# Set up consistency checks between date fields "Date_of_Birth" and "Date_of_Diagnosis"
test_params.loc[test_params['Field']=='Date_of_Birth', 'Consistency_Date_Relations'] = True
test_params.loc[test_params['Field']=='Date_of_Birth', 'Consistency_Date_Relations_Field'] = 'Date_of_Diagnosis'
test_params.loc[test_params['Field']=='Date_of_Birth', 'Consistency_Date_Relationship'] = '>' # i.e. raise an error if Date of Birth > Date of Diagnosis


# In[8]:


# Timeliness
# Raise an error if a time difference threshold of 10 minutes is exceeded
test_params.loc[test_params['Field']=='Datetime_Event1', 'Timeliness_Date_Diff'] = True
test_params.loc[test_params['Field']=='Datetime_Event1', 'Timeliness_Date_Diff_Field'] = 'Datetime_Logging1'
test_params.loc[test_params['Field']=='Datetime_Event1', 'Timeliness_Date_Diff_Threshold'] = '10' # i.e. raise an error if timediff >10 minutes


# In[9]:


# (1) Future Dates
test_params.loc[test_params['Field']=='Date_of_Diagnosis', 'Validity_Dates_Future'] = True
test_params.loc[test_params['Field']=='Date_of_Birth', 'Validity_Dates_Future'] = True


# In[10]:


# (2) Date Outliers
test_params.loc[test_params['Field']=='Date_of_Diagnosis', 'Validity_Date_Range'] = True
test_params.loc[test_params['Field']=='Date_of_Birth', 'Validity_Date_Range'] = True

test_params.loc[test_params['Field']=='Date_of_Diagnosis', 'Validity_Date_Range_Min'] = '2011-01-01'
test_params.loc[test_params['Field']=='Date_of_Birth', 'Validity_Date_Range_Min'] = '1900-01-01'

test_params.loc[test_params['Field']=='Date_of_Diagnosis', 'Validity_Date_Range_Max'] = '2023-07-07'
test_params.loc[test_params['Field']=='Date_of_Birth', 'Validity_Date_Range_Max'] = '2023-01-01'


# In[11]:


# (3) Numerical Outliers
test_params.loc[test_params['Field']=='Age', 'Validity_Range'] = True
test_params.loc[test_params['Field']=='Age', 'Validity_Range_Min'] = 0
test_params.loc[test_params['Field']=='Age', 'Validity_Range_Max'] = 120

test_params.loc[test_params['Field']=='Height_cm', 'Validity_Range'] = True
test_params.loc[test_params['Field']=='Height_cm', 'Validity_Range_Min'] = 20
test_params.loc[test_params['Field']=='Height_cm', 'Validity_Range_Max'] = 210


# In[12]:


# (4) NHS Number Validator
# test_params.loc[test_params['Field']=='NHS_Number', 'Validity_NHS_Number'] = True


# In[13]:


# (5) UK Postcode Validator
test_params.loc[test_params['Field']=='Postcode', 'Validity_Postcode_UK'] = True


# In[14]:


# (6a) Data Standards
#lu_filename_user_made = './data/lookups/LU_toydf_gender_user_made.csv'
lu_filename_user_made = 'LU_toydf_gender_user_made.csv'
# dq.save_user_lookup(pd.DataFrame({'Code': ['Male', 'Female']}), lu_filename_user_made)


# In[15]:


#(6b) Use an external csv data standard list of valid codes
lu_filename = '..DQMaRC/data/lookups/LU_toydf_gender.csv'

# Here we will apply a pre-defined data standard for "gender"
test_params.loc[test_params['Field']=='Gender', 'Validity_Lookup_Table'] = True
test_params.loc[test_params['Field']=='Gender', 'Validity_Lookup_Table_Filename'] = lu_filename


# In[16]:


# (7) Regular Expression Pattern
test_params.loc[test_params['Field']=='Datetime_Event1', 'Validity_Pattern'] = True
test_params.loc[test_params['Field']=='Datetime_Event1', 'Validity_Pattern_Regex'] = "(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2})"

test_params.loc[test_params['Field']=='Datetime_Event2', 'Validity_Pattern'] = True
test_params.loc[test_params['Field']=='Datetime_Event2', 'Validity_Pattern_Regex'] = "[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}"


# In[17]:


# Accuracy
# Set a manually validated version of the data set as the gold standard
test_params['Gold_Standard'] = True

# supply gold stand data - we are using the same dataset here for ease
dq.accuracy.set_gold_standard(df)


# In[18]:


# Read in example data as pandas dataframe
test_params_definitions = pd.read_csv('../DQMaRC/data/test_params_definitions.csv')
test_params_definitions


# In[19]:


test_params_upload = pd.read_csv(resource_filename('DQMaRC', 'data/toydf_subset_test_params_24.05.16.csv'))
test_params_upload


# In[20]:


dq.set_test_params(test_params_upload)


# In[21]:


dq.run_all_metrics()

# To run separately use following methods.
# dq.completeness.run_metrics()
# dq.uniqueness.run_metrics()
# dq.consistency.run_metrics()
# dq.timeliness.run_metrics()
# dq.validity.run_metrics()
# dq.accuracy.run_metrics()


# In[22]:


raw = dq.raw_results()
raw

# The full results can be joined to the source data by the index.
# source_df_raw = df.join(raw)


# In[23]:


agg = dq.aggregate_results()
agg


# In[24]:


# Prepare DQ Dashboard
raw_subset = raw.filter(regex='completeness|validity|consistency|uniqueness_count|accuracy|timeliness')
calculator = MetricCalculator(raw_subset)

# Simulate the calculation step, calculate aggregates
calculator.calculate_metrics()

summary_results = calculator.result
summary_results['Colour_Good'] = summary_results.apply(col_good, axis=1)
summary_results['Colour_Bad'] = summary_results.apply(col_bad, axis=1)
summary_results['Colour_NA'] = '#B2C3C6'

# Overall quality label
from IPython.display import HTML

# Function to display overall quality in a Jupyter Notebook
def display_overall_quality_label():
    if not summary_results.empty:
        data1 = summary_results[summary_results['Prop_NA'] == 0]
        avg_prop_good = data1['Prop_Good'].mean()
        overall_quality_level, background_color, text_colour = overall_quality_fx(avg_prop_good)

        overall_quality_text = f"Overall Quality: {overall_quality_level}"
        html = f"""
        <div style="
            background-color: {background_color};
            padding: 10px;
            border-radius: 5px;
            color: {text_colour};
            border: 2px solid {text_colour};
            text-align: center;
            width: 300px;">
            {overall_quality_text}
        </div>
        """
        return HTML(html)
    else:
        return HTML("<div style='text-align: center;'>No data available</div>")

# Use the function to display the result
display_overall_quality_label()


# In[25]:


DonutChartGenerator(summary_results).plot_donut_charts()


# In[26]:


BarPlotGenerator(summary_results, "completeness").plot_bar()


# In[27]:


BarPlotGenerator(summary_results, "consistency").plot_bar()


# In[28]:


BarPlotGenerator(summary_results, "timeliness").plot_bar()


# In[29]:


BarPlotGenerator(summary_results, "uniqueness").plot_bar()


# In[30]:


BarPlotGenerator(summary_results, "validity").plot_bar()


# In[31]:


# Join source data to the full DQ markup results
df_DQ_full = df.join(raw, how="left")


# In[32]:


gender_completeness_conditions = (df_DQ_full['Completeness_NULL_|_Gender']>0) | \
    (df_DQ_full['Completeness_Empty_|_Gender']>0) | \
        (df_DQ_full['Completeness_Encoded_|_Gender']>0)

df_DQ_full[['Gender','Completeness_NULL_|_Gender',
            'Completeness_Empty_|_Gender', 'Completeness_Encoded_|_Gender',
            'completeness_count_|_Gender']].loc[(gender_completeness_conditions)]


# In[33]:


# Check which rows have duplication where they should be unique
df_DQ_full[['Patient_ID', 'Gender']][df_DQ_full[['Patient_ID', 'Gender']].duplicated()]

# Show how uniqueness flags are shown
uniqueness_conditions = (df_DQ_full['Patient_ID']==1) | (df_DQ_full['Patient_ID']==10)

df_DQ_full[['Patient_ID', 'Gender',
            'row_uniqueness_|_full_row_uniqueness']].loc[(uniqueness_conditions)]


# In[34]:


consistency_conditions_metastatic_indicator = (df_DQ_full['Consistency_Compare_|_Metastatic_Indicator']>0)

df_DQ_full[['Tumour_M_Stage','Metastatic_Indicator',
            'Consistency_Compare_|_Metastatic_Indicator',
            'consistency_count_|_Metastatic_Indicator']].loc[(consistency_conditions_metastatic_indicator)]


# In[35]:


consistency_conditions_dates = (df_DQ_full['Consistency_Date_Relations_|_Date_of_Diagnosis']>0) | \
    (df_DQ_full['Consistency_Date_Relations_|_Date_of_Birth']>0)

df_DQ_full[['Date_of_Birth','Date_of_Diagnosis',
            'Consistency_Date_Relations_|_Date_of_Birth',
            'Consistency_Date_Relations_|_Date_of_Diagnosis']].loc[(consistency_conditions_dates)]


# In[36]:


timeliness_conditions = (df_DQ_full['Timeliness_Date_Diff_|_Datetime_Event2']>0)
df_DQ_full[['Datetime_Event2','Datetime_Logging2',
            'Timeliness_Date_Diff_|_Datetime_Event2',
            'timeliness_count_|_Datetime_Event2']].loc[(timeliness_conditions)]


# In[37]:


validity_future_dates_conditions = (df_DQ_full['Validity_Dates_Future_|_Date_of_Diagnosis']>0)
df_DQ_full[['Date_of_Diagnosis','Validity_Dates_Future_|_Date_of_Diagnosis']].loc[(validity_future_dates_conditions)]


# In[38]:


validity_outlier_dates_conditions = (df_DQ_full['Validity_Date_Range_|_Date_of_Diagnosis']>0)
df_DQ_full[['Date_of_Diagnosis','Validity_Date_Range_|_Date_of_Diagnosis']].loc[(validity_outlier_dates_conditions)]


# In[39]:


#validity_NHS_number_conditions = (df_DQ_full['Validity_NHS_Number_|_NHS_number']>0)
#df_DQ_full[['NHS_number','Validity_NHS_Number_|_NHS_number']].loc[(validity_NHS_number_conditions)]


# In[40]:


validity_UK_postcodes_conditions = (df_DQ_full['Validity_Postcode_UK_|_Postcode']>0)
df_DQ_full[['Postcode','Validity_Postcode_UK_|_Postcode']].loc[(validity_UK_postcodes_conditions)]


# In[41]:


validity_codes_conditions = (df_DQ_full['Validity_Lookup_Table_|_ICD_10_Code']>0)
df_DQ_full[['ICD_10_Code','Validity_Lookup_Table_|_ICD_10_Code']].loc[(validity_codes_conditions)]


# In[42]:


validity_numerical_ranges_conditions = (df_DQ_full['Validity_Range_|_Height_cm']>0)
df_DQ_full[['Height_cm','Validity_Range_|_Height_cm']].loc[(validity_numerical_ranges_conditions)]


# In[43]:


validity_pattern_conditions = (df_DQ_full['Validity_Pattern_|_Datetime_Event1']>0)
df_DQ_full[['Datetime_Event1','Validity_Pattern_|_Datetime_Event1']].loc[(validity_pattern_conditions)]


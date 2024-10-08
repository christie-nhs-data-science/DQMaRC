
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from itertools import product
from htmltools import TagList, tags
from shiny import ui

def overall_quality_fx(avg_prop_good):
    """
    Determines the overall quality level based on the average proportion of 'good' data.

    Parameters
    ----------
    avg_prop_good : float
        The average proportion (percentage) of 'good' quality data across all metrics.

    Returns
    -------
    str
        A string representing the overall quality level. 
        Possible values are "Outstanding", "Good", "Requires Improvement", or "Inadequate" with corresponding colours for background and text.
    """

    if avg_prop_good > 90:
        return ["Outstanding", "#a6cee3", "#1f78b4"]  # Light blue for Outstanding 
    elif avg_prop_good >= 80:
        return ["Good", "#b2df8a", "#33a02c"]  # Green for Good
    elif avg_prop_good >= 60:
        return ["Requires Improvement", "#fdbf6f", "#ff7f00"]  # Amber for Requires Improvement
    else:
        return ["Inadequate", "#fb9a99", "#e31a1c"]  # Red for Inadequate
    
class DonutChartGenerator:
    """
    A class for generating donut charts to visualise data quality metrics.

    Attributes
    ----------
    data : pandas.DataFrame
        The data containing quality metrics to be visualised.

    Methods
    -------
    plot_donut_charts()
        Generates a subplot of donut charts for each quality metric in the data.

        Returns
        -------
        plotly.graph_objs._figure.Figure
            A Plotly Figure object containing the subplot of donut charts.

            
    """

    def __init__(self, data):
        # """
        # Initialises the DonutChartGenerator with data.

        # Parameters
        # ----------
        # data : pandas.DataFrame
        #     The data containing quality metrics to be visualised.
        # """

        self.data = data

    def plot_donut_charts(self):
        # """
        # Generates and returns a subplot of donut charts for each unique quality metric in the data.

        # Returns
        # -------
        # plotly.graph_objs._figure.Figure
        #     A Plotly Figure object containing the subplot of donut charts.
        # """
        # Initialise variables and create subplot framework
        metrics = self.data['Metric'].unique()

        # create subplots
        fig = make_subplots(
            rows=1,
            cols=len(metrics),
            specs=[[{'type': 'domain'}] * len(metrics)],
            subplot_titles=metrics
        )

        for i, metric in enumerate(metrics, start=1):
            metric_data_copy = self.data.copy()
            metric_data = metric_data_copy[(metric_data_copy['Metric'] == metric) & (metric_data_copy['Prop_NA'] == 0)]
            avg_prop_good = round(metric_data['Prop_Good'].mean(), 2)
            avg_prop_bad = round(metric_data['Prop_Bad'].mean(), 2)

            marker_vals = dict(colors=metric_data[['Colour_Bad', 'Colour_Good']][:1].values.tolist()[0])

            fig.add_trace(
                go.Pie(
                    labels=['Bad', 'Good'],  # Updated labels
                    values=[avg_prop_bad, avg_prop_good],
                    title=f"{avg_prop_good}%",
                    titlefont_size=22,
                    hole=0.6,
                    textposition="none",
                    showlegend=False,
                    marker=marker_vals
                ),
                row=1, col=i
            )
            fig.update_traces(
                showlegend = False,
                hoverinfo = "label+value"
                )

        # Customising subplot titles to be bold and larger text size
        for i, ann in enumerate(fig.layout.annotations):
            fig.layout.annotations[i].font = dict(size=16, color="black", family="Arial, bold")
            fig.layout.annotations[i].text = ann.text.upper()  # Convert text to uppercase

        return fig

class BarPlotGenerator:
    """
    A class for generating bar plots to visualise data quality metrics for a chosen metric.

    Attributes
    ----------
    data : pandas.DataFrame
        The data containing quality metrics to be visualised.
    chosen_metric : str
        The metric for which to generate the bar plot.

    Methods
    -------
    plot_bar()
        Generates a bar plot for the chosen metric.

        Returns
        -------
        plotly.graph_objs._figure.Figure
            A Plotly Figure object containing the bar plot.

    """

    def __init__(self, data, chosen_metric):
        # """
        # Initialises the BarPlotGenerator with data and the chosen metric.

        # Parameters
        # ----------
        # data : pandas.DataFrame
        #     The data containing quality metrics to be visualised.
        # chosen_metric : str
        #     The metric for which to generate the bar plot.
        # """

        self.data = data
        self.chosen_metric = chosen_metric
    
    def plot_bar(self):
        # """
        # Generates and returns a bar plot for the chosen quality metric in the data.

        # Returns
        # -------
        # plotly.graph_objs._figure.Figure
        #     A Plotly Figure object containing the bar plot.
        # """
        
        # Filter the data based on the chosen metric and non-NA values
        metric_data = self.data[(self.data['Metric'] == self.chosen_metric) & (self.data['Prop_NA'] != 100)].copy()

        # Sort the filtered data
        metric_data.sort_values(by=['Prop_Good', 'Field'], inplace=True)
        
        # Generate the figure and add bar traces for Good, Bad, and NA proportions
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                name = "Good", 
                x = metric_data['Prop_Good'], 
                y = metric_data['Field'], 
                orientation='h',
                marker_color = metric_data['Colour_Good']
                )
            )
        fig.add_trace(
            go.Bar(
                name = "Bad", 
                x = metric_data['Prop_Bad'], 
                y = metric_data['Field'], 
                orientation='h',
                marker_color = metric_data['Colour_Bad']
                )
            )
        fig.add_trace(
            go.Bar(
                name = "NA", 
                x = metric_data['Prop_NA'], 
                y = metric_data['Field'], 
                orientation='h',
                marker_color = metric_data['Colour_NA']
                )
            )
        fig.update_layout(
            barmode = 'stack'
        )
        fig.update_traces(
            showlegend = False,
            hoverinfo = "name+x"
            )

        return fig

class MetricCalculator:
    """
    A class designed to calculate and compile data quality metrics from a provided dataset.

    Attributes
    ----------
    data : pandas.DataFrame
        The input dataset containing various quality metrics and fields.
    result : pandas.DataFrame
        A DataFrame initialised to store the calculated metrics, including counts and proportions of good, bad, and N/A data.

    Methods
    -------
    calculate_metrics()
        Calculates aggregate metrics for each field and metric combination present in the input data, updating the `result` attribute.
        
    """

    def __init__(self, data):
        # """
        # Initialises the MetricCalculator with the given dataset.

        # Parameters
        # ----------
        # data : pandas.DataFrame
        #     The input dataset from which data quality metrics will be calculated.
        # """

        self.data = data
        self.result = pd.DataFrame()

    def calculate_metrics(self):
        # """
        # Processes the input dataset to calculate aggregate metrics for each unique field and metric combination.

        # This method populates the `result` DataFrame with each field-metric combination's total count, and the proportion of good, bad, and N/A data. It relies on the naming convention in the dataset columns to identify and separate fields and metrics.

        # The resulting DataFrame is structured to provide a comprehensive overview of data quality across multiple dimensions.
        # """
        # Extract unique fields and metrics from the dataset's column names
        fields = set()
        metrics = set()

        for column in self.data.columns:
            parts = column.split('_count_|_')
            metric, field = parts[0], parts[1]
            fields.add(field)
            metrics.add(metric)

        # Initialise the result DataFrame with combinations of fields and metrics
        field_metric_pairs = list(product(fields, metrics))
        field_list, metric_list = zip(*field_metric_pairs)

        self.result['Field'] = field_list
        self.result['Metric'] = metric_list
        self.result['Count'] = 0
        self.result['Prop_Bad'] = 0.0
        self.result['Prop_Good'] = 0.0
        self.result['Prop_NA'] = 0.0

        # Fill in data quality metrics for each field-metric pair
        for index, row in self.result.iterrows():
            field = row['Field']
            metric = row['Metric']
            column_name = f'{metric}_count_|_{field}'

            if column_name in self.data.columns:
                prop_na = len(self.data) - self.data[column_name].count()

                if prop_na == len(self.data):
                    self.result.at[index, f'{metric}_count_|_{field}'] = np.nan
                else:
                    count = self.data[column_name].sum()
                    prop_bad = (count / len(self.data)) * 100
                    self.result.at[index, f'{metric}_count_|_{field}'] = count
                    self.result.at[index, f'Count'] += count
                    self.result.at[index, f'Prop_Bad'] += prop_bad
                    self.result.at[index, f'Prop_Good'] += 100 - prop_bad
                
                self.result.at[index, f'Prop_NA'] = (prop_na / len(self.data)) * 100
            
            else:
                self.result.at[index, f'Prop_NA'] = 100.0
        
        # Finalise the result DataFrame structure
        self.result = self.result[['Field', 'Metric', 'Count', 'Prop_Bad', 'Prop_Good', 'Prop_NA']]
        self.result.sort_values(by = ['Field','Metric'], inplace=True)
        self.result.drop_duplicates(subset=['Field', 'Metric'], inplace=True)
        self.result[['Prop_Bad', 'Prop_Good', 'Prop_NA']] = self.result[['Prop_Bad', 'Prop_Good', 'Prop_NA']].round(2)

def col_bad(row):
    """
    Assigns a color code to a data quality metric indicating a "bad" quality status.

    Parameters
    ----------
    row : pandas.Series
        A row from a DataFrame, expected to contain a 'Metric' column specifying the data quality metric.

    Returns
    -------
    str
        A hexadecimal color code associated with the "bad" quality status of the specified metric.

    Notes
    -----
    The function maps different data quality metrics to specific color codes, enhancing visual distinction in graphical representations.
    """
    # Define color mappings for various data quality metrics indicating "bad" status
    metric_color_map = {
        'completeness': '#a6cee3',
        'consistency': '#fb9a99',
        'timeliness': '#fdbf6f',
        'uniqueness': '#cab2d6',
        'validity': '#F49FA0',  # Updated color code from a commented-out alternative
        'accuracy': '#fb9a99'
    }
    # Default color if metric is not in the predefined list
    default_color = '#a6cee3'

    return metric_color_map.get(row['Metric'], default_color)

def col_good(row):
    """
    Assigns a color code to a data quality metric indicating a "good" quality status.

    Parameters
    ----------
    row : pandas.Series
        A row from a DataFrame, expected to contain a 'Metric' column specifying the data quality metric.

    Returns
    -------
    str
        A hexadecimal color code associated with the "good" quality status of the specified metric.

    Notes
    -----
    Similar to `col_bad`, this function provides a way to visually differentiate between various data quality metrics in graphical representations by mapping them to specific color codes for "good" quality status.
    """
    # Define color mappings for various data quality metrics indicating "good" status
    metric_color_map = {
        'completeness': '#1f78b4',
        'consistency': '#e31a1c',
        'timeliness': '#ff7f00',
        'uniqueness': '#6a3d9a',
        'validity': '#b15928',
        'accuracy': '#e31a1c'
    }
    # Default color if metric is not in the predefined list
    default_color = '#1f78b4'

    return metric_color_map.get(row['Metric'], default_color)

about_text = TagList(
    tags.h3("Welcome to the Data Quality Profiling Tool"),
    tags.p(
        """
        This is the front-end to a data quality 
        profiling tool that is built in python.
        It provides a suite of data quality tests across six dimensions, 
        including """, 
        tags.strong("Completeness"), ", ",
        tags.strong("Validity"), ", ",
        tags.strong("Uniqueness"), ", ",
        tags.strong("Timeliness"), ", ",
        tags.strong("Consistency"), " and " ,
        tags.strong("Accuracy"),".",
        style="""
        text-align: justify;
        word-break:break-word;
        hyphens: auto;
        """,
    ),
)

key_features_text = TagList(
    tags.h4("Key Features"),
    tags.strong("1) Comprehensive DQ Checks:"),
    "Dive deep into your data with checks across six critical dimensions of data quality.",
    tags.strong("2) Custom Test Parameters: "),
    "Tailor data quality checks to meet the unique needs of your dataset with customisable test parameters.",
    tags.strong("3) Aggregated Results Overview: "),
    "Gain a bird's-eye view of your data's quality through aggregated summaries and detailed error reporting.",
    tags.strong("4) Dynamic Test Configuration: "),
    "Easily configure and modify tests to adapt to your evolving data quality requirements.",
    tags.strong("5) Interactive Results Analysis: "),                
    "Explore error details with interactive reports that make pinpointing issues straightforward.",
)
get_started_text = TagList(
    tags.h4("Get Started"),
    tags.strong("1) Upload Your Dataset:"),
    "Begin by uploading a csv of the dataset you wish to analyse.",
    tags.strong("2) Set Your Test Parameters: "),
    "Customise your data quality checks by setting parameters tailored to your dataset's specific needs. You can do this by initialising a test parameter template based on your input dataset. ",
    tags.strong("3) Run Data Quality Checks: "),
    "Execute a comprehensive suite of tests across your dataset with just a click.",
    tags.strong("4) Analyse Results: "),
    "View aggregated summaries, explore detailed error reports, and make informed decisions to improve your data quality.",
)

error_input_df_text = TagList(
    ui.markdown(
        """
        No input dataset found. Please choose a **.csv** or **.xlsx** file.
        """
    )
)
error_test_params_text = TagList(
    ui.markdown(
        """
        No test parameters found. 
        Please choose your test parameters either by initialising them
        via the **"Initialise Parameters"** or by uploading a .csv or .xlsx 
        test parameters file via the **"Upload Parameters"** button.
        """
    )
)

error_metric_variable_choice_text = TagList(
    ui.markdown(
        """
        No errors were found for this combination of DQ metric and chosen variable.
        """
    )
)
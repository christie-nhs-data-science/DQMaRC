# ================
# === Packages ===
# ================
import sys
import pandas as pd

# === shiny packages === 
from shiny import App, reactive, render, ui
from shiny.types import FileInfo
from shiny import reactive
import asyncio

from shinywidgets import output_widget, render_widget, register_widget

# Conditional import of shinywidgets
if 'shiny' in sys.modules:
    from ipydatagrid import DataGrid, TextRenderer
    from shinywidgets import output_widget, render_widget, register_widget

from datetime import datetime

# === custom modules ===
from DQMaRC import DataQuality
from DQMaRC.UtilitiesDQMaRC import (
    MetricCalculator, 
    BarPlotGenerator, 
    DonutChartGenerator, 
    overall_quality_fx, col_good, col_bad,
    about_text, key_features_text, get_started_text, 
    error_input_df_text
)


# ==================================================================
# =============================== UI ===============================
# ==================================================================

app_ui = ui.page_fillable(
        ui.tags.head(
            # Custom CSS rules
            ui.tags.style("""
                .btn.action-button {
                    background-color: #a6cee3 !important; /* Light blue background */
                    color: #252525 !important; /* White text color */
                }
                .btn-file {
                    background-color: #a6cee3 !important; /* Light blue background */
                    color: #252525 !important; /* White text color */
                }
                /* Additional styles for hover effect */
                .btn-file:hover {
                    background-color: #95c8d8 !important; /* Slightly darker light blue on hover */
                }
                .shiny-download-link, .btn-default.shiny-download-link {
                    background-color: #a6cee3 !important; /* Light blue background */
                    color: #252525 !important; /* White text color */
                }
                /* Additional styles for hover effect */
                .shiny-download-link:hover, .btn-default.shiny-download-link:hover {
                    background-color: #95c8d8 !important; /* Slightly darker light blue on hover */
                }

            """)
        ),

    # Title
    ui.p(
        ui.strong(ui.h1(
            "DQMaRC: Data Quality Profiling",
            )
        ), 
    ),

    ui.navset_tab(

        # ==== tab 1. Welcome Page & Instructions ====
        ui.nav_panel(
            "1. Welcome",
            ui.card(
                about_text,
            ),
            # DQ Dims Explanatory Text
            ui.layout_column_wrap(
                ui.card(
                    key_features_text,
                ),
                ui.card(
                    get_started_text,
                ),
                width= 1 / 2
                ),
            ),

        # ==== tab 2. Data Upload ====
        ui.nav_panel(
            "2. Data Upload",
            ui.layout_column_wrap(
                ui.card(
                    ui.help_text("Upload your data here"),

                    # upload data 
                    ui.input_file(
                        id = "upload_data_file", 
                        label = "", 
                        button_label = "Browse",
                        accept=[".csv", ".xlsx"]
                        ),
                    ),
            ui.card(
                ui.help_text("Input Data Shape"),
                ui.output_ui("input_data_shape")),
            ),
            # view uploaded dataset
            ui.card(
                ui.output_data_frame("view_input_data"),
            )
        ),

        # ==== tab 3. Test Params =====
        ui.nav_panel(
            "3. Test Parameters",
            # test params action buttons
            ui.card(
                ui.layout_column_wrap(

                    #initialise test params
                    ui.input_action_button(
                        id = "initialise_params",
                        label = "Initialise Parameters",
                        class_="custom-class"
                    ),
                    
                    # upload test params
                    ui.input_file(
                        id = "upload_test_params_file", 
                        label = "", 
                        button_label = "Upload Parameters",
                        accept=[".csv", ".xls"]
                    ),

                    # download test params
                    ui.download_button(
                        id = "download_params",
                        label = "Download Parameters",
                        class_="custom-class"
                    ),
                )
            ),
              
            # test params table
            ui.card(
                output_widget("render_test_params"),
                # max_height="600px",
                class_="my-custom-card-class" # optional for future custom CSS classes
                ),
            ),
                
        # ==== tab 4. DQ Dashboard ====
        ui.nav_panel(
            "4. DQ Dashboard",

            ui.card(
                ui.input_action_button(id = "run_parameters", label = "Set and Run Parameters")
            ),
            
            ui.card(
                ui.panel_conditional(
                "input.choose_metric",

                # overall quality label
                ui.card(
                    ui.h2(ui.output_ui("overall_quality_label"))
                ),

                # donut
                ui.card(
                    output_widget("donutchart")
                ),

                # barplot + error records
                ui.layout_column_wrap(
                    # barplot
                    ui.card(
                        output_widget("barplot_chart"), full_screen=True),
                    
                    # DQ metric explanatory text
                    ui.card(ui.layout_column_wrap(
                        # choose a metric
                        ui.input_select(
                        id = "choose_metric",
                        label = "Choose a Dimension",
                        selected = None,
                        choices = []
                        ),
                        # choose a variable
                        ui.input_select(
                        id = "choose_variable",
                        label = "Choose a Variable",
                        selected = None,
                        choices = []
                        ), 
                        width = 1 / 2
                    ),
                        # filtered erroneous records
                        output_widget("error_records_datagrid"),
                        full_screen=True
                    ),
                    width = 1 / 2
                ),

                # Download results
                ui.card(
                    ui.layout_column_wrap(

                        # download full raw results
                        ui.download_button(
                            id = "download_full_results",
                            label = "Download Full Results",
                        ),

                        # download summary results
                        ui.download_button(
                            id = "download_summary_results",
                            label = "Download Summary Results",
                        )
                    ),
                ) # download results layout column wrap
            )
            ) # panel conditional
        ) # nav panel
    ) # navset tab
) # ui

# ==================================================================
# ============================= SERVER =============================
# ==================================================================

def server(input, output, session):
    """
    Defines the server logic for handling user inputs, processing data,
    and generating outputs for DQMaRC.

    Functions
    ---------
    handle_source_data_upload()
        Handles the upload of the source data file.
    show_error_input_df_text(df_input, id_num)
        Displays an error message if no dataset is found.
    input_data()
        Renders the uploaded DataFrame for viewing.
    input_data_shape_fx()
        Displays the shape of the uploaded DataFrame.
    initialise_test_params()
        Initialises test parameters based on the uploaded data.
    handle_test_params_upload()
        Handles the upload of test parameters file.
    initialise_DQ_tool()
        Initialises the DataQuality tool with the uploaded data.
    render_test_params()
        Renders the test parameters UI for editing.
    run_metrics()
        Runs the data quality metrics based on the test parameters.
    download_full_results()
        Downloads the full results of the DQ checks.
    download_summary_results()
        Downloads the summary results of the DQ checks.
    overall_quality_label_fx()
        Displays the overall quality label based on the summary results.
    donutchart_fx()
        Generates donut charts for the DQ metrics.
    barplot_chart_fx()
        Generates bar charts for the selected DQ metric.
    update_metric_choices()
        Updates the metric choices based on the summary results.
    update_variable_choices()
        Updates the variable choices based on the selected metric.
    display_error_records_fx()
        Displays the error records based on the selected metric and variable.
    """
    # global variables
    input_df_global = reactive.Value() # needed to set and run params
    test_params_global = reactive.Value() # needed to set and run params
    test_params_global_updated = reactive.Value() # updated test params global
    summary_results_global = reactive.Value()
    source_df_raw_global = reactive.Value()

    # ==================================
    # ========== Input Data ============
    # ==================================
    # Handle the upload of source data file
    @reactive.Effect
    @reactive.event(input.upload_data_file)
    def handle_source_data_upload():
        source_data_file = input.upload_data_file()
        if source_data_file:
            df_source_data = pd.read_csv(source_data_file[0]["datapath"], sep=",", na_filter=False)
            input_df_global.set(df_source_data)
            ui.notification_show("Input data successfully uploaded.", type='message')
        else:
            ui.notification_show("Please upload an input dataset CSV file.", type='error')

    #===================================
    def show_error_input_df_text(df_input, id_num):
        @output(id="{}".format(id_num))
        @render.text
        def error_input_df_fx():
            if df_input.empty: 
                # Display an error message if no dataset is found
                return error_input_df_text
            else:
                pass

    #===================================
    @output(id="view_input_data")
    @render.data_frame
    def input_data():
        """
        Renders the DataFrame created from the uploaded file for viewing, or an error message if no data is available.
        """
        df = input_df_global()
        show_error_input_df_text(df, "error_input_df")
        return df

    #===================================
    @output(id="input_data_shape")
    @render.text
    def input_data_shape_fx():
        """
        Displays the shape of the uploaded DataFrame.
        """
        df = input_df_global()
        if df.empty:
            return error_input_df_text
        else:
            out_shape_text = f"Rows: {df.shape[0]}, Columns: {df.shape[1]}"
            return out_shape_text

    # ==================================
    # ========= TEST PARAMS ============
    # ==================================
    # you can have one of two test params csv/df's: default or pre-defined (upload)
    # test_params (TP) = None else default else uploaded_TP
    # Initialise or Upload Test Params
    @reactive.Effect
    @reactive.event(input.initialise_params)
    def initialise_test_params():
        df_input = input_df_global()
        if df_input is not None and not df_input.empty:
            dq_tool = DataQuality(df_input)
            test_params_df = dq_tool.get_test_params()
            test_params_global.set(test_params_df)
            test_params_global_updated.set(test_params_df)
            ui.notification_show("Test parameters initialised.", type='message')
        else:
            ui.notification_show("Please upload an input dataset before initialising parameters.", type='error')

    # Handle the upload of test parameters file
    @reactive.Effect
    @reactive.event(input.upload_test_params_file)
    def handle_test_params_upload():
        file = input.upload_test_params_file()
        if file:
            df = pd.read_csv(file[0]["datapath"])
            test_params_global.set(df)
            test_params_global_updated.set(df)
            ui.notification_show("Test parameters file uploaded successfully.", type='message')
        else:
            ui.notification_show("Please select a test parameters file to upload.", type='error')

    # initialise DQ tool
    @reactive.Calc
    @reactive.event(input.initialise_params, input.run_parameters)
    def initialise_DQ_tool():
        df = input_df_global()
        if df is None or df.empty:
            # Show notification if no data is uploaded
            ui.notification_show(
                ui.tags.div("Please upload an input dataset"),
                type='error', 
                duration=5  # Adjust duration as needed
            )
        else:
            try:
                dq = DataQuality(df)
                return dq
            except Exception as e:
                print("!! error in initialise DQ tool")
    
    # render editable test parameters 
    @render_widget
    @reactive.event(input.initialise_params, input.upload_test_params_file)
    def render_test_params():
        """
        Renders the test parameters UI allowing for editing and interaction.
        """
        try:
            test_params = test_params_global()
            test_params = DataGrid(
                test_params, 
                editable=True, 
                header_visibility='column',
                base_column_size = 180,
                base_column_header_size = 30,
                header_renderer=TextRenderer(background_color='lightblue'),
                grid_style={"header_background_color": "lightblue"}  
                )
            register_widget("params_table", test_params)

            # Create a reactive value for tracking cell changes
            cell_changes = reactive.Value()

            def on_cell_changed(cell):
                cell_changes.set(str(cell))
                test_params_global_updated.set(test_params.get_visible_data()) 

            # register cell change callback
            test_params.on_cell_change(on_cell_changed)

            # download test parameters
            @render.download(filename=f"{datetime.now().strftime('%Y-%m-%d %H.%M.%S')}_test_params.csv", encoding='UTF-8-sig')
            def download_params():
                yield test_params.get_visible_data().to_csv(index=False)

            return test_params
        
        except Exception as e:
            ui.notification_show(
                ui.tags.div("Error in render_test_params."),
                type='error', 
                duration=5  # Adjust duration as needed
            )

    # ======================================
    # ====== set & run current params ======
    # this is for checking test params output in raw table output position
    # Set and Run Test Parameters
    @reactive.Effect
    @reactive.event(input.run_parameters)
    async def run_metrics():
        df_input = input_df_global()
        # Call the function once and use the result multiple times
        updated_params = test_params_global_updated()

        # Check if updated_params is None or empty, and use a default if so
        df_params = updated_params if updated_params is not None and not updated_params.empty else test_params_global()

        if df_input is None or df_input.empty:
            ui.notification_show("Please upload an input dataset before running tests.", type='error')

        if df_params is None or df_params.empty:
            ui.notification_show("Please initialise or upload test parameters before running them.", type='error')

        try:
            # Proceed with running metrics...
            with ui.Progress(min=1, max=8) as progress:  # Adjust the max value based on the number of steps
                progress.set(message="(1/8) Initialising test parameters.")
                await asyncio.sleep(0.5)  # Wait for 1 second

                # Simulate processing steps with progress updates
                progress.inc(message="(2/8) Test parameters loaded.")
                await asyncio.sleep(0.5)  # Wait for 1 second

                dq = initialise_DQ_tool()
                progress.inc(message="(3/8) Data Quality tool initialised.")
                await asyncio.sleep(0.5)  # Wait for 1 second

                dq.set_test_params(df_params)
                progress.inc(message="(4/8) Test parameters set.")
                await asyncio.sleep(0.5)  # Wait for 1 second
                
                # Simulate the metrics computation step
                dq.run_all_metrics()
                progress.inc(message="(5/8) Running metrics.")
                await asyncio.sleep(0.5)  # Wait for 1 second
                
                # raw results joined to source/input df
                raw = dq.raw_results()
                source_df_raw = input_df_global().join(raw)
                source_df_raw_global.set(source_df_raw)

                # prepare results for DQ dashboard, first by subsetting final sums/counts of DQ dimensions
                raw_subset = raw.filter(regex='completeness|validity|consistency|uniqueness_count|accuracy|timeliness')
                calculator = MetricCalculator(raw_subset)
                progress.inc(message="(6/8) Calculating results.")
                await asyncio.sleep(0.5)  # Wait for 1 second
                
                # Simulate the calculation step, calculate aggregates
                calculator.calculate_metrics()
                progress.inc(message="(7/8) Finalising calculation.")
                await asyncio.sleep(1)  # Wait for 1 second
                
                summary_results = calculator.result
                summary_results['Colour_Good'] = summary_results.apply(col_good, axis=1)
                summary_results['Colour_Bad'] = summary_results.apply(col_bad, axis=1)
                summary_results['Colour_NA'] = '#B2C3C6'
                summary_results_global.set(summary_results)

                progress.inc(message="(8/8) Results ready.")
                await asyncio.sleep(2)  # Wait for 1 second
                
                # update set parameters input action button to "Rerun..."
                ui.update_action_button("run_parameters", label="Re-run Test Parameters")

                # Finish progress
                progress.close()
            # Simulate a long-running operation
            await asyncio.sleep(2)
            ui.notification_show("Metrics computation completed successfully.", type='message')
            # Update UI elements or global state as necessary
        except Exception as e:
            ui.notification_show(f"An error occurred while running metrics: {e}", type='error')

    # ======================================
    # ======= DOWNLOAD Full Results ========
    @render.download(
            filename=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_full_results.csv"
    )
    def download_full_results():
        yield source_df_raw_global().to_csv(index=False)

    # ======================================
    # ====== DOWNLOAD Summary Results ======
    @render.download(
            filename=f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_summary_results.csv"
    )
    def download_summary_results():
        yield summary_results_global()[['Field', 'Metric', 'Count','Prop_Bad','Prop_Good','Prop_NA']].to_csv(index=False)

    # ===================================
        
    # overall DQ label
    @output(id="overall_quality_label")
    @render.ui
    def overall_quality_label_fx():
        data = summary_results_global()
        if not data.empty:
            data1 = data[data['Prop_NA'] == 0]
            avg_prop_good = data1['Prop_Good'].mean()
            overall_quality_level = overall_quality_fx(avg_prop_good)[0]
            background_color = overall_quality_fx(avg_prop_good)[1]
            text_colour = overall_quality_fx(avg_prop_good)[2]
            overall_quality_text = f"Overall Quality: {overall_quality_level}"

            return ui.tags.div(
                overall_quality_text,
                style=f"""
                    background-color: {background_color}; 
                    padding: 10px; 
                    border-radius: 5px; 
                    color: {text_colour}; 
                    border: 2px solid {text_colour};
                    text-align: center;"""
            )
        else:
            # Fallback content if data is empty
            return ui.tags.div("No data available", style="text-align: center;")

    #===================================
    # Donut charts
    @output(id="donutchart")
    @render_widget
    def donutchart_fx():
        data = summary_results_global()
        if data is not None:
            return DonutChartGenerator(data).plot_donut_charts()
  
    #===================================
    # bar chart
    @output(id="barplot_chart")
    @render_widget
    def barplot_chart_fx():
        data = summary_results_global()
        if data is not None:
            metric = input.choose_metric()
            return BarPlotGenerator(data, metric).plot_bar()

# =============================
    @reactive.Effect
    def update_metric_choices():
        summary_results = summary_results_global()
        if summary_results is not None and not summary_results.empty:
            metrics = summary_results['Metric'].unique().tolist()
            ui.update_select("choose_metric", choices=metrics)

    @reactive.Effect
    def update_variable_choices():
        summary_results = summary_results_global()
        selected_metric = input.choose_metric()
        if summary_results is not None and not summary_results.empty and selected_metric:
            # Filter summary_results to exclude rows where Prop_NA == 100 for the selected metric
            valid_fields = summary_results[(summary_results['Metric'] == selected_metric) & (summary_results['Prop_NA'] != 100)]['Field'].unique().tolist()
            ui.update_select("choose_variable", choices=valid_fields)

    def get_unique_variables_message(test_params):
        unique_variables = test_params[test_params["Uniqueness_Rows"] == True]["Field"].to_list()
        if unique_variables:
            return pd.DataFrame({"Variables Included": unique_variables})
        return pd.DataFrame({"Message": ["No unique variables found"]})
    
    def get_consistency_comparison(full_results, test_params, selected_variable, error_column):
        # Check if the selected variable exists in the test_params table
        if selected_variable not in test_params["Field"].values:
            return pd.DataFrame({"Message": [f"Variable '{selected_variable}' not found in test parameters"]})
        
        test_param_row = test_params[test_params["Field"] == selected_variable].iloc[0]
        
        # Determine which comparison approach to use
        if test_param_row["Consistency_Compare"] == True:
            compare_variable = test_param_row["Consistency_Compare_Field"]
        elif test_param_row["Consistency_Date_Relations"] == True:
            compare_variable = test_param_row["Consistency_Date_Relations_Field"]
        elif test_param_row["Timeliness_Date_Diff"] == True:
            compare_variable = test_param_row["Timeliness_Date_Diff_Field"]
        else:
            return pd.DataFrame({"Message": ["Neither Consistency_Compare nor Consistency_Date_Relations is set to True for selected variable"]})
        
        # Check for NA values in compare_variable
        if pd.isna(compare_variable):
            return pd.DataFrame({"Message": ["Comparison variable not found or is NA"]})
        
        # Ensure selected_variable and, if applicable, compare_variable exist in the full_results
        # if selected_variable not in full_results.columns or (compare_variable not in full_results.columns and compare_variable != "Consistency_Date_Relations"):
        if selected_variable not in full_results.columns or compare_variable not in full_results.columns:
            return pd.DataFrame({"Message": ["Selected or comparison variable not found in data"]})
        
        # Ensure the error column exists in full_results
        if error_column not in full_results.columns:
            return pd.DataFrame({"Message": ["Error column not found in data"]})
              
        # Proceed with comparison for other cases
        error_records = full_results[full_results[error_column] > 0]
        relevant_data = error_records[[selected_variable, compare_variable, error_column]]
        if error_records.empty:
            return pd.DataFrame({"Message": ["No errors found"]})

        if relevant_data.empty:
            return pd.DataFrame({"Message": ["No relevant data found for consistency comparison"]})
        
        aggregated_data = relevant_data.groupby([selected_variable, compare_variable]).size().reset_index(name='Count')
        if aggregated_data.empty:
            return pd.DataFrame({"Message": ["No consistency errors found between variables"]})
        
        aggregated_data_sorted = aggregated_data.sort_values(by="Count", ascending=False)
        return aggregated_data_sorted

    def get_error_records(full_results, selected_variable, error_column):
        error_records = full_results[full_results[error_column] > 0]
        if error_records.empty:
            return pd.DataFrame({"Message": ["No errors found"]})
        aggregated_errors = error_records.groupby(selected_variable)[error_column].agg('count').reset_index()
        aggregated_errors_renamed = aggregated_errors.rename(columns={error_column: "Count"})
        return aggregated_errors_renamed.sort_values(by="Count", ascending=False)

    def display_filtered_errors():
        full_results = source_df_raw_global()
        test_params = test_params_global()
        selected_metric = input.choose_metric()
        selected_variable = input.choose_variable()
        error_column = f"{selected_metric.lower()}_count_|_{selected_variable}"

        if selected_metric == "uniqueness":
            return get_unique_variables_message(test_params)

        elif selected_metric == "consistency" or selected_metric == "timeliness":
            return get_consistency_comparison(full_results, test_params, selected_variable, error_column)

        if full_results is not None and not full_results.empty and selected_metric and selected_variable:
            if error_column in full_results.columns:
                return get_error_records(full_results, selected_variable, error_column)
            return pd.DataFrame({"Message": ["Error column not found"]})

        return pd.DataFrame({"Message": ["Please select both metric and variable"]})

    @output(id="error_records_datagrid")
    @render_widget
    def display_error_records_fx():
        data = display_filtered_errors()
        data_datagrid = DataGrid(
            data, 
            header_visibility='all',
            base_column_header_size = 50,
            auto_fit_columns = True,
            selection_mode = 'cell',
            header_renderer=TextRenderer(background_color='lightblue'),
            grid_style={"header_background_color": "lightblue"}
            )
        return data_datagrid    

app = App(app_ui, server)

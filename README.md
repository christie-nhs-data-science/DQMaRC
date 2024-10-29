# DQMaRC: A Python Tool for Structured Data Quality Profiling

**Version:** 1.0.0  
**Author:** Anthony Lighterness and Michael Adcock  
**License:** MIT License and Open Government License v3

[![Project Status: Suspended – Initial development has started, but there has not yet been a stable, usable release; work has been stopped for the time being but the author(s) intend on resuming work.](https://www.repostatus.org/badges/latest/suspended.svg)](https://www.repostatus.org/#suspended)

---

## Overview

**DQMaRC** (Data Quality Markup and Ready-to-Connect) is a Python tool designed to facilitate comprehensive data quality profiling of structured tabular data. It allows data analysts, engineers, and scientists to systematically assess and manage the quality of their datasets across multiple dimensions including completeness, validity, uniqueness, timeliness, consistency, and accuracy.

DQMaRC can be used both programmatically within Python scripts and interactively through a Shiny web application front-end user interface, making it versatile for different use cases ranging from ad-hoc analysis to integration within larger data pipelines.

## Key Features

- **Multi-dimensional Data Quality Checks:** Evaluate datasets across key dimensions including Completeness, Validity, Uniqueness, Timeliness, Consistency, and Accuracy.
- **Customisable Test Parameters:** Configure data quality test parameters easily via python or a user friendly spreadsheet to tailor your data quality assessment to your dataset.
- **Interactive Shiny App:** Setup, run, explore and visualise data quality issues interactively through a Shiny app for Python.
- **Integration with Data Pipelines:** Easily integrate DQMaRC into your data processing pipelines for scheduled data quality checks.
- **Detailed Reporting:** Generate comprehensive reports detailing data quality issues at both the cell and aggregate levels.

## Installation

### Using Pip or Conda

You can install DQMaRC using pip or conda. Ensure you have a virtual environment activated.

```bash
pip DQMaRC
```

```bash
conda install DQMaRC
```

### Dependencies

The package dependencies are listed in the `requirements.txt` file and will be installed automatically during the installation of DQMaRC.

## Getting Started

### 1. Import Libraries

Start by importing the necessary libraries and DQMaRC modules in your Python environment.

```python
import pandas as pd
from DQMaRC import DataQuality
```

### 2. Load Your Data

Load the dataset you wish to profile.

```python
# Load your data
df = pd.read_csv('path_to_your_data.csv')
```

### 3. Initialise DQMaRC and Set Test Parameters

Initialise the DQ tool and set the test parameters. You can generate a template or import predefined parameters.

```python
# Initialise the Data Quality object
dq = DataQuality(df)

# Generate test parameters template
test_params = dq.get_param_template()

# (Optional) Load pre-configured test parameters
# test_params = pd.read_csv('path_to_test_parameters.csv')

# Set the test parameters
dq.set_test_params(test_params)
```

### 4. Run Data Quality Checks

Run the data quality checks across all dimensions.

```python
dq.run_all_metrics()
```

### 5. Retrieve and Save Results

Retrieve the full results and join them with your original dataset for detailed analysis.

```python
# Get the full results
full_results = dq.raw_results()

# Join results with the original dataset
df_with_results = df.join(full_results, how="left")

# Save results to a CSV file
df_with_results.to_csv('path_to_save_results.csv', index=False)
```

## Using the Shiny App

In addition to programmatic usage, DQMaRC includes an interactive Shiny web app for Python that allows users to explore and visualise data quality issues.

You can test the DQMaRC ShinyLive Demo by copying and pasting the URL located [HERE](https://github.com/christie-nhs-data-science/DQMaRC/blob/main/DQMaRC_ShinyLiveEditor_link) into your webbrowser. This link will take you to a ShinyLive Editor where you can test the DQMaRC functionality. If you encounter an error, try refreshing the webpage once or twice. If you still encounter an error after this, please feel free to get in touch by contacting us or raising an issue on our repository.

**PLEASE NOTE**
The ShinyLive UI is recommended only for **testing** and getting used to the DQMaRC too functionality. This interface is deployed on your machine, meaning it is only as secure as your machine is. It will store data you upload in its local memory before being wiped when you exit the app.

### Running the Shiny App

To run the Shiny app, use the following command in your terminal:

```bash
shiny run --reload --launch-browser path_to_your_app/app.py
```

### Deploying the Shiny App

For deploying the Shiny app on a server, follow the [official Shiny for Python deployment guide](https://shiny.posit.co/py/docs/install-create-run.html).

## Documentation

Comprehensive documentation for DQMaRC, including detailed API references and user guides, is available [HERE](https://christie-nhs-data-science.github.io/DQMaRC/) or in the project `docs/` directory.

## Repo Structure
### Top-level Structure

```

DQMaRC	
│   requirements.txt 			# package dependencies
│   setup.py	 			# setup configuration for the python package distribution
│       
├───docs	 			# user docs material
│   │...   
│           
├───DQMaRC  				# source code
│   │   Accuracy.py
│   │   app.py
│   │   Completeness.py
│   │   Consistency.py
│   │   DataQuality.py
│   │   Dimension.py
│   │   Timeliness.py
│   │   Uniqueness.py
│   │   UtilitiesDQMaRC.py
│   │   Validity.py
│   │   __init__.py
│   │   
│   ├───data	 			# data used in the tutorial(s)
│   │   │   DQ_df_full.csv
│   │   │   test_params_definitions.csv
│   │   │   toydf_subset.csv
│   │   │   toydf_subset_test_params_24.05.16.csv
│   │   │   
│   │   └───lookups	 		# data standards and or value lists for data validity checks
│   │           LU_toydf_gender.csv
│   │           LU_toydf_ICD10_v5.csv
│   │           LU_toydf_M_stage.csv
│   │           LU_toydf_tumour_stage.csv
│   │           
│   ├───notebooks	
│   │      Backend_Tutorial.ipynb   	# Tutorial for python users
│...

```

## Contributing

Contributions to DQMaRC are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines on how to contribute to this project.

## License

DQMaRC is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

This project was developed by Anthony Lighterness and Michael Adcock. Special thanks to all contributors and testers who helped in the development of this tool.

## Citation

Please use the following citation if you use DQMaRC:

Lighterness, A., Adcock, M.A., and Price, G. (2024). DQMaRC: A Python Tool for Structured Data Quality Profiling (Version 1.0.0) [Software]. Available from https://github.com/christie-nhs-data-science/DQMaRC.

## Notice on Maintenance and Support

Please Note: This library is an open-source project maintained by a small team of contributors. 
While we strive to keep the package updated and well-maintained, ongoing support and development may vary depending on resource availability.

We strongly encourage users to engage with the project by reporting any issues, errors, or suggestions for improvements. 
Your feedback is invaluable in helping us identify and prioritise areas for improvement. 
Please feel free to submit questions, bug reports, or feature requests via our GitHub issues page or by reaching out.

Thank you for your understanding and for contributing to the growth and improvement of this project!

---

*For more information, please visit the [project repository](https://github.com/christie-nhs-data-science/DQMaRC)*

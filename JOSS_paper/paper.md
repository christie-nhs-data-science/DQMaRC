---
title: 'DQMaRC: A Python Tool for Structured Data Quality Profiling.'
tags:
  - Python
  - shiny for python
  - data quality
  - metadata
  - DAMA
  - data management
  - data accuracy
  - data completeness
  - data validity
  - data timeliness
  - data uniqueness
  - data consistency
  - structured data
authors:
  - name: Anthony Lighterness
    orcid: 0000-0001-6898-6265
    equal-contrib: true
    affiliation: 1
  - name: Michael Thomas Adcock
    orcid: 0009-0009-5111-380X
    equal-contrib: true
    affiliation: 1
  - name: Gareth Price
    orcid: 0000-0003-4353-3360
    affiliation: "1, 2"
affiliations:
 - name: Clinical Outcomes and Data Unit, The Christie NHS Foundation Trust, Manchester, UK
   index: 1
 - name: University of Manchester, Manchester, UK
   index: 2
date: 01 December 2024
bibliography: paper.bib
---

# Summary

`DQMaRC` (Data Quality Markup and Ready-to-Connect) is an open-source Python tool designed to enable comprehensive data quality (DQ) profiling of structured data. It offers easy-to-customise parameters to evaluate DQ across six core dimensions defined by the Data Management Association (DAMA), including completeness, uniqueness, validity, consistency, timeliness, and accuracy [@dama2017dmbok]. `DQMaRC` is accessible either through a python API or a user-friendly `shiny for python` graphical user interface, making it accessible to both Python and non-Python users. The main product that `DQMaRC` generates is a detailed cell-level markup of DQ errors that connects to the source input data, allowing users to pinpoint specific issues within their datasets.

# Statement of need
The quality of data describes if data is fit for a given purpose. This expected behavior can be documented and understood using metadata – additional data that provides meaning and context by describing how the data it is associated with should have been captured, defined, structured, and represented. Metadata, in turn, can inform the design of quantifiable metrics that measure the compliance of data against a set of relevant business rules and constraints during DQ assessment.

Scholars have proposed various multi-dimensional frameworks for comprehensive DQ assessment. Despite differing definitions and terminologies, certain DQ concepts are consistently studied and well-represented in the literature, popular frameworks, and DQ profiling software. The six core dimensions defined by DAMA – completeness, validity, consistency, uniqueness, timeliness, and accuracy – serve as the foundation for DQMaRC's assessment criteria [@dama2017dmbok].

In the current landscape of data-driven research and decision making, access to high quality data is crucial to maximise confidence and accuracy of outcomes. Despite the abundance of available DQ profiling software, current tooling often lack of sufficient user documentation, suffer from interoperability issues, don't offer functionality for a range of DQ dimensions or metrics, have complex configuration requirements, or don't generate DQ results that faciliate in-depth root cause analysis or monitoring capabilites [@Lighterness:2024]. `DQMaRC` addresses these gaps by offering:

1. **Extensive User Documentation**: `DQMaRC` user documentation provides extensive explanations and examples of each customisable feature, user function, and output product.
2. **Interoperability**: The `DQMaRC` python API offers a high degree of flexibility, making it interoperable with a wide range of applications and information technology infrastructures.
3. **Cell-Level Markup of DQ Results**: The primary DQ report consists of a cell-level markup of DQ errors that can be joined with the source data to enable thorough DQ analysis.
4. **Multi-Dimensional Analysis**: `DQMaRC` provides simple functions to evaluate DQ across six key dimensions as defined by DAMA (UK).
5. **Plug-and-Play Functionality**: `DQMaRC` offers quickstart capabilities by auto-generating a template for test parameters to run based on the input source data, allowing users to quickly understand its capabilities without the need for extensive configuration.
6. **Comprehensive Customisation**: Users can customise a range of test parameters for each DQ dimension, tailoring the tool and outputs to specific needs.
7. **Accessibility**: User-friendly python functions and a graphical user interface makes `DQMaRC` accessible to both Python and non-Python users.

# DQMaRC Workflow
The workflow that DQMaRC follows includes three main steps. Each step involves a key dataset, which is summarised and illustrated in [Figure 1](#fig:workflow_general) below. Firstly, the user selects a structured dataset to perform DQ profiling on. This data can be stored in a database or a csv file. In the second step, the user initialises `DQMaRC`, which produces a template of test parameters based on the input source dataset. The user can customise these parameters or proceed with running `DQMaRC`. In the third step, `DQMaRC` generates a cell-level markup of DQ flags, indicating the presence of errors. This report can be joined with the input source data for in-depth DQ analysis of possible root causes or patterns.

<figure class="image">
  <img src="../docs/source/images/DQMaRC_method.png" 
  alt="{{ include.description }}" width="80%" id="fig:workflow_general">
  <figcaption>Figure 1: An image illustrating the key steps involved in running the DQMaRC workflow.</figcaption>
</figure>

## DQMaRC for Non-Python Users
`DQMaRC` is accessible to non-python users via a user-friendly graphical user interface built using `shiny for python`. This is accessible by navigating to this link: [DQMaRC shiny frontend](https://placeholder-link.com). [Figure 2](#fig:workflow_shiny) below shows a series of screenshot images taken from the frontend graphical user interface of `DQMaRC`. These correspond with the aforementioned workflow.

<figure class="image">
  <img src="../docs/source/images/DQMaRC_method_shiny_GUI.png" 
  alt="{{ include.description }}" id="fig:workflow_shiny">
  <figcaption>Figure 2: A series of screenshots taken from the DQMaRC graphical user interface built using shiny for python.</figcaption>
</figure>

## DQMaRC for Python Users
The user documentation explains in-depth how to install ``DQMaRC`` using pip or conda. This can be accessed from this link (insert user docs URL). 

`DQMaRC` uses the `pandas` and `numpy` libraries to perform data manipulation and calculations according to user specified test parameters. The python API makes user-friendly functions available to follow an intuitive workflow, as illustrated in [Figure 1](#fig:workflow_general) above. In python, these steps are as follows:

1. **Source Data**
```
# Import source data for DQ profiling
df = pd.read_csv("./directory_to_data.csv")
```

1. **Test Parameters**
```
# Initialise the test parameters template
dq = DataQuality(df)
test_params = dq.get_test_params()

# (Optional: edit test parameters programmatically)
# For example, let's set Completeness Encoding only for the "Gender" column
test_params.at[2,'Completeness_Encoded']=True
test_params.at[2,'Completeness_Encoded_Mapping']='Unknown|Not Known|na' 

# (Optional: import a test parameters csv edited using MS Excel)
final_test_params = pd.read_csv('./directory_to_test_parameters.csv')

# Set the final test parameters
dq.set_test_parameters(final_test_params)
```

3. **DQ Results**
```
# Run DQMaRC
dq.run_all_metrics()

# Yield full results
full_results = dq.raw_results()

# Join results to source data
df_DQ_full = df.join(full_results, how="left")
```

# Funding

This work was supported by Cancer Research UK RadNet Manchester [C199/A28701]. Dr Price was supported by the NIHR Manchester Biomedical Research Centre (NIHR203308).

# Acknowledgements

The authors would like to thank Dr Catherine O'Hara and Dr Lauren Scanlon from the Clinical Outcomes and Data Unit at The Christie NHS Foundation Trust for their support and guidance in this project.

# References

.. _welcome_page:

===============
Getting Started
===============

Welcome to :ref:`DQMaRC <api.DQMaRC>` (**Data Quality Markup and Ready-to-Connect**). 
:ref:`DQMaRC <api.DQMaRC>` is a Python-based tool for data quality profiling. We are pleased that you are interested to 
learn about :ref:`DQMaRC <api.DQMaRC>` and hope that it is useful for your data quality profiling needs. This guide will provide
you with the foundational knowledge and practical steps needed to get started with :ref:`DQMaRC <api.DQMaRC>`, whether you're a 
seasoned Python programmer or a non-technical user.

What is Data Quality? 
---------------------
Data quality (DQ) refers to the condition of a dataset, assessing whether it meets the needs of its intended use.
High-quality data is critical for effective and accurate decision-making in any field, particularly in healthcare, 
finance, and research. DQ errors are indicative of real-world problems arising from behaviours, processes, or systems.

DQMaRC evaluates data quality across six core dimensions as defined by the Data Management Association (DAMA) 
`[1] <https://www.gov.uk/government/news/meet-the-data-quality-dimensions>`_:

.. raw:: html

    <div class="tile-container">
        <div class="tile" id="tile-completeness" onclick="showDescription('tile-completeness')">
            <img src="../_static/images/completeness.png" alt="Completeness">
        </div>
        <div class="tile" id="tile-validity" onclick="showDescription('tile-validity')">
            <img src="../_static/images/validity.png" alt="Validity">
        </div>
        <div class="tile" id="tile-consistency" onclick="showDescription('tile-consistency')">
            <img src="../_static/images/consistency.png" alt="Consistency">
        </div>
        <div class="tile" id="tile-timeliness" onclick="showDescription('tile-timeliness')">
            <img src="../_static/images/timeliness.png" alt="Timeliness">
        </div>
        <div class="tile" id="tile-uniqueness" onclick="showDescription('tile-uniqueness')">
            <img src="../_static/images/uniqueness.png" alt="Uniqueness">
        </div>
        <div class="tile" id="tile-accuracy" onclick="showDescription('tile-accuracy')">
            <img src="../_static/images/accuracy.png" alt="Accuracy">
        </div>
    </div>
    <div id="description-area">
        <p id="description-text">Click on a tile to learn more about each dimension.</p>
    </div>



Why Use DQMaRC?
---------------

#. **In-Depth Cell-Level Markup**: DQMaRC generates detailed cell-level markup of DQ issues, allowing precise identification of problematic data directly connected to the source.

#. **Multi-Dimensional Analysis**: Provides custom metrics to evaluate DQ across six key dimensions as defined by DAMA, ensuring a thorough assessment.

#. **Plug-and-Play Functionality**: DQMaRC offers readily available test parameters that allow users to quickly start assessing DQ without extensive setup or configuration.

#. **Easy and Thorough Customisation**: Users can easily customise DQ test parameters either programmatically or in Excel, tailoring the tool to specific needs.

#. **Accessibility**: Designed for both Python programmers and non-technical users, with a graphical user interface (GUI) built with Shiny for Python, lowering the barrier to entry.

#. **Flexible and Interoperable**: The DQMaRC Python API can be integrated into a diverse range of applications, IT infrastructures, data processing and analysis workflows. 


How does DQMaRC Work: The Role of Metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Metadata is data about data. It provides context, meaning, and guidelines on how data should be captured, defined, structured, and represented. Metadata should be comprehensive,
up-to-date, and thorough in its description of how data should be defined, captured, structured, and analysed. 
Robust metadata is the cornerstone of any DQ evaluation process as it forms the foundations of business rules and constraints during DQ assessment. :ref:`DQMaRC <api.DQMaRC>`
uses metadata in the form of test parameters to perform DQ tests. The results of these tests generate a binary markup of 1's and 0's, i.e. flags indicating the presence
or absence of an error for a given dimension of DQ.
Overall, the workflow when using :ref:`DQMaRC <api.DQMaRC>` can be described in three key steps as illustrated in :ref:`figworkflow1`:

#. Identify and prepare the source dataset.
#. Identify and define the relevant metadata, test parameters, and data standards.
#. Analyse the DQ results.

.. _figworkflow1:

.. figure:: ../images/DQMaRC_method.png
  :alt: DQMaRC workflow
  :scale: 20%

  Figure 1: image showing DQMaRC workflow.


.. _setup_python:

How To Access DQMaRC? 
---------------------
See below how you can access :ref:`DQMaRC <api.DQMaRC>` either by installing it through pip or conda, or by accessing the user friendly graphical user interface (GUI).

Python Installation
^^^^^^^^^^^^^^^^^^^
If you want to run :ref:`DQMaRC <api.DQMaRC>` as a Python user, please follow the tutorial provided in the :ref:`Backend Python Tutorial <Backend_Tutorial>` section. 

To install :ref:`DQMaRC <api.DQMaRC>` into your python environment, please follow the instructions below.

To view the package dependencies, you can access the `requirements.txt` and/or `environment.yml` file from the `DQMaRC GitHub Repository <https://github.com/yourusername/DQMaRC>`_.

The key dependencies are: 
    * Python (>= 3.9)
    * NumPy (>= 1.16)
    * pandas (>=2.2)
    * plotly (>=5.22)
    * shiny (>=0.10)
    * ipydatagrid (>1.3)
    * ipywidgets (>8.1)

**Installation**

.. tabs::
    
    .. tab:: Conda Virtual Environment

        1. **Install Conda**:

        Make sure you have Conda installed. If not, download and install it from the `Anaconda <https://www.anaconda.com/products/distribution>`_ 
        website or the `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ website.

        2. **Navigate to the Directory Containing `environment.yml`**:

        Open a terminal (or Anaconda Powershell) and navigate to your project directory.
        You can also download the ``DQMaRC`` `environment.yml` file and place it here if you prefer to setup a conda
        environment using the yml file.

        3. **Create the Conda Environment**:

        Create your conda environment either from scratch or using the environment.yml file:

        A new conda environment: 

        .. code-block:: bash

            conda create -n myenv python=3.9 pandas numpy
        
        From the yml file:
        
        .. code-block:: bash

            conda env create -f environment.yml


        4. **Activate the Conda Environment**:

        Once the environment is created, activate it using:

        .. code-block:: bash
            
            conda activate <environment_name>

        Replace `<environment_name>` with your conda environment name or the name specified in the `environment.yml` file.

        5. **Verify the Environment**:

        You can verify that the environment is active and working by checking the installed packages:
        
        .. code-block:: bash

            conda list

        6. **Conda Install DQMaRC**

        .. code-block:: console

            $ conda install -c conda-forge DQMaRC

            $ git clone https://github.com/The-Christie-NHS-FT/DQMaRC



    .. tab:: Python Virtual Environment

        1. **Install Python>=3.9**:

        Make sure you have Python>=3.9 installed. You can download it from the `Python <https://www.python.org/>`_ website.

        2. **Install `virtualenv`**:

        Install `virtualenv` if you don't have it already:
        
        .. code-block:: bash

            pip install virtualenv

        3. **Navigate to the Appropriate Directory**:

        Open a terminal and navigate to your project directory.

        4. **Create your own python virtual environment (must have python >=3.9)**

        .. code-block:: bash

            python -m venv <environment_name>

        Replace `<environment_name>` with your desired environment name.

        5. **Activate the Virtual Environment**:

            **Windows**:

            .. code-block:: bash

                <environment_name>\Scripts\activate


            **MacOS/Linux**:
                
            .. code-block:: bash

                source <environment_name>/bin/activate


        6. **Download and Install DQMaRC**:
        Using the distribution wheel file:

        .. code-block:: bash

            pip install DQMaRC-1.0.0-py3-none-any.whl


        Using PyPi:

        .. code-block:: bash

            pip install DQMaRC


        Or clone directly from GitHub:

        .. code-block:: console

            $ git clone https://github.com/The-Christie-NHS-FT/DQMaRC


        7. **Verify the Installation**:

        You can verify that the environment is active and working by checking the installed packages:

        .. code-block:: bash

            pip list


.. _setup_nonpython:

The Shiny App User Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you prefer a graphical interface, please refer to the :ref:`Frontend ShinyPy Tutorial <Frontend_Tutorial>` section. 
This guide will walk you through the installation and use of the Shiny for Python interface to run DQMaRC without writing any code.
We have built a frontend graphical user interface using `shiny for python <https://shiny.posit.co/py/>`_ to encourage non-python users to use ``DQMaRC``.

You can access a serverless, web-hosted version here: `DQMaRC Shiny Front End <https://github.com/christie-nhs-data-science/DQMaRC/blob/main/DQMaRC_ShinyLiveEditor_link>`_. 
Please note this will run in your local web browser. For more information refer to `Shinylive web hosting <https://shiny.posit.co/py/docs/shinylive.html>`_

If you installed ``DQMaRC`` using pip or conda, you can also run the ``shiny app`` in terminal, bash, or Anaconda Powershell:

.. tabs::

    .. tab:: Serverless Web-Browser

        You can access a serverless, web-hosted version here: `DQMaRC Shiny Front End <https://github.com/christie-nhs-data-science/DQMaRC/blob/main/DQMaRC_ShinyLiveEditor_link>`_. 


    .. tab:: Cloned from GitHub

        If you cloned the `DQMaRC GitHub repo  <https://placeholder.link>`_:

        .. code-block:: console

            shiny run --reload --launch-browser "C:\Users\...\pip_env_dqmarc1\Lib\site-packages\DQMaRC\app.py"


    .. tab:: Installed via Pip or Conda

        Once you have installed ``DQMaRC`` using pip or conda and have your pip or conda virtual environment setup, run the following code in terminal or anaconda powershell. 
        This will deploy the app.py script to your local web-browser at localhost. 
        Please adjust the directory string below to point to where you have DQMaRC installed. 

        .. code-block:: console

            shiny run --reload --launch-browser "C:\Users\...\Lib\site-packages\DQMaRC\app.py"

        To find the location of where you installed ``DQMaRC``, you can use the following command in terminal:

        .. code-block:: console

            pip show DQMaRC


Here is an overview of the front-end user interface. This is explained in more detail in :ref:`Frontend ShinyPy Tutorial <Frontend_Tutorial>` section. 

.. figure:: ../images/DQMaRC_method_shiny_GUI.png
  :alt: DQMaRC shiny frontend graphical user interface.
  :scale: 10%

  Figure 2: Example data processed in the DQMaRC frontend graphical user interface built in shiny for python.


Cite DQMaRC
-----------

Please use the following citation if you use DQMaRC:

Lighterness, A., Adcock, M.A., and Price, G. (2024). DQMaRC: A Python Tool for Structured Data Quality Profiling (Version 1.0.0) [Software]. Available from https://github.com/christie-nhs-data-science/DQMaRC.


References
----------
[1] Government Data Quality Hub. (2021, June 24). Meet the data quality dimensions. GOV.UK. https://www.gov.uk/government/news/meet-the-data-quality-dimensions

.. _deployment_guide:

Deployment Guide
================

Once you have downloaded and installed ``DQMaRC`` from Pip or Conda, or cloned the GitHub repo, you can find the shiny front-end user interface script 
in the ``DQMaRC/app.py`` script. This app can be deployed locally, to the cloud, or an on-premises server. 

.. tabs::

    .. tab:: Local Deployment

        Once you have installed ``DQMaRC`` using pip or conda and have your pip or conda virtual environment setup, run the following code in terminal or anaconda powershell. 
        This will deploy the app.py script to your local web-browser at localhost. 
        Please adjust the directory string below to point to where you have DQMaRC installed. 

        .. code-block:: bash

            shiny run --reload --launch-browser "C:\Users\...\Lib\site-packages\DQMaRC\app.py"

        To find the location of where you installed ``DQMaRC``, you can use the following command in terminal:

        .. code-block:: bash

            pip show DQMaRC

    .. tab:: Cloud or Server Deployment

        The official shiny for python documentation specify the deployment options here: `Shiny for Python Hosting and Deployment <https://shiny.posit.co/py/docs/deploy.html>`_.


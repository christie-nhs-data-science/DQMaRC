from setuptools import setup, find_packages
from pathlib import Path

with open("requirements.txt", encoding="utf-8-sig") as f:
    requirements = f.read().splitlines()

setup(
    name='DQMaRC',
    version='1.0.2',
    author='Anthony Lighterness and Michael Adcock',
    author_email='tony.lighterness@gmail.com',
    
    description='DQMaRC is a python tool for data quality profiling of structured tabular data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/christie-nhs-data-science/DQMaRC',
    packages=find_packages(),
    #packages=["DQMaRC"],

    # install_requires=requirements,
    install_requires=requirements,
    include_package_data=True,
    package_data={
        'DQMaRC': ['data/*.csv'],
    },

    entry_points={
        'console_scripts': [
            'dqmarc=DQMaRC.DataQuality:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Open Government License v3'
    ],
    python_requires='>=3.9',
)

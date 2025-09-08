# pypi-info-scraper

The repository contains the script used for the automatic data collection necessary for an academic research paper on FPGA-related packages on the Python Package Index ([PyPI](https://pypi.org/)).

The paper will be published in the 10th South-East Europe Design Automation, Computer Engineering, Computer Networks and Social Media Conference (**SEEDA-CECNSM 2025**).

The paper is titled "_The State of Python-Based FPGA Development: A PyPI Repository Study_".

## Prerequisites
- [python](https://www.python.org/)
- [selenium](https://pypi.org/project/selenium/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4)
- [pandas](https://pypi.org/project/pandas/)
- [openpyxl](https://pypi.org/project/openpyxl/)

The script should be compatible with most operating systems.

## Handling Anti-Scraping Measures

Since the Python Package Index ([PyPI](https://pypi.org/)) has anti-scraping measures in place, a user challenge is necessary the first time the browser window is opened automatically from the Python script.

In that sense, when the script performs the "fpga" keyword search for the first page (page 1), user intervention is necessary. The user is given more time to perform the necessary actions.

Subsequent requests for the next pages of the search (page 2, 3, etc.) do not require further intervention. Additionally, no anti-scraping measures are required in the next stage of the process, where the JSON data for each package in the list is retrieved.

## Output Format

The scraping results are saved in a structured Excel file.

The script was executed at the beginning of 2025 in order to acquire the information necessary for writing the aforementioned statistical review.

You can find the scraped data in _pypi_packages.xlsx_.

## Utility and Significance

Basic statistics on packages hosted on [PyPI](https://pypi.org/) can be gathered automatically by customizing this scraper.

This should aid future research of that nature.

The script is distributed under the MIT license.

## Publication

The paper can be found on IEEE Xplore: **TO BE INCLUDED**

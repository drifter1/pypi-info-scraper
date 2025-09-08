
from selenium import webdriver
from bs4 import BeautifulSoup

import pandas as pd

import json
import time

import re
from collections import defaultdict


# Filter package classifiers for 'Development Status'
def classify_development_status(classifiers):

    dev_status = [c for c in classifiers if 'Development Status' in c]

    if dev_status:
        status = dev_status[0].split('-')[-1].strip()
    else:
        status ="Not specified"
        
    return status    


# Filter package classifiers for 'Intended Audience'
def classify_intended_audience(classifiers):

    intended_audience = [c for c in classifiers if 'Intended Audience' in c]

    if intended_audience:
        audience = intended_audience[0].split('::')[-1].strip()
    else:
        audience = "Not specified"
        
    return audience    


# Package class
class Package:
    
    def __init__(self, name, version, summary, author, author_email, project_url, requires_python,
                license, last_release_date, release_count, package_size, has_wheel, has_egg,
                development_status, intended_audience):
        self.name = name  # Package name
        self.version = version # Version of the package
        self.summary = summary # Short description of the package
        self.author = author # Author of the package
        self.author_email = author_email # Author's email address
        self.project_url = project_url # URL to the project homepage or repository
        self.requires_python = requires_python # Python version requirement (e.g., >=3.6)
        self.license = license # License of the package (e.g., MIT, BSD, GPL, Apache)
        self.last_release_date = last_release_date # Date of the most recent release
        self.release_count = release_count # Total number of releases     
        self.package_size = package_size # Size of the package distribution files        
        self.has_wheel = has_wheel # Whether the package has a wheel distribution
        self.has_egg = has_egg # Whether the package has an egg distribution
        self.development_status = development_status # Development status (e.g., Alpha, Beta, Production/Stable)
        self.intended_audience = intended_audience # Intended Audience (e.g., Developers, Science/Research)

    def __str__(self) -> str:
        return f"Package: {self.name}, Version: {self.version}, Last Release Date: {self.last_release_date}"


# Retrieve search results for a specific keyword. This yields a list of packages
def scrape_pypi_search_results(keyword, order_type):
    
    # Base URL for PyPI search
    if (order_type == "date_last_updated"):
        base_url = f"https://pypi.org/search/?o=-created&q={keyword}&page="
    else:
        base_url = f"https://pypi.org/search/?q={keyword}&page="
    
    # Initialize page number and result storage
    page = 1
    all_packages = []

    # open a Chrome web browser
    driver = webdriver.Chrome()
    
    while True:
        
        # Construct the search URL    
        url = base_url + str(page)
        
        # Request search page with the current page number
        driver.get(url)

        # wait a few seconds for the page to load. wait longer on the first page so that the user challenge can be performed
        if page == 1:
            time.sleep(10)
        else:
            time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find the search result package snippets
        results = soup.find_all('a', class_='package-snippet')
        
        # If no results are found, stop the loop
        if not results:
            break
        
         # Store the result in a dictionary
        for result in results:
            all_packages.append(result)
            
        print(f"Scraped page {page} with {len(results)} results.")
        
        # Move to the next page
        page += 1

    # quit the web browser
    driver.quit()
    
    return all_packages


# Fetch the raw information of a specific package
def get_pypi_package_info(driver, package_name):

    try:
        # PyPI JSON API endpoint for a package
        url = f"https://pypi.org/pypi/{package_name}/json"
        driver.get(url)

        # wait a few seconds for the page to load.
        time.sleep(2)

        # Extract the raw page content
        page_source = driver.page_source

        # Parse JSON from the page source
        # Attempt to find the JSON-like structure in the page source
        start_idx = page_source.find("{")
        end_idx = page_source.rfind("}") + 1

        if start_idx != -1 and end_idx != -1:
            json_text = page_source[start_idx:end_idx]
            package_data = json.loads(json_text)
            return package_data

        else:
            return None

    except Exception as e:
        return None



# Extract the information of all packages and populate a list of Package objectinstances
def extract_package_information(results):
    packages : List[Package] = []

    # open a Chrome web browser
    driver = webdriver.Chrome()
        
    for result in results:
        
        package_name = result.find('span', class_='package-snippet__name').text
        
        # Fetch package info
        package_data = get_pypi_package_info(driver, package_name)
        
        # Extract information from the JSON response
        if package_data:
            package_info = package_data['info']
            package_urls = package_data['urls']
            
            name = package_info['name']
            version = package_info['version']
            summary = package_info['summary']
            author = package_info['author']
            author_email = package_info['author_email']
            project_url = package_info['project_url']
            requires_python = package_info['requires_python']
            license = package_info['license']
            last_release_date = package_urls[0]['upload_time'] if package_urls else ''
            release_count = len(package_data['releases'])
            package_size = sum(url['size'] for url in package_urls)
            has_wheel = any('wheel' in url['packagetype'].lower() for url in package_urls)
            has_egg = any('egg' in url['packagetype'].lower() for url in package_urls)

            # Extract classifiers from the metadata
            classifiers = package_info['classifiers']
            
            # Filter development status and intended audience from the classifiers
            development_status = classify_development_status(classifiers)
            intended_audience = classify_intended_audience(classifiers)
                
            # Create a Package instance with all details
            package = Package(name, version, summary, author, author_email, project_url, requires_python, license,
                              last_release_date, release_count, package_size, has_wheel, has_egg,
                              development_status, intended_audience)
            
            print(package)
                
            packages.append(package)

     # quit the web browser
    driver.quit()
        
    return packages


'''
MAIN FUNCTION
'''


# Retrieve the results for the search string "fpga". Sort by date
results = scrape_pypi_search_results('fpga', "date_last_updated")


# Extract package information and populate a list
packages = extract_package_information(results)


# Convert list of Package objects into a list of dictionaries
packages_dict = [vars(package) for package in packages]


# Create a Pandas DataFrame from the list of dictionaries
df = pd.DataFrame(packages_dict)


# Export the DataFrame to an Excel file
df.to_excel('pypi_packages.xlsx', index=False)


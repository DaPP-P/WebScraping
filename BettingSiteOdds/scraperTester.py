import os
import subprocess
import time
import random
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import platform


# Inital admin for subprocess.
python_interpreter = 'python3'
resultchecker_script = 'resultChecker.py'
arbitrage_script = 'arbitrage.py'

# Initial admin. Set up with help from: https://www.youtube.com/watch?v=kpONBQ3muLg
user_agent = 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/116.0'
firefox_driver = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')

test_service = Service(firefox_driver, log_output = None)

# TEST THINGS
test_website = "tab"
test_file = "tabResults.txt"
test_url = "https://www.tab.co.nz/sport/8/basketball/matches"
test_container_name = "event-list event-list--vertical"
test_sport = "basketball"

# Set the settings 
firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)
#firefox_options.add_argument('-headless')

# Create separate browsers for each website needing to be accessed
test_browser = webdriver.Firefox(service=test_service, options=firefox_options)

# Set up paths for the TxtFiles for BASKETBALL
script_dir = os.path.dirname(os.path.abspath(__file__))
txt_files_folder = os.path.join(script_dir, "TxtFiles")

# Set up paths for the TxtFiles for TENNIS
script_tennis_dir = os.path.dirname(os.path.abspath(__file__))
tennis_txt_files_folder = os.path.join(script_dir, "TxtFilesTennis")

test_file_name = test_file
test_file_path = os.path.join(txt_files_folder, test_file_name)
test_tennis_file_path = os.path.join(tennis_txt_files_folder, test_file_name)

# Load test website
print("Opening test url: ", test_url)
test_browser.get(test_url)
time.sleep(20)

page_source = test_browser.page_source
test_browser.quit()
print("Closed test url: ", test_url)

# Uses BeautifulSoup to get the content of the page_source.
soup = BeautifulSoup(page_source, "html.parser")
container = soup.find_all("div", class_ = test_container_name)
container_contents = []

# Checks if the container can be found and return results.
if container:
    for container in container:
        # Extract the content of the container
        container_content = container.get_text()
        container_contents.append(container_content)
        container_contents.append("\n")
    upload_test_odds = (container_contents)
else:
    print("Container not found")
    upload_test_odds = ""






# Method for importing the scraped odds to the desired txt file.
def upload_odds(website, odds, sport):
    
    # Upload Basketball odds
    if sport == "Basketball":
        file_path = test_file_path
        with open(file_path, "a") as file:
            file.truncate(0)
            if odds:
                for odd in odds:
                    file.write(str(odd))
                print("raw", website, "BASKETBALL stats have been scraped")
            else:
                print("raw", website, "BASKETBALL stats have NOT been scraped")
    
    # Upload Tennis odds
    if sport == "Tennis":
        file_path = test_file_path
        with open(file_path, "a") as file:
            file.truncate(0)
            if odds:
                for odd in odds:
                    file.write(str(odd))
                print("raw", website, "TENNIS stats have been scraped")
            else:
                print("raw", website, "TENNIS stats have NOT been scraped")

upload_odds(test_website, upload_test_odds, test_sport)
print("odds: ", upload_test_odds)
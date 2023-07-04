import os
import time
import re
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup


def get_current_temp(location):
    # Admin set up stuff gotten from: https://www.youtube.com/watch?v=kpONBQ3muLg
    # Not really sure how it works but it works but it sets up Selenium
    user_agent  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
    firefox_driver = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
    firefox_service = Service(firefox_driver)
    firefox_options = Options()
    firefox_options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    firefox_options.set_preference('general.useragent.override', user_agent)
    browser = webdriver.Firefox(service=firefox_service, options= firefox_options)

    # Opens the locations weather page
    print("Loading Website for", location.capitalize()) 
    url = f"https://www.metservice.com/towns-cities/locations/{location}"
    browser.get(url)

    # Wait for the page to load
    time.sleep(2)

    # Get the page source then cloes the page
    page_source = browser.page_source
    browser.quit()
    print("Closing Website...")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Find the element containing the current temperature
    temperature_element = soup.find(class_="temperature-current")

    if temperature_element:
        # Extract the temperature value
        temperature = temperature_element.get_text()
        return location.capitalize(), temperature
    else:
        return location.capitalize(), "Unable to retrieve the temperature"

def is_float(string):
    try:   
        float(string)
        return True
    except ValueError:
        return False

# Locations to retrieve the temperature for
locations = ["dunedin", "auckland", "wellington", "Hamilton", "Gisborne", "Palmerston-north", "Christchurch", "Queenstown", "taupo", "nelson"]

# Array to store the results
temperature_data = []

# Iterate over the locations and get the temperature for each
for location in locations:
    location_name, temperature = get_current_temp(location)
    temperature_data.append((location_name, temperature))

# Print the temperature data
for location, temperature in temperature_data:
    print(f"Current temperature in {location}: {temperature}")

# Remove the degree symbol from the temperature strings using regex
degree_regex = re.compile(r"°")
temperature_data = [(location, degree_regex.sub("", temperature)) for location, temperature in temperature_data]

# Filter out entries with "Unable to retrieve the temperature"
filtered_temperature_data = [(location, temperature) for location, temperature in temperature_data if is_float(temperature)]

# Find the highest and lowest temperatures
if filtered_temperature_data:
    highest_temp = max(filtered_temperature_data, key=lambda x: float(x[1]))
    lowest_temp = min(filtered_temperature_data, key=lambda x: float(x[1]))

    print(f"Highest temperature: {highest_temp[1]}°C in {highest_temp[0]}")
    print(f"Lowest temperature: {lowest_temp[1]}°C in {lowest_temp[0]}")
else:
    print("No temperature data available.")
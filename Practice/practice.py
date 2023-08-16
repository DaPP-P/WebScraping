import os
import concurrent.futures
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
geckodriver_path = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
firefox_service = Service(geckodriver_path)
firefox_options = Options()
firefox_options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
firefox_options.set_preference('general.useragent.override', user_agent)

locations = ["https://www.metservice.com/towns-cities/locations/auckland",
             "https://www.metservice.com/towns-cities/locations/wellington",
             "https://www.metservice.com/towns-cities/locations/christchurch"]

def scrape_temperature(location):
    with webdriver.Firefox(service=firefox_service, options=firefox_options) as driver:
        driver.get(location)
        temperature_element = driver.find_element_by_class_name("temperature-current")
        temperature = temperature_element.text
        return temperature

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = executor.map(scrape_temperature, locations)

temperature_data = list(results)
print(temperature_data)

import os
import time
import re
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Uses python 3.9.13 64-bit


def get_bet365_odds():
    # Admin set up stuff gotten from: https://www.youtube.com/watch?v=kpONBQ3muLg
    # Not really sure how it works but it works but it sets up Selenium
    user_agent  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
    firefox_driver = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
    firefox_service = Service(firefox_driver)
    firefox_options = Options()
    firefox_options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    firefox_options.set_preference('general.useragent.override', user_agent)
    browser = webdriver.Firefox(service=firefox_service, options= firefox_options)

    # Open Bet365 website
    print("Opening website...")
    url = "https://www.bet365.com/#/HO/"
    browser.get(url)

    # Wait for the page to load
    time.sleep(10)

    # Accepts Cookies
    #accept_button_xpath = "/html/body/div[3]/div/div[2]/div[2]"
    #accept_button = browser.find_element(By.XPATH, accept_button_xpath)
    #accept_button.click()

    # Open up the basketball page
    #basketball_button_xpath = "/html/body/div[1]/div/div[3]/div[2]/div/div/div[1]/div/div[2]/div/div[10]"
    #basketball_button = browser.find_element(By.XPATH, basketball_button_xpath)
    #basketball_button.click()

    # Get the page source then cloes the page
    page_source = browser.page_source
    browser.quit()
    print("Closing Website...")

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    container = soup.find("div", class_ = "gl-MarketGroup_Wrapper src-MarketGroup_Container ")
    container2 = soup.find("div", class_ = "event-list__item-link")

    if container:
        # Extract the content of the container
        container_content = container.get_text()
        return (container_content)
    else:
        print("Container not found")

    if container2:
        # Extract the content of the container
        container_content2 = container2.get_text()
        return (container_content2)
    else:
        print("Container2 not found")

script_dir = os.path.dirname(os.path.abspath(__file__))
txt_files_folder = os.path.join(script_dir, "..", "TxtFiles")
file_name = "bet365Results.txt"

file_path = os.path.join(txt_files_folder, file_name)

file = open(file_path, "w")
odds = get_bet365_odds()

for odd in odds:
    file.write(str(odd))

file.close
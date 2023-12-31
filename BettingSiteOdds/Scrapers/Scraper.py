import os
import time
import re
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import platform

system_name = platform.system()

def get_odds(url, containerName):

    # Admin set up stuff gotten from: https://www.youtube.com/watch?v=kpONBQ3muLg
    # Not really sure how it works but it works but it sets up Selenium
    user_agent  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"
    firefox_driver = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
    firefox_service = Service(firefox_driver)
    firefox_options = Options()
    #firefox_options.headless = True
    
    # For Windows:
    if system_name == "Windows":
        firefox_options.binary_location = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"

    # For Mac:
    if system_name == "MacOS":
        firefox_options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"

    # For Linux:
    if system_name == "Linux":
        firefox_options.binary_location = "/usr/bin/firefox"
    
    firefox_options.set_preference('general.useragent.override', user_agent)
    browser = webdriver.Firefox(service=firefox_service, options= firefox_options)

    # Open website
    print("Opening", url)
    browser.get(url)

    # Wait for the page to load FIX: MAKE IT NOT WORK OFF SLEEP
    time.sleep(10)


    # Get the page source then cloes the page
    page_source = browser.page_source
    browser.quit()
    print("Closing", url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, "lxml")

    container = soup.find_all("div", class_ = containerName)
    
    # KEEP: IT IS NEEDED FOR TAB CONTAINERS BE FUCKED UP
    container2 = soup.find("div", class_ = "event-list__item-link")

    container_contents = []

    if container:
        for container in container:
        # Extract the content of the container
            container_content = container.get_text()
            container_contents.append(container_content)
            container_contents.append("\n")
        return (container_contents)
    else:
        print("Container not found")

    if container2:
        # Extract the content of the container
        container_content2 = container2.get_text()
        return (container_content2)
    else:
        print("Container2 not found")

# Set up the path for the TxtFiles
script_dir = os.path.dirname(os.path.abspath(__file__))
txt_files_folder = os.path.join(script_dir, "..", "TxtFiles")

# Set up path for the tab
tab_file_name = "tabResults.txt"
tab_file_path = os.path.join(txt_files_folder, tab_file_name)

# Set up path for bet365
bet365_file_name = "bet365Results.txt"
bet365_file_name_file_path = os.path.join(txt_files_folder,bet365_file_name)

# Set up path for pinnacle
pinnacle_file_name = "pinnacleResults.txt"
pinnacle_file_path = os.path.join(txt_files_folder, pinnacle_file_name)

# Set up path for pointsbet
pointsbet_file_name = "pointsbetResults.txt"
pointsbet_file_path = os.path.join(txt_files_folder, pointsbet_file_name)

# Set up path for unibet
unibet_file_name = "unibetResults.txt"
unibet_file_path = os.path.join(txt_files_folder, unibet_file_name)

# Set up path for ladbrokes
ladbrokes_file_name = "ladbrokesResults.txt"
ladbrokes_file_path = os.path.join(txt_files_folder, ladbrokes_file_name)

# Set up path for Tonybet
tonybet_file_name = "tonybetResults.txt"
tonybet_file_path = os.path.join(txt_files_folder, tonybet_file_name)

# Getting odds from the TAB
tab_file = open(tab_file_path, "w")
tab_odds = get_odds("https://www.tab.co.nz/sport/8/basketball/matches", "event-list event-list--vertical")

# FOR FUTURE BETTING SITES
# Pinnacle
# "https://www.pinnacle.com/en/basketball/matchups/", "style_row__3CKCJ style_row__3xXUg"
# Looks like a bitch to do.

if tab_odds:
    for odd in tab_odds:
        tab_file.write(str(odd))
    print("raw TAB odds have been scraped")
else:
    print("raw TAB odds have NOT been scraped")

tab_file.close


# Getting odds from bet365
#bet365_file = open(bet365_file_path, "w")
#bet365_odds = get_odds("https://www.tab.co.nz/sport/8/basketball/matches", "event-list event-list--vertical")

#for odd in bet365_odds:
#    bet365_file.write(str(odd))ç

#bet365_file.close

print("raw bet365 odds have NOT been scraped")

# Getting odds from pinnacle
# pinnacle_file = open(pinnacle_file_path, "w")
# pinnacle_odds = get_odds("https://tonybet.com/nz/prematch", "event-table__row")

# if pinnacle_odds:
#     for odd in pinnacle_odds:
#         pinnacle_file.write(str(odd))
#     print("raw Tonybet odds have been scraped")
# else:
#     print("raw Tonybet odds have NOT been scraped")

# pinnacle_file.close

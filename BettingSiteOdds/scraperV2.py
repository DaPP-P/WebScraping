import os
import subprocess
import time
import random
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# Inital admin for subprocess.
python_interpreter = 'python3'
resultchecker_script = 'resultChecker.py'
arbitrage_script = 'arbitrage.py'

# Initial admin. Set up with help from: https://www.youtube.com/watch?v=kpONBQ3muLg
user_agent = 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/116.0'
firefox_driver = os.path.join(os.getcwd(), 'Drivers', 'geckodriver')

# Create separate services for each browser instance
tab_service = Service(firefox_driver, log_output=None)
pointsbet_service = Service(firefox_driver, log_output=None)
unibet_service = Service(firefox_driver, log_output=None)
ladbrokes_service1 = Service(firefox_driver, log_output=None)
ladbrokes_service2 = Service(firefox_driver, log_output=None)
ladbrokes_service3 = Service(firefox_driver, log_output=None)

firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)
firefox_options.add_argument('-headless')

# Create separate browsers for each website needing to be accessed
tab_browser = webdriver.Firefox(service=tab_service, options=firefox_options)
pointsbet_browser = webdriver.Firefox(service=pointsbet_service, options=firefox_options)
unibet_browser = webdriver.Firefox(service=unibet_service, options=firefox_options)
ladbrokes_browser1 = webdriver.Firefox(service=ladbrokes_service1, options=firefox_options)
ladbrokes_browser2 = webdriver.Firefox(service=ladbrokes_service2, options=firefox_options)
ladbrokes_browser3 = webdriver.Firefox(service=ladbrokes_service3, options=firefox_options)

# Set up paths for the TxtFiles
script_dir = os.path.dirname(os.path.abspath(__file__))
txt_files_folder = os.path.join(script_dir, "TxtFiles")

# Set up path for the tab
tab_file_name = "tabResults.txt"
tab_file_path = os.path.join(txt_files_folder, tab_file_name)

# Set up path for pointsbet
pointsbet_file_name = "pointsbetResults.txt"
pointsbet_file_path = os.path.join(txt_files_folder, pointsbet_file_name)

# Set up path for unibet
unibet_file_name = "unibetResults.txt"
unibet_file_path = os.path.join(txt_files_folder, unibet_file_name)

# Set up path for ladbrokes
ladbrokes_file_name = "ladbrokesResults.txt"
ladbrokes_file_path = os.path.join(txt_files_folder, ladbrokes_file_name)

# Load TAB website
tab_browser.get("https://www.tab.co.nz/sport/8/basketball/matches")

# Load PointsBet website
pointsbet_browser.get("https://pointsbet.com.au/sports/basketball")

# Load Unibet website
unibet_browser.get("https://www.unibet.com/betting/sports/filter/basketball/all/matches")

# Load Labrokes website
ladbrokes_browser1.get("https://www.ladbrokes.com.au/sports/basketball/usa")
ladbrokes_browser2.get("https://www.ladbrokes.com.au/sports/basketball/international")
ladbrokes_browser3.get("https://www.ladbrokes.com.au/sports/basketball/australia")

time.sleep(20)

def get_odds(url, container_name, browser):
    print("Opeing", url)
    page_source = browser.page_source
    print("Closing", url)

    soup = BeautifulSoup(page_source, "html.parser")
    container = soup.find_all("div", class_ = container_name)
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

def perform_task():
    # Get odds for the TAB
    tab_odds = get_odds("https://www.tab.co.nz/sport/8/basketball/matches", "event-list event-list--vertical", tab_browser)
    print(tab_odds)
    upload_odds("tab", tab_odds)
    print("---------")
    pointsbet_odds = get_odds("https://pointsbet.com.au/sports/basketball", "f3wis39", pointsbet_browser)
    print(pointsbet_odds)
    upload_odds("pointsbet", pointsbet_odds)
    print("---------")
    unibet_odds = get_odds("https://www.unibet.com/betting/sports/filter/basketball/all/matches", "_28843", unibet_browser)
    print(unibet_odds)
    upload_odds("unibet", unibet_odds)
    print("---------")
    ladbrokes_odds1 = get_odds("https://www.ladbrokes.com.au/sports/basketball/usa", "sports-market-primary__prices-inner", ladbrokes_browser1)
    ladbrokes_odds2 = get_odds("https://www.ladbrokes.com.au/sports/basketball/international", "sports-market-primary__prices-inner", ladbrokes_browser2)
    ladbrokes_odds3 = get_odds("https://www.ladbrokes.com.au/sports/basketball/australia", "sports-market-primary__prices-inner", ladbrokes_browser3)
    ladbrokes_upload_odds(ladbrokes_odds1, ladbrokes_odds2, ladbrokes_odds3)

def upload_odds(website, odds):
    file_path = tab_file_path if website == "tab" else pointsbet_file_path if website == "pointsbet" else unibet_file_path
    with open(file_path, "a") as file:
        file.truncate(0)
        if odds:
            for odd in odds:
                file.write(str(odd))
            print("raw", website, "have been scraped")
        else:
            print("raw", website, "have NOT been scraped")

def ladbrokes_upload_odds(odds1, odds2, odds3):
    with open (ladbrokes_file_path, "a") as file:
        file.truncate(0)
        if odds1:
            for odd in odds1:
                file.write(str(odd))
        if odds2:
            for odd in odds2:
                file.write(str(odd))
        if odds3:
            for odd in odds3:
                file.write(str(odd))

i = 0
while True:

    print("Start of loop")
    # Generate a random time interval between 1 and 2 minutes
    interval = random.randint(60, 120) # seconds random.randint(60, 120)  

    # Wait for the random interval
    time.sleep(interval)

    # Perform the task
    i += 1
    if i <= 3:
        print("starting task")
        perform_task()
        print("finished task", i)

        # Run the result checker script
        process = subprocess.Popen([python_interpreter, resultchecker_script], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        process.wait()
        
        return_code = process.returncode
        if return_code == 0:
            print("Result checker script ran successfully")
        else:
            print(f"Result checker Script failed to run, error code {return_code}")


        # Run the arbitrage script
        process2 = subprocess.Popen([python_interpreter, arbitrage_script], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        process2.wait()
        
        return_code = process2.returncode
        if return_code == 0:
            print("Arbitrage script ran successfully")
        else:
            print(f"Arbitrage script failed to run, error code {return_code}")
    
    else:
        tab_browser.quit()
        pointsbet_browser.quit()
        unibet_browser.quit()
        ladbrokes_browser1.quit()
        ladbrokes_browser2.quit()
        ladbrokes_browser3.quit()
        break
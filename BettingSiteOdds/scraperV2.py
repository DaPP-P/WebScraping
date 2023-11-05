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

# Create separate services for each BASKETBALL browser instance
tab_service = Service(firefox_driver, log_output=None)
pointsbet_service = Service(firefox_driver, log_output=None)
unibet_service = Service(firefox_driver, log_output=None)
ladbrokes_service1 = Service(firefox_driver, log_output=None)
ladbrokes_service2 = Service(firefox_driver, log_output=None)
ladbrokes_service3 = Service(firefox_driver, log_output=None)
#tonybet_service = Service(firefox_driver, log_output= None)

# Create separate service for each TENNIS browser instance
tab_tennis_service = Service(firefox_driver, log_output=None)
pointsbet_tennis_service = Service(firefox_driver, log_output=None)
unibet_tennis_service = Service(firefox_driver, log_output=None)
ladbrokes_tennis_service = Service(firefox_driver, log_output=None)


# Set the settings 
firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)
firefox_options.add_argument('-headless')


# Create separate browsers for each BASKETBALL website needing to be accessed
tab_browser = webdriver.Firefox(service=tab_service, options=firefox_options)
pointsbet_browser = webdriver.Firefox(service=pointsbet_service, options=firefox_options)
unibet_browser = webdriver.Firefox(service=unibet_service, options=firefox_options)
ladbrokes_browser1 = webdriver.Firefox(service=ladbrokes_service1, options=firefox_options)
ladbrokes_browser2 = webdriver.Firefox(service=ladbrokes_service2, options=firefox_options)
ladbrokes_browser3 = webdriver.Firefox(service=ladbrokes_service3, options=firefox_options)
#tonybet_browser = webdriver.Firefox(service=tonybet_service, options=firefox_options)

# Create separate browsers for each TENNIS website needing to be accessed
tab_tennis_browser = webdriver.Firefox(service=tab_tennis_service, options=firefox_options)
pointsbet_tennis_browser = webdriver.Firefox(service=pointsbet_tennis_service, options=firefox_options)
unibet_tennis_browser = webdriver.Firefox(service=unibet_tennis_service, options=firefox_options)
ladbrokes_tennis_browser = webdriver.Firefox(service=ladbrokes_tennis_service, options=firefox_options)


# Set up paths for the TxtFiles for BASKETBALL
script_dir = os.path.dirname(os.path.abspath(__file__))
txt_files_folder = os.path.join(script_dir, "TxtFiles")

# Set up paths for the TxtFiles for TENNIS
script_tennis_dir = os.path.dirname(os.path.abspath(__file__))
tennis_txt_files_folder = os.path.join(script_dir, "TxtFilesTennis")


# Set up paths for the Tab
tab_file_name = "tabResults.txt"
tab_file_path = os.path.join(txt_files_folder, tab_file_name)
tab_tennis_file_path = os.path.join(tennis_txt_files_folder, tab_file_name)

# Set up path for Pointsbet
pointsbet_file_name = "pointsbetResults.txt"
pointsbet_file_path = os.path.join(txt_files_folder, pointsbet_file_name)
pointsbet_tennis_file_path = os.path.join(tennis_txt_files_folder, pointsbet_file_name)

# Set up path for Unibet
unibet_file_name = "unibetResults.txt"
unibet_file_path = os.path.join(txt_files_folder, unibet_file_name)
unibet_tennis_file_path = os.path.join(tennis_txt_files_folder, unibet_file_name)

# Set up path for Ladbrokes
ladbrokes_file_name = "ladbrokesResults.txt"
ladbrokes_file_path = os.path.join(txt_files_folder, ladbrokes_file_name)
ladbrokes_tennis_file_path = os.path.join(tennis_txt_files_folder, ladbrokes_file_name)

# Set up path for Tonybets
tonybet_file_name = "tonybetResults.txt"
tonybet_file_path = os.path.join(txt_files_folder, tonybet_file_name)

# Load TAB website
tab_browser.get("https://www.tab.co.nz/sport/8/basketball/matches")
tab_tennis_browser.get("https://www.tab.co.nz/sport/37/tennis/matches")

# Load PointsBet website
pointsbet_browser.get("https://pointsbet.com.au/sports/basketball")
pointsbet_tennis_browser.get("https://pointsbet.com.au/sports/tennis")

# Load Unibet website
unibet_browser.get("https://www.unibet.com/betting/sports/filter/basketball/all/matches")
unibet_tennis_browser.get("https://www.unibet.com/betting/sports/filter/tennis/all/matches")

# Load Labrokes website
ladbrokes_browser1.get("https://www.ladbrokes.com.au/sports/basketball/usa")
ladbrokes_browser2.get("https://www.ladbrokes.com.au/sports/basketball/international")
ladbrokes_browser3.get("https://www.ladbrokes.com.au/sports/basketball/australia")
ladbrokes_tennis_browser.get("https://www.ladbrokes.com.au/sports/tennis")

# Load TonyBet website
#tonybet_browser.get("https://tonybet.com/nz/prematch/basketball")

# Gives time for the browsers to be loaded
time.sleep(90)


# Method for scraping the odds from the website. @input: url, the websites url; container_name, the name of the container
# that needs to be scraped; browser, the name of the browser that was set up above.
def get_odds(url, container_name, browser):
    
    # Opens and close the browser
    print("Opening", url)
    page_source = browser.page_source # Update so only gets the needs page_source.
    print("Closing", url)

    # Uses BeautifulSoup to get the content of the page_source.
    soup = BeautifulSoup(page_source, "lxml")
    container = soup.find_all("div", class_ = container_name)
    container_contents = []

    # Checks if the container can be found and return results.
    if container:
        for container in container:
            # Extract the content of the container
            container_content = container.get_text()
            container_contents.append(container_content)
            container_contents.append("\n")
        return (container_contents)
    else:
        print("Container not found")

# Method for getting odds from the websites. Calls 'get_odds'.
choice = True
def perform_task():

    global choice
    
    if choice == True:
        choice = False

        # Gets odds for basketball scores from the TAB
        tab_odds = get_odds("https://www.tab.co.nz/sport/8/basketball/matches", "event-list event-list--vertical", tab_browser)
        print(tab_odds)
        upload_odds("tab", tab_odds, "Basketball")
        print("---------")

        # Gets odds for basketball scores from Pointsbet
        pointsbet_odds = get_odds("https://pointsbet.com.au/sports/basketball", "f3wis39", pointsbet_browser)
        print(pointsbet_odds)
        upload_odds("pointsbet", pointsbet_odds, "Basketball")
        print("---------")

        # Gets odds for basetball scores from Unibet
        unibet_odds = get_odds("https://www.unibet.com/betting/sports/filter/basketball/all/matches", "_28843", unibet_browser)
        print(unibet_odds)
        upload_odds("unibet", unibet_odds, "Basketball")
        print("---------")

        # Gets odds for basketball scores from Ladbrokes
        ladbrokes_odds1 = get_odds("https://www.ladbrokes.com.au/sports/basketball/usa", "sports-market-primary__prices-inner", ladbrokes_browser1)
        ladbrokes_odds2 = get_odds("https://www.ladbrokes.com.au/sports/basketball/international", "sports-market-primary__prices-inner", ladbrokes_browser2)
        ladbrokes_odds3 = get_odds("https://www.ladbrokes.com.au/sports/basketball/australia", "sports-market-primary__prices-inner", ladbrokes_browser3)
        ladbrokes_upload_odds(ladbrokes_odds1, ladbrokes_odds2, ladbrokes_odds3)
        print("---------")

        # Gets odds for basketball scores from Tonybets.
        #tonybet_odds = get_odds("https://tonybet.com/nz/prematch/basketball", "event-table__row", tonybet_browser)
        #upload_odds("tonybet", tonybet_odds)
    
    if choice == False:
        choice = True

        # Gets odds for tennis scores from the TAB
        tab_odds = get_odds("https://www.tab.co.nz/sport/37/tennis/matches", "event-list event-list--vertical", tab_tennis_browser)
        print(tab_odds)
        upload_odds("tab", tab_odds, "Tennis")
        print("---------")

        # Gets odds for tennis scores from Pointsbet
        #print(pointsbet_odds)
        #upload_odds("pointsbet", pointsbet_odds, "Tennis")
        #print("---------")

        # Gets odds for tennis scores from Unibet
        unibet_odds = get_odds("https://www.unibet.com/betting/sports/filter/tennis/all/matches", "c21a2", unibet_tennis_browser)
        print(unibet_odds)
        upload_odds("unibet", unibet_odds, "Tennis")
        print("---------")

        # Gets odds for tennis scores from Ladbrokes
        ladbrokes_odds = get_odds("https://www.ladbrokes.com.au/sports/tennis", "sports-market-primary__prices-inner", ladbrokes_tennis_browser)
        print(ladbrokes_odds)
        upload_odds("ladbrokes", ladbrokes_odds, "Tennis")
        print("("---------")")



# Method for importing the scraped odds to the desired txt file.
def upload_odds(website, odds, sport):
    
    # Upload Basketball odds
    if sport == "Basketball":
        file_path = tab_file_path if website == "tab" else pointsbet_file_path if website == "pointsbet" else unibet_file_path
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
        file_path = tab_tennis_file_path if website == "tab" else pointsbet_tennis_file_path if website == "pointsbet" else unibet_tennis_file_path if website == "unibet" else ladbrokes_tennis_file_path
        with open(file_path, "a") as file:
            file.truncate(0)
            if odds:
                for odd in odds:
                    file.write(str(odd))
                print("raw", website, "TENNIS stats have been scraped")
            else:
                print("raw", website, "TENNIS stats have NOT been scraped")


# Method for importing the scarped odds for ladbrokes.
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


# Start of the program.

i = 0
while i < 2 :

    print("Start of loop")
    # Generate a random time interval between two intervals.
    interval = random.randint(60, 120) # seconds random.randint(60, 120)  

    i += 1

    # Wait for the random interval before running the rest of the code.
    time.sleep(interval)
    print(interval)
        
    print("starting task")
    perform_task()
    print("finished task, number:", i)

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
    
# Once the program has been run i amount of times it must close the browsers.
else:
    tab_browser.quit()
    pointsbet_browser.quit()
    unibet_browser.quit()
    ladbrokes_browser1.quit()
    ladbrokes_browser2.quit()
    ladbrokes_browser3.quit()
    #tonybet_browser.quit()
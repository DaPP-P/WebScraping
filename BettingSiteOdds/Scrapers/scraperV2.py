import os
import time
import random
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# Initial admin. Set up with help from: https://www.youtube.com/watch?v=kpONBQ3muLg
user_agent = 'Mozilla/5.0 (X11; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/116.0'
firefox_driver = os.path.join(os.getcwd(), 'Drivers', 'geckodriver')
firefox_service = Service(firefox_driver)
firefox_options = Options()
firefox_options.set_preference('general.useragent.override', user_agent)
firefox_options.headless = True
browser = webdriver.Firefox(service=firefox_service, options=firefox_options)
browser.get("https://www.tab.co.nz/sport/8/basketball/matches")
time.sleep(20)

def get_odds(url, container_name):
    print("Opeing", url)
    #browser.get(url)
    #time.sleep(10)
    page_source = browser.page_source
    #browser.quit()
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
    tab_odds = get_odds("https://www.tab.co.nz/sport/8/basketball/matches", "event-list event-list--vertical")
    print(tab_odds)

while True:
    i = 0
    # Generate a random time interval between 1 and 2 minutes
    interval = random.randint(60, 120) # seconds random.randint(60, 120)  

    # Wait for the random interval
    time.sleep(interval)

    # Perform the task
    i += 1
    if i < 5:
        print("starting task")
        perform_task()
        print("finished task", i)
    else:
        browser.quit()
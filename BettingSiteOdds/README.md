# Betting Site Odds
Author: Daniel Prvanov

The aim of these programs is to create an automatic arbitrage opportunity finder. The main steps done to complete this process are:
1. Scrape the data from bookie websites.
2. Process the scraped data from bookie websites into a compatible format.
3. Compare data from different bookie websites to find arbitrage opportunities.
4. Placing the optimal bets on the bookie websites.

## Critical items of To-Do List

1. Set up Raspberry Pi and check how it runs with the program
2. REDO: CHOOSE A METHOD THAT GETS THE DATA QUICKER AT THE MOMENT TAKES A WHILE TO GET ALL THE DATA.
    * Potential solutions: have the websites already open so they don't need to be loaded or/and run all loadings of websites at the same time.
    * NOTE: This needs to be quick for linux, it can be slow for windows.

## 1. Scraping the Data

done using the file **Scraper.py**

**Initial Setup:**

Used this video (https://www.youtube.com/watch?v=kpONBQ3muLg) to set up a lot of the initial admin using Selenium and Beautiful Soup.

Neccasry packages:
```
import os
import time
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import platform
```

**How it works:**

**What Websites are Scraped:**

**To Do:**

* Need to set up the correct driver for my desktop. At the moment get output:
```
The version of firefox cannot be detected. Trying with latest driver version
```
* Remove bet365.
* Automatically close cookies button if detected.
* For either pointsbet or unibet if no information can be scraped scrape from a different location.
* Get rid of 'time.sleep' and use a more efficient method.
* Find out why TAB doesn't work on the first go.
* REDO: CHOOSE A METHOD THAT GETS THE DATA QUICKER AT THE MOMENT TAKES A WHILE TO GET ALL THE DATA.
    * Potential solutions: have the websites already open so they don't need to be loaded or/and run all loadings of websites at the same time.
    * NOTE: This needs to be quick for linux, it can be slow for windows.

## 2. Process the scraped data

done using the file **resultChecker.py**

**Inital Setup:**

Neccasry packages:
```
import re
```

**How it works:**

**What Websites are Scraped:**

**To Do:**

## 3. Compare data

done using the file **arbitrage.py**

**Inital Setup:**

Neccasry packages:
```
None
```

**How it works:**

**What Websites are Scraped:**

**To Do:**
* Make sure that both teams match not just one. Can bug out if the same team has several games avaible. Update following method:
```
# Method for finding matching games and adding them to a dictionary 
def find_same_games(bigList):
    seenList = []
    findList = []
    result_dict = {}

    # Find items in list[1] that occur more than once
    for lst in bigList:
        if lst[1] in seenList:
            findList.append(lst[1])
        seenList.append(lst[1])

    # Initialize empty lists in the result_dict for each item in findList
    for item in findList:
        result_dict[item] = []

    # Populate the result_dict with the lists containing the items from findList
    for lst in bigList:
        if lst[1] in findList:
            result_dict[lst[1]].append(lst)

    return result_dict
```

## Other Things:

### Raspberry Pi

* Set up Raspberry Pi and check how it runs with the program

### Brain

**brain.py**

* Find out why never works with TAB

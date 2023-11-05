# Betting Site Odds
Author: Daniel Prvanov

Using python version: python 3.9.13 64-bit

The aim of these programs is to create an automatic arbitrage opportunity finder. The main steps done to complete this process are:
1. Scrape the data from bookie websites.
2. Process the scraped data from bookie websites into a compatible format.
3. Compare data from different bookie websites to find arbitrage opportunities.
4. Placing the optimal bets on the bookie websites.

## Critical items of To-Do List

1. Set up script so that it auto runs when Pi is started.
2. Figure out how to process Pinnacle odds and maybe figure out why tony bet doesn't load properly (i'm assuming its got anti-scraping features).
3. Add Tennis odds, double the pool of odds available.
4. For Pointsbet make it switch to next up.
5. For unibet make it open all of the games.

## 1. Scraping the Data

done using the file **scraperV2.py**

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

1. First loads all the browser instances. 
2. Then on a loop calls perform_task which calls get_odds and upload_odds.
3. get_odds works by using BeautifulSoup to scrape the raw odds.
4. Then uploads the odds to the desired file using upload_odds.
5. Calls resultChecker.py
6. Calls arbitrage.py

**What Websites are Scraped:**

* TAB
* PointsBet
* UniBet
* LadBrokes
* TonyBet (if it wasn't a cunt)

**To Do:**

* Update:
```
  page_source = browser.page_source 
```
so that it only gets the part of page_source that is necessary.
* See if I can get TonyBet to work.
* Do it for tennis odds as well.

## 2. Process the scraped data

done using the file **resultChecker.py**

**Inital Setup:**

Neccasry packages:
```
import re
```

**How it works:**

Most of the heavy lifting done in the tiny_odds method.
* For each different website it formats the odds in to a readable and uniform format so that it can be processed in arbitrage.py.

**To Do:**

* Figure out how to process Pinnacle.

## 3. Compare data

done using the file **arbitrage.py**

**Inital Setup:**

Neccasry packages:
```
None
```

**How it works:**

* Checks the odds against each other websites odds and returns the best opportunity for each matchup and if the odds are profitable. 

**To Do:**

* Add Pinnacle or any other site if they added.
* Otherwise seems to be done for now.
* Note: not sure if master list is being updated, will need to keep an eye on.


# Raspberry Pi

* Set up so that ScraperV2 auto runs on boot.

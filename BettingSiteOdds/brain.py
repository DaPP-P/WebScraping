import os
import subprocess
import platform


# When scraping TAB from brain results are not scraped while when ran from Scraper 
# TAB results are gathered. :/ IDK why this is like this
scraper_path = "Scrapers/Scraper.py"
resultChecker_path = "resultChecker.py"
arbitrage_path = "arbitrage.py"

if platform.system() == "Windows":
    # Use 'start' command on Windows
    subprocess.run(["start",scraper_path], shell=True)
else:
    # Use 'open' command on macOS or Linux
    subprocess.run(["python3",scraper_path])
    print("Scraper Done")
    subprocess.run(["python3",resultChecker_path])
    print("Result Checker Done")
    print("------------------")
    print("ARBITRAGE RESULTS:")
    subprocess.run(["python3",arbitrage_path])




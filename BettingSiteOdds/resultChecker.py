import re

# Upload TAB Odds
tab_file_path = "TxtFiles/tabResults.txt"
tab_file = open(tab_file_path,"r")
tabFileIn = tab_file.read()
tabResults = tabFileIn.split("\n")
tab_file.close()

# Upload PointsBet Odds
pointsbet_file_path = "TxtFiles/pointsbetResults.txt"
pointsbet_file = open(pointsbet_file_path,"r")
pointsbetFileIn = pointsbet_file.read()
pointsbetResults = pointsbetFileIn.split("\n")
pointsbet_file.close()

# Upload LadBrokes Odds
ladbrokes_file_path = "TxtFiles/ladbrokesResults.txt"
ladbrokes_file = open(ladbrokes_file_path, "r")
ladbrokesFileIn = ladbrokes_file.read()
ladbrokesResults = ladbrokesFileIn.split("\n")
ladbrokes_file.close()

# Upload UniBet Odds
unibet_file_path = "TxtFiles/unibetResults.txt"
unibet_file = open(unibet_file_path, "r")
unibetFileIn = unibet_file.read()
unibetResults = unibetFileIn.split("\n")
unibet_file.close()


# Method for a clean upload
def cleanUpload(file, odds):
    for odd in odds:
        odd = str(odd).replace('[', '').replace(']', '').replace("'", "")
        if "N/A" not in odd:
            file.write(odd+"\n")
    file.close


# Method for finding where the betting odds are located
def find_word_positions(text, word):
    positions = []
    start = 0
    while start < len(text):
        index = text.find(word, start)
        if index == -1:
            break
        positions.append((index, index + len(word) - 1))
        start = index + 1
    return positions


# Method for tidying the odds
def tidyOdds(results, siteName, wordToSplit):
    
    # Output list
    firstItemResults = []

    # Splits Text Via wordToSplit
    results = results.replace("U19","U19 ")
    results = results.replace("u19","u19 ")
    results = results.replace(wordToSplit, "SPLITHERE")
    results = results.split("SPLITHERE")

    for string in results:

        # Finds odds As The First Two Decimal Formats
        findDecimalNumbers = re.findall(r'[0-9]*\.[0-9]+', string)
        odds = findDecimalNumbers[:2]
        
        # Checks if odds have been found. If they have not set the names to N/A
        if odds and siteName == "TAB":
            # Gets TeamOne
            positions = find_word_positions(string, odds[0])
            teamOneIsBefore = positions[0][0]
            teamOne = string[:teamOneIsBefore]
            # Gets TeamTwo
            positions = find_word_positions(string, odds[0])
            teamTwoIsAfter = positions[-1][1] + 1
            
            if len(odds) >= 2:
                positions2 = find_word_positions(string, odds[1])
                teamTwoIsBefore = positions2[0][0]
                teamTwo = string[teamTwoIsAfter:teamTwoIsBefore]
                # Gets TeamOne and TeamTwo Odds
                teamOneOdds, teamTwoOdds = odds
            else:
                teamTwo = "N/A"
                teamTwoOdds = 0.00

            # Checks if the odds are money lines and not head to head
            if teamOne[-1] == "-" or teamOne[-1] == "+":
                teamOne, teamTwo, teamOneOdds, teamTwoOdds = "N/A", "N/A", 0.00, 0.00
                
        elif odds and siteName == "Pointsbet": 
            # Removes words that may mess up the regex
            string = string.replace("Line", "")
            string = string.replace("total", "")
            string = string.replace("Ov ", "")
            string = string.replace("Un ", "")
            
            # Finds the team names and their odds
            pattern = r'([A-Za-z ]+)(\d+\.\d{2})'
            matches = re.findall(pattern, string)
            try:
                # Checks for live matches that mess up the odds. And Removes the live scores
                teamOne, teamOneOdds, teamTwo, teamTwoOdds = [item for match in matches for item in match]
                while len(teamOneOdds) > 4 and teamOneOdds[0].isnumeric():
                    teamOneOdds = teamOneOdds[1:]
                while len(teamTwoOdds) > 4 and teamTwoOdds[0].isnumeric():
                    teamTwoOdds = teamTwoOdds[1:]
            except:
                teamOne, teamOneOdds, teamTwo, teamTwoOdds = "N/A", 0.00, "N/A", 0.00

        elif odds and siteName == "LadBrokes":

            # If The Game is not a head to head and instead points line sets to N/A
            pattern = r'\([^)]*\)'
            
            if "Over" in string or "Under" in string:
                teamOne, teamOneOdds, teamTwo, teamTwoOdds = "N/A", 0.00, "N/A", 0.00
            elif re.search(pattern, string):
                teamOne, teamOneOdds, teamTwo, teamTwoOdds = "N/A", 0.00, "N/A", 0.00
            
            # Uses regex to find team names and odds
            else:
                try:
                    pattern = r'([A-Za-z0-9 ]+)[\t ]+([0-9.]+)'
                    matches = re.findall(pattern, string)
                    teamOne, teamOneOdds, teamTwo, teamTwoOdds = [item for match in matches for item in match]
                    teamOne, teamOneOdds, teamTwo, teamTwoOdds = teamOne.strip(), teamOneOdds.strip(), teamTwo.strip(), teamTwoOdds.strip()
                except:
                    teamOne, teamTwo, teamOneOdds, teamTwoOdds = "N/A", "N/A", 0.00, 0.00
        elif odds and siteName == "Unibet":
            string = string.replace("(W)", "Women ")
        else:
            teamOne = "N/A"
            teamTwo = "N/A"
            teamOneOdds = 0.00
            teamTwoOdds = 0.00

        # Appends and returns the tidy odds.
        firstItemResults.append([siteName, teamOne, teamTwo, teamOneOdds, teamTwoOdds])

    return firstItemResults


# Upload clean values for the TAB
tab_file_path = "TxtFiles/tabResultsCleaned.txt"
tab_file = open(tab_file_path, "w")
tab_file.truncate(0)

# The phrase used for splitting
target = "HandicapTotal"

# Odds for teams for TAB
for result in tabResults:
    if target in result:
        odds = tidyOdds(result, "TAB", target)
        cleanUpload(tab_file, odds)

tab_file.close()
print("TAB odds uploaded")
print("_________________")

# Upload clean values for pointsbet
pointsbet_file_path = "TxtFiles/pointsbetResultsCleaned.txt"
pointsbet_file = open(pointsbet_file_path, "w")
pointsbet_file.truncate(0)

# The phrase used for splitting

# Remove Line and total

target = "MarketsHead To Head"

all_results = []

# Odds for teams for pointsbet
for result in pointsbetResults:
    #result = result.replace("Line", "")
    #result = result.replace("total", "")
    if target in result:
        odds = tidyOdds(result, "Pointsbet", target)
        cleanUpload(pointsbet_file, odds)

pointsbet_file.close()
print("Pointsbet odds uploaded")
print("_________________")


# # Upload clean values for ladbrokes
ladbrokes_file_path = "TxtFiles/ladbrokesResultsCleaned.txt"
ladbrokes_file = open(ladbrokes_file_path, "w")

# # The phrase used for splitting

# # Remove Line and total

target = "NOSPLIT"

all_results = []
# #print(ladbrokesResults)
# # Odds for teams for ladbrokes
for result in ladbrokesResults:
    odds = tidyOdds(result, "LadBrokes", target)
    cleanUpload(ladbrokes_file, odds)

ladbrokes_file.close()
print("ladbrokes odds uploaded")
print("_________________")

# For tonybet, unibet and pinnacle I could save the info and check if those things are in a already saved team.

# Upload clean values for unibet
unibet_file_path = "TxtFiles/unibetResultsCleaned.txt"
unibet_file = open(unibet_file_path, "w")
unibet_file.truncate(0)

target = "Handicap"
all_results = []

for result in unibetResults:
    odds = tidyOdds(result, "Unibet", target)
    cleanUpload(unibet_file, odds)

unibet_file.close()
print("Unibet odds uploaded")
print("_________________")
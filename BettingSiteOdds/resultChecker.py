import re

# Upload Master Team List. This is needed for Unibet, Tonybets and Pinnacle
master_team_list_file = open("masterTeamList.txt", "r")
masterTeamListIn = master_team_list_file.read()
master_team_list = masterTeamListIn.split("\n")
master_team_list_file.close()

# Open TAB odds
# For basketball
tab_file_path = "TxtFiles/tabResults.txt"
tab_file = open(tab_file_path,"r")
tabFileIn = tab_file.read()
tabResults = tabFileIn.split("\n")
tab_file.close()
#For tennis
tennis_tab_file_path = "TxtFilesTennis/tabResults.txt"
tennis_tab_file = open(tennis_tab_file_path,"r")
tennis_tabFileIn = tennis_tab_file.read()
tennis_tabResults = tennis_tabFileIn.split("\n")
tennis_tab_file.close()

# Upload PointsBet Odds
# For basketball
pointsbet_file_path = "TxtFiles/pointsbetResults.txt"
pointsbet_file = open(pointsbet_file_path,"r")
pointsbetFileIn = pointsbet_file.read()
pointsbetResults = pointsbetFileIn.split("\n")
pointsbet_file.close()
# For tennis
tennis_pointsbet_file_path = "TxtFilesTennis/pointsbetResults.txt"
tennis_pointsbet_file = open(tennis_pointsbet_file_path,"r")
tennis_pointsbetFileIn = tennis_pointsbet_file.read()
tennis_pointsbetResults = tennis_pointsbetFileIn.split("\n")
tennis_pointsbet_file.close()

# Upload LadBrokes Odds
# For basketball
ladbrokes_file_path = "TxtFiles/ladbrokesResults.txt"
ladbrokes_file = open(ladbrokes_file_path, "r")
ladbrokesFileIn = ladbrokes_file.read()
ladbrokesResults = ladbrokesFileIn.split("\n")
ladbrokes_file.close()
# For tennis
tennis_ladbrokes_file_path = "TxtFilesTennis/ladbrokesResults.txt"
tennis_ladbrokes_file = open(tennis_ladbrokes_file_path, "r")
tennis_ladbrokesFileIn = tennis_ladbrokes_file.read()
tennis_ladbrokesResults = tennis_ladbrokesFileIn.split("\n")
tennis_ladbrokes_file.close()

# Upload UniBet Odds
# For basketball
unibet_file_path = "TxtFiles/unibetResults.txt"
unibet_file = open(unibet_file_path, "r")
unibetFileIn = unibet_file.read()
unibetResults = unibetFileIn.split("\n")
unibet_file.close()
# For tennis
tennis_unibet_file_path = "TxtFilesTennis/unibetResults.txt"
tennis_unibet_file = open(tennis_unibet_file_path, "r")
tennis_unibetFileIn = tennis_unibet_file.read()
tennis_unibetResults = tennis_unibetFileIn.split("\n")
tennis_unibet_file.close()

# Upload Tonybet Odds
# For basketball
tonybet_file_path = "TxtFiles/tonybetResults.txt"
tonybet_file = open(tonybet_file_path, "r", encoding="iso-8859-1")
tonybetFileIn = tonybet_file.read()
tonybetResults = tonybetFileIn.split("\n")
tonybet_file.close()
# For tennis
tennis_tonybet_file_path = "TxtFilesTennis/tonybetResults.txt"
tennis_tonybet_file = open(tennis_tonybet_file_path, "r", encoding="iso-8859-1")
tennis_tonybetFileIn = tennis_tonybet_file.read()
tennis_tonybetResults = tennis_tonybetFileIn.split("\n")
tennis_tonybet_file.close()

# Method for a clean upload
def clean_upload(file, odds):
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
def tidy_odds(results, site_name, wordToSplit):
    
    # Output list
    first_item_results = []

    # Splits Text Via wordToSplit
    results = results.replace("U19","U19 ")
    results = results.replace("u19","u19 ")
    results = results.replace(wordToSplit, "SPLITHERE")
    results = results.split("SPLITHERE")

    for string in results:

        # Finds odds As The First Two Decimal Formats
        find_decimal_numbers = re.findall(r'[0-9]*\.[0-9]+', string)
        odds = find_decimal_numbers[:2]
        
        # Checks if odds have been found. If they have not set the names to N/A
        if odds and site_name == "TAB":
            # Gets team_one
            positions = find_word_positions(string, odds[0])
            team_one_is_before = positions[0][0]
            team_one = string[:team_one_is_before]
            # Gets team_two
            positions = find_word_positions(string, odds[0])
            team_two_is_after = positions[-1][1] + 1
            
            if len(odds) >= 2:
                positions2 = find_word_positions(string, odds[1])
                team_two_is_before = positions2[0][0]
                team_two = string[team_two_is_after:team_two_is_before]
                # Gets team_one and team_two Odds
                team_one_odds, team_two_odds = odds
            else:
                team_two = "N/A"
                team_two_odds = 0.00

            # Checks if the odds are money lines and not head to head
            if team_one[-1] == "-" or team_one[-1] == "+":
                team_one, team_two, team_one_odds, team_two_odds = "N/A", "N/A", 0.00, 0.00
                
        elif odds and site_name == "Pointsbet": 
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
                team_one, team_one_odds, team_two, team_two_odds = [item for match in matches for item in match]
                while len(team_one_odds) > 4 and team_one_odds[0].isnumeric():
                    team_one_odds = team_one_odds[1:]
                while len(team_two_odds) > 4 and team_two_odds[0].isnumeric():
                    team_two_odds = team_two_odds[1:]
            except:
                team_one, team_one_odds, team_two, team_two_odds = "N/A", 0.00, "N/A", 0.00

        elif odds and site_name == "LadBrokes":

            # If The Game is not a head to head and instead points line sets to N/A
            pattern = r'\([^)]*\)'
            
            if "Over" in string or "Under" in string:
                team_one, team_one_odds, team_two, team_two_odds = "N/A", 0.00, "N/A", 0.00
            elif re.search(pattern, string):
                team_one, team_one_odds, team_two, team_two_odds = "N/A", 0.00, "N/A", 0.00
            
            # Uses regex to find team names and odds
            else:
                try:
                    pattern = r'([A-Za-z0-9 ]+)[\t ]+([0-9.]+)'
                    matches = re.findall(pattern, string)
                    team_one, team_one_odds, team_two, team_two_odds = [item for match in matches for item in match]
                    team_one, team_one_odds, team_two, team_two_odds = team_one.strip(), team_one_odds.strip(), team_two.strip(), team_two_odds.strip()
                except:
                    team_one, team_two, team_one_odds, team_two_odds = "N/A", "N/A", 0.00, 0.00
        elif odds and site_name == "Unibet":
            string = string.replace("(W)", "Women ")

            # Regex for finding teams that are in the master team list.
            consecutive_pattern = r'({})({})'.format('|'.join(master_team_list), '|'.join(master_team_list))
            consecutive_teams = re.findall(consecutive_pattern, string)

            # Finds team names
            if consecutive_teams:
                for team_pair in consecutive_teams:
                    if team_pair[0] and team_pair[1]:
                        team_one = team_pair[0]
                        team_two = team_pair[1]

            # Finds odds for the teams
            end_of_team_two = string.find(team_two) + len(team_two)
            next_eight_items = string[end_of_team_two:end_of_team_two + 8]
            if next_eight_items[1] == ".":
                team_one_odds = next_eight_items[0:4]
                team_two_odds = next_eight_items[4:8]
            else:
                team_one_odds = 0.00
                team_two_odds = 0.00

        elif odds and site_name == "Tonybet":
            # Regex for finding teams that are in the master team list.
            consecutive_pattern = r'({})({})'.format('|'.join(master_team_list), '|'.join(master_team_list))
            consecutive_teams = re.findall(consecutive_pattern, string)

            team_one = "N/A"
            team_two = "N/A"
            team_one_odds = 0.00
            team_two_odds = 0.00

            # Finds team names
            if consecutive_teams:
                for team_pair in consecutive_teams:
                    if team_pair[0] and team_pair[1]:
                        team_one = team_pair[0]
                        team_two = team_pair[1]
            
            # Finds the positions of '.' which can be used for odds
            positions = []
            for i in range(len(string)):
                if string[i] == '.':
                    positions.append(i)
            
            # Odds positions
            position1 = positions[0]
            position2 = positions[1]
            
            # Sets the team_one and team_two odds
            team_one_odds = string[position1-1:position1+3]
            team_two_odds = string[position2-1:position2+3]

        else:
            team_one = "N/A"
            team_two = "N/A"
            team_one_odds = 0.00
            team_two_odds = 0.00

        # Appends and returns the tidy odds.
        first_item_results.append([site_name, team_one, team_two, team_one_odds, team_two_odds])

    return first_item_results


# Upload clean values for the TAB
# For basketball
tab_file_path = "TxtFiles/tabResultsCleaned.txt"
tab_file = open(tab_file_path, "w")
tab_file.truncate(0)
# for tennis
tennis_tab_file_path = "TxtFilesTennis/tabResultsCleaned.txt"
tennis_tab_file = open(tennis_tab_file_path, "w")
tennis_tab_file.truncate(0)

# The phrase used for splitting
target = "HandicapTotal"

# Odds for teams for TAB
for result in tabResults:
    if target in result:
        odds = tidy_odds(result, "TAB", target)
        clean_upload(tab_file, odds)

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
        odds = tidy_odds(result, "Pointsbet", target)
        clean_upload(pointsbet_file, odds)

pointsbet_file.close()
print("Pointsbet odds uploaded")
print("_________________")


# Upload clean values for ladbrokes
# For basketball
ladbrokes_file_path = "TxtFiles/ladbrokesResultsCleaned.txt"
ladbrokes_file = open(ladbrokes_file_path, "w")
ladbrokes_file.truncate(0)
# For tennis
tennis_ladbrokes_file_path = "TxtFilesTennis/ladbrokesResultsCleaned.txt"
tennis_ladbrokes_file = open(tennis_ladbrokes_file_path, "w")
tennis_ladbrokes_file.truncate(0)

# The phrase used for splitting

# Remove Line and total

target = "NOSPLIT"

all_results = []
# #print(ladbrokesResults)
# # Odds for teams for ladbrokes
for result in ladbrokesResults:
    odds = tidy_odds(result, "LadBrokes", target)
    clean_upload(ladbrokes_file, odds)
ladbrokes_file.close()
print("Ladbrokes basketball odds uploaded")

for result in tennis_ladbrokesResults:
    odds = tidy_odds(result, "LadBrokes", target)
    clean_upload(tennis_ladbrokes_file, odds)
tennis_ladbrokes_file.close()
print("Ladbrokes tennis odds uploaded")

print("All Ladbrokes odds uploaded")
print("_________________")

# For tonybet, unibet and pinnacle I could save the info and check if those things are in a already saved team.

# Upload clean values for unibet
# For basketball
unibet_file_path = "TxtFiles/unibetResultsCleaned.txt"
unibet_file = open(unibet_file_path, "w")
unibet_file.truncate(0)
# For tennis
tennis_unibet_file_path = "TxtFilesTennis/unibetResultsCleaned.txt"
tennis_unibet_file = open(tennis_unibet_file_path, "w")
tennis_unibet_file.truncate(0)

target = ":"
all_results = []

for result in unibetResults:
    odds = tidy_odds(result, "Unibet", target)
    clean_upload(unibet_file, odds)
unibet_file.close()
print("Unibet basketball odds uploaded")

for result in tennis_unibetResults:
    odds = tidy_odds(result, "Unibet", target)
    clean_upload(tennis_unibet_file, odds)
tennis_unibet_file.close()
print("Unibet tennis odds uploaded")

print("All Unibet odds uploaded")
print("_________________")

# Upload clean values for tonybet
tonybet_file_path = "TxtFiles/tonybetResultsCleaned.txt"
tonybet_file = open(tonybet_file_path, "w")
tonybet_file.truncate(0)

target = ":"
all_results = []

for result in tonybetResults:
    odds = tidy_odds(result, "Tonybet", target)
    clean_upload(tonybet_file, odds)
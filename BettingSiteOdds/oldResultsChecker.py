import re

# USE PYTHON 3.11.4 64-bit

# Useful Lists :  RENAME TO NBA/WNBA TEAMS
listOfNBATeams = ["Celtics", "Nets", "Knicks", "76ers", "Raptors", "Bulls", "Cavaliers", "Pistons", "Pacers", "Bucks", "Hawks", "Hornets", "Heat", "Magic", "Wizards", "Nuggets", "Timberwolves", "Thunder", "Trail Blazers", "Jazz", "Warriors", "Clippers", "Lakers", "Suns", "Kings", "Mavericks", "Rockets", "Grizzlies", "Pelicans", "Spurs", "Dream", "Sky", "Fever", "Liberty", "Mystics", "Wings", "Aces", "Sparks", "Lynx", "Mercury"]
#, "Storm", "Tuatara", "Rams", "Bulls", "Jets", "Giants", "Sharks", "Airs", "Saints", "36ers", "Bullets", "Taipans", "United", "Breakers", "Wildcats", "Phoenix", "JackJumpers"]
listOfCitys = ["Boston","Brooklyn", "New York", "Philadelphia", "Toronto", "Chicago", "Detroit", "Indiana", "Milwaukee", "Atlanta", "Charlotte", "Miami", "Orlando", "Washington", "Denver", "Minnesota", "Oklahoma City", "Portland", "Utah", "Golden State", "LA", "Los Angeles", "Phoenix", "Sacramento", "Dallas", "Houston", "Memphis", "New Orleans", "San Antonio", "Connecticut", "Indiana", "Las Vegas", "Seattle", "Auckland", "Canterbury", "Franklin", "Hawke's Bay", "Manawatu", "Nelson","Otago", "Southland","Tarnaki", "Wellington","Adelaide", "Brisbane", "Cairns","Illawarra","Melbourne","NZ","New Zealand", "Perth","South", "East", "Melbourne", "SE", "Sydney", "Tasmania"]

# Words that need to be removed for TAB
tabWordsToRemove  = ["Summer","League3","League4","League5", "League6", "League7", "Tomorrow","4Options" ,"5Options","Options"]

#tabWordsToRemove.extend(listOfCitys)
pointsbetWordsToRemove  = ["WNBATomorrow" ,"MarketsHead" ,"To" ,"HeadLinetotal" ,"," ,"Summer","League3","League4","League5", "League6", "League7", "Tomorrow","4Options","Options"]
pointsbetWordsToRemove.extend(listOfCitys)

# Words that need to be removed for bet365

# Words that need to be removed for pinnacle


# Upload results to be cleaned

# TAB odds
tab_file_path = "TxtFiles/tabResults.txt"
tab_file = open(tab_file_path,"r")
tabFileIn = tab_file.read()
tabResults = tabFileIn.split("\n")
tab_file.close()

# Bet365 odds
bet365_file_path = "TxtFiles/bet365Results.txt"
bet365_file = open(bet365_file_path,"r")
bet365Results = bet365_file.read()
bet365Results = bet365Results.split("\n")
bet365_file.close()

# Pinnacle odds
pinnacle_file_path = "TxtFiles/pinnacleResults.txt"
pinnacle_file = open(pinnacle_file_path,"r")
pinnacleResults = pinnacle_file.read()
pinnacleResults = pinnacleResults.split("\n")
pinnacle_file.close()

# PointsBet odds
pointsbet_file_path = "TxtFiles/pointsbetResults.txt"
pointsbet_file = open(pointsbet_file_path,"r")
pointsbetResults = pointsbet_file.read()
pointsbetResults = pointsbetResults.split("\n")
pointsbet_file.close()

# UniBet odds
unibet_file_path = "TxtFiles/unibetResults.txt"
unibet_file = open(unibet_file_path,"r")
unibetResults = unibet_file.read()
unibetResults = unibetResults.split("\n")
unibet_file.close()

# Method for a clean upload
def cleanUpload(file):
    for odd in odds:
        odd = str(odd).replace('[', '').replace(']', '').replace("'", "")
        file.write(odd+"\n")
    file.close

# Method for tidying the TAB NBA odds
def tidyTabOddsNBA(tabResults):
    
    # Output list
    firstItemResults = []  # 0 = team1, 1 = team1 odds, 3 = team2, 4 = team2 odds

    # Remove unwanted words
    for word in tabWordsToRemove:
        tabResults = tabResults.replace(word, "")

    # Split tabResults
    tabResults = tabResults.split("NBA")
    tabResults = [string.lstrip() for string in tabResults]
    tabResults.pop()

    # Seperate team names and words that need to be separated
    for string in tabResults:
        for team in listOfNBATeams:
            string = string.replace(team+"", team + " ")
        for city in listOfCitys:
            string = string.replace(city, " "+city)

        string = string.replace("Trail Blazers", "Trailblazers")
        string = string.replace("New York", "NewYork")
        string = string.replace("Oklahoma City", "OklahomaCity")
        string = string.replace("Golden State", "GoldenState")
        string = string.replace("Los Angeles", "LosAngeles")
        string = string.replace("New Orleans", "NewOrleans")
        string = string.replace("San Antonio", "SanAntonio")
        string = string.replace("Las Vegas", "LasVegas")
        string = string.replace("Hawke's Bay", "Hawke'sBay")
        string = string.replace("New Zealand", "NewZealand")

        string = string.replace("HeadHandicapTotal", "Head Handicap Total")

        # Finds odds
        findDecimalNumbers = re.findall(r'\d+\.\d+', string)

        # Splits team name and odds into firstItemResults
        for line in string.split("\n"):
            words = line.split()
            if words:
                try:
                    first_team = words[0]
                    first_team2 = words[1]
                    second_team = words[3]
                    second_team2 = words[4]
                    odds = findDecimalNumbers[:2]
                    firstItemResults.append([first_team,first_team2,second_team, second_team2, *odds])
                except IndexError:
                    print("List index out of range.")
    return firstItemResults

# Method for tidying the PointsBet NBA odds
def tidyPointsbetOddsNBA(pointsbetResults):
    # Output list
    firstItemResults = []  # 0 = team1, 1 = team1 odds, 3 = team2, 4 = team2 odds

    # Remove unwanted words
    for word in pointsbetWordsToRemove:
        pointsbetResults = pointsbetResults.replace(word, "")

    # Seperate team names and words that need to be separated
    for team in listOfNBATeams:
        pointsbetResults = pointsbetResults.replace(team, team + " ")
    pointsbetResults = pointsbetResults.replace("HeadHandicapTotal", "Head Handicap Total")

    # Finds odds
    findDecimalNumbers = re.findall(r'\d+\.\d+', pointsbetResults)
    
    # Splits team name and odds into firstItemResults
    words = pointsbetResults.split()
    first_team = words[0]
    second_team = words[2]
    first_team_odds = findDecimalNumbers[0]
    second_team_odds = findDecimalNumbers[3]
    firstItemResults.append([first_team, second_team, first_team_odds, second_team_odds])

    return firstItemResults

# Method for tidying the uniBet NBA odds
def tidyUnibetOddsNBA(unibetResults):

    # Output list
    firstItemResults = []  # 0 = team1, 1 = team1 odds, 3 = team2, 4 = team2 odds
    

    for team in listOfNBATeams:
        unibetResults = unibetResults.replace(team+"", team + " ")
    
    for city in listOfCitys:
        unibetResults = unibetResults.replace(city, " "+city)
    
    # Join city names with '|', escape special characters
    #city_pattern = "|".join(re.escape(city) for city in listOfCitys)

    # Find the city names in the string and remove preceding text
    #unibetResults = re.sub(fr"^(.*?{city_pattern})", r"\1", unibetResults)
    
    for city in listOfCitys:
        index = unibetResults.find(city)
        if index != -1:
            unibetResults = unibetResults[index + len(city):]
            break
    
    print(unibetResults)

    # string = unibetResults
    # string = string.replace("Trail Blazers", "Trailblazers")
    # string = string.replace("New York", "NewYork")
    # string = string.replace("Oklahoma City", "OklahomaCity")
    # string = string.replace("Golden State", "GoldenState")
    # string = string.replace("Los Angeles", "LosAngeles")
    # string = string.replace("New Orleans", "NewOrleans")
    # string = string.replace("San Antonio", "SanAntonio")
    # string = string.replace("Las Vegas", "LasVegas")
    # string = string.replace("Hawke's Bay", "Hawke'sBay")
    # string = string.replace("New Zealand", "NewZealand")

    return firstItemResults


# Upload clean values for the TAB
tab_file_path = "TxtFiles/tabResultsCleaned.txt"
tab_file = open(tab_file_path, "w")
tab_file.write("TAB\n")

# Odds for NBA teams for TAB
for result in tabResults:
    if "NBA Summer League" in result: 
        odds = tidyTabOddsNBA(result)
        cleanUpload(tab_file)
#        print("Tidy odds uploaded. Odds are:")
#        print(tidyTabOddsNBA(result))

# Odds for WNBA teams for TAB
for result in tabResults:
    if "WNBA" in result: 
        odds = tidyTabOddsNBA(result)
        cleanUpload(tab_file)
#        print("Tidy odds uploaded. Odds are:")
 #       print(tidyTabOddsNBA(result))


# Closes file
tab_file.close()
print("--------------------------------------------------------------------------")

# Upload clean values for Bet365

# Upload clean values for Pinnacle

# Upload clean values for PointsBet
pointsbet_file_path = "TxtFiles/pointsbetResultsCleaned.txt"
pointsbet_file = open(pointsbet_file_path, "w")
pointsbet_file.write("PointsBet\n")

# Uploads results for WNBA teams for PointsBet
for result in pointsbetResults:
    if sum(word in result for word in listOfNBATeams) == 2: 
        odds = tidyPointsbetOddsNBA(result)
        cleanUpload(pointsbet_file)
#        print("Tidy odds uploaded. Odds are:")
#        print(tidyPointsbetOddsNBA(result))

# Closes file
pointsbet_file.close()
print("--------------------------------------------------------------------------")


# Upload clean values for Unibet
unibet_file_path = "TxtFiles/unibetResultsCleaned.txt"
unibet_file = open(unibet_file_path, "w")
unibet_file.write("Unibet\n")

# Uploads results for NBA teams for Unibet
for result in unibetResults:
    odds = tidyUnibetOddsNBA(result)
    cleanUpload(unibet_file)
    print("Tidy odds uploaded. Odds are:")
    #print(tidyUnibetOddsNBA(result))

# Closes file
unibet_file.close()
print("--------------------------------------------------------------------------")
import datetime
import git
import platform
import os

system_name = platform.system()
current_dir = os.path.abspath(os.path.dirname(__file__))
repo_path = '/home/daniel/WebScraping'

# Master team name list
masterTeamList_file_path = "masterTeamList.txt"
masterTeamList_file = open(masterTeamList_file_path, "r")
masterTeamListFileIn = masterTeamList_file.read()
masterTeamList = masterTeamListFileIn.split("\n")
masterTeamList_file.close()

# TAB cleaned odds
tab_file_path = "TxtFiles/tabResultsCleaned.txt"
tab_file = open(tab_file_path,"r")
tabFileIn = tab_file.read()
tabResults = tabFileIn.split("\n")
tab_file.close()

# Bet365 cleaned odds
bet365_file_path = "TxtFiles/bet365ResultsCleaned.txt"
bet365_file = open(bet365_file_path,"r")
bet365FileIn = bet365_file.read()
bet365Results = bet365FileIn.split("\n")
bet365_file.close()

# Pinnacle cleaned odds
pinnacle_file_path = "TxtFiles/pinnacleResultsCleaned.txt"
pinnacle_file = open(pinnacle_file_path,"r")
pinnacleFileIn = pinnacle_file.read()
pinnacleResults = pinnacleFileIn.split("\n")
pinnacle_file.close()

# PointsBet cleaned odds
pointsbet_file_path = "TxtFiles/pointsbetResultsCleaned.txt"
pointsbet_file = open(pointsbet_file_path,"r")
pointsbetFileIn = pointsbet_file.read()
pointsbetResults = pointsbetFileIn.split("\n")
pointsbet_file.close()

# LabBrokes cleaned odds
ladbrokes_file_path = "TxtFiles/ladbrokesResultsCleaned.txt"
ladbrokes_file = open(ladbrokes_file_path,"r")
ladbrokesFileIn = ladbrokes_file.read()
ladbrokesResults = ladbrokesFileIn.split("\n")
ladbrokes_file.close()

# Unibet cleaned odds
unibet_file_path = "TxtFiles/unibetResultsCleaned.txt"
unibet_file = open(unibet_file_path,"r")
unibetFileIn = unibet_file.read()
unibetResults = unibetFileIn.split("\n")
unibet_file.close()

# Tonybet cleaned odds
tonybet_file_path = "TxtFiles/tonybetResultsCleaned.txt"
tonybet_file = open(tonybet_file_path,"r")
tonybetFileIn = tonybet_file.read()
tonybetResults = tonybetFileIn.split("\n")
tonybet_file.close()

# Method for removing empty lists in a list of lists
def remove_empty_lists(list_of_lists):
    result = []
    for sublist in list_of_lists:
        if sublist != ['']:
            result.append(sublist)
    return result

# Method for finding matching games and adding them to a dictionary 
def find_same_games(bigList):
    seenList = []
    findList = []
    result_dict = {}

    # Find items in list[1] and list[2] that occur more than once
    for lst in bigList:
        if (lst[1], lst[2]) in seenList:
            findList.append((lst[1], lst[2]))
        seenList.append((lst[1], lst[2]))

    # Initialize empty lists in the result_dict for each item in findList
    for item in findList:
        result_dict[item] = []

    # Populate the result_dict with the lists containing the items from findList
    for lst in bigList:
        if (lst[1], lst[2]) in findList:
            result_dict[(lst[1], lst[2])].append(lst)

    return result_dict

# Method that returns the best odds that can be used for arbitrage
def getBestOdds(matchingGames):
    outputResults = []
    for games in matchingGames.values():
        
        # Sets variables to nothing TxtFiles
        teamOne = ""
        teamTwo = ""
        highestTeamOneOdds = 0.00
        highestTeamOneSite = ""
        highestTeamTwoOdds = 0.00
        highestTeamTwoSite = ""

        for game in games:
            teamOne = game[1]
            teamTwo = game[2]
            if float(game[3]) > highestTeamOneOdds:
                highestTeamOneOdds = float(game[3])
                highestTeamOneSite = game[0]
            if float(game[4]) > highestTeamTwoOdds:
                highestTeamTwoOdds = float(game[4])
                highestTeamTwoSite = game[0]

        outputResults.append([teamOne, teamTwo, highestTeamOneSite, highestTeamTwoSite, highestTeamOneOdds, highestTeamTwoOdds])
    return outputResults


# Method for completing the arbitrage using the best odds
def arbitrage(list):
    current_time = datetime.datetime.now().time()
    current_time = current_time.strftime("%H:%M")
    outputResults = []
    for line in list:
        teamOneArbitrage = 100/float(line[4])
        teamTwoArbitrage = 100/float(line[5])
        cost = (teamOneArbitrage + teamTwoArbitrage)
        if cost < 100:
            profitable = "YES"
            profit = 100 - cost
        else:
            profitable = "NO"
            profit = 0
        outputResults.append([line[0], line[1], line[2], line[3], line[4], line[5], round(teamOneArbitrage,2), round(teamTwoArbitrage,2), round(cost,2), profitable, round(profit,2), current_time])
    return outputResults


# Combining lists together
allResults = tabResults + bet365Results + pinnacleResults + pointsbetResults + ladbrokesResults + unibetResults + tonybetResults

#Splits via ","
newAllResults = []
for item in allResults:
    newAllResults.append(item.split(","))

allResults = remove_empty_lists(newAllResults)

# Find all teams that have been found in easily splittable sites and check if they
# are in the not easily splittable sites.
listOfAllTeams = []
for team in allResults:
    listOfAllTeams.append(team[1].strip())
    listOfAllTeams.append(team[2].strip())

# This updates the master team lists so that I can save all teams that are ever on
# Tab, pointsbet or Ladbrokes.
masterTeamList_file = open(masterTeamList_file_path, "a")
if listOfAllTeams:
    for team in listOfAllTeams:
        if team not in masterTeamList:
            masterTeamList_file.write(str(team))
            masterTeamList_file.write(str("\n"))
masterTeamList_file.close()


matchingGames = find_same_games(allResults)
listToArbitrage = (getBestOdds(matchingGames))

arbitrageResults = "TxtFiles/arbitrageResults.txt"
arbitrageResults_file = open(arbitrageResults, "a")

profitableArbitrageResults = "TxtFiles/profitableArbitrageResults.txt"
profitableArbitrageResults_file = open(profitableArbitrageResults, "a")

has_profitable_result = False

results = arbitrage(listToArbitrage)
for result in results:
    arbitrageResults_file.write(str(result) + '\n')
print(results)
print("----")
print("Profitable: ")
for result in results:
    if result[9] == "YES":
        profitableArbitrageResults_file.write(str(result) + '\n')
        if system_name == "Linux":
            has_profitable_result = True
        
        print(result)

if has_profitable_result and system_name == "Linux":
    repo = git.Repo(repo_path)
    profitable_file_path = 'BettingSiteOdds/TxtFiles/profitableArbitrageResults.txt'
    repo.index.add([profitable_file_path])
    repo.index.commit("AUTOMATIC: Profitable Arbitrage Found")
    origin = repo.remote('origin')
    origin.push()
    
    has_profitable_result == False

arbitrageResults_file.close()
profitableArbitrageResults_file.close()
import datetime
import git
import platform
import os

system_name = platform.system()
current_dir = os.path.abspath(os.path.dirname(__file__))
repo_path = '/home/daniel/WebScraping'

def readFile(path):
    file = open(path, "r")
    fileIn = file.read()
    list = fileIn.split("\n")
    file.close()
    return list

# Master team name list
master_team_list = readFile("masterTeamList.txt")

# TAB cleaned odds
tabResults = readFile("TxtFiles/tabResultsCleaned.txt")
tennis_tabResults = readFile("TxtFilesTennis/tabResultsCleaned.txt")

# Bet365 cleaned odds
bet365Results = readFile("TxtFiles/bet365ResultsCleaned.txt")
tennis_bet365Results = readFile("TxtFilesTennis/bet365ResultsCleaned.txt")

# Pinnacle cleaned odds
pinnacleResults = readFile("TxtFiles/pinnacleResultsCleaned.txt")
tennis_pinnacleResults = readFile("TxtFilesTennis/pinnacleResultsCleaned.txt")

# PointsBet cleaned odds
pointsbetResults = readFile("TxtFiles/pointsbetResultsCleaned.txt")
tennis_pointbetResults = readFile("TxtFilesTennis/pointsbetResultsCleaned.txt")

# LabBrokes cleaned odds
# For basketball
ladbrokesResults = readFile("TxtFiles/ladbrokesResultsCleaned.txt")
tennis_ladbrokesResults = readFile("TxtFilesTennis/ladbrokesResultsCleaned.txt")

# Unibet cleaned odds
unibetResults = readFile("TxtFiles/unibetResultsCleaned.txt")
tennis_unibetResults = readFile("TxtFilesTennis/unibetResultsCleaned.txt")

# Tonybet cleaned odds
tonybetResults = readFile("TxtFiles/tonybetResultsCleaned.txt")
tennis_tonybetResults = readFile("TxtFilesTennis/tonybetResultsCleaned.txt")

# Method for removing empty lists in a list of lists
def remove_empty_lists(list_of_lists):
    result = []
    for sublist in list_of_lists:
        if sublist != ['']:
            result.append(sublist)
    return result

# Method for finding matching games and adding them to a dictionary 
def find_same_games(big_list):
    seen_list = []
    find_list = []
    result_dict = {}

    # Find items in list[1] and list[2] that occur more than once
    for lst in big_list:
        if (lst[1], lst[2]) in seen_list:
            find_list.append((lst[1], lst[2]))
        seen_list.append((lst[1], lst[2]))

    # Initialize empty lists in the result_dict for each item in find_list
    for item in find_list:
        result_dict[item] = []

    # Populate the result_dict with the lists containing the items from find_list
    for lst in big_list:
        if (lst[1], lst[2]) in find_list:
            result_dict[(lst[1], lst[2])].append(lst)

    return result_dict

# Method that returns the best odds that can be used for arbitrage
def get_best_odds(matching_games):
    output_results = []
    for games in matching_games.values():
        
        # Sets variables to nothing TxtFiles
        team_one = ""
        team_two = ""
        highest_team_one_odds = 0.00
        highest_team_one_site = ""
        highest_team_two_odds = 0.00
        highest_team_two_site = ""

        for game in games:
            team_one = game[1]
            team_two = game[2]
            if float(game[3]) > highest_team_one_odds:
                highest_team_one_odds = float(game[3])
                highest_team_one_site = game[0]
            if float(game[4]) > highest_team_two_odds:
                highest_team_two_odds = float(game[4])
                highest_team_two_site = game[0]

        output_results.append([team_one, team_two, highest_team_one_site, highest_team_two_site, highest_team_one_odds, highest_team_two_odds])
    return output_results


# Method for completing the arbitrage using the best odds
def arbitrage(list):
    current_time = datetime.datetime.now().time()
    current_time = current_time.strftime("%H:%M")
    output_results = []
    for line in list:
        if line[4] != 0 and line[5] != 0:
            team_one_arbitrage = 100/float(line[4])
            team_two_arbitrage = 100/float(line[5])
        cost = (team_one_arbitrage + team_two_arbitrage)
        if cost < 100:
            profitable = "YES"
            profit = 100 - cost
        else:
            profitable = "NO"
            profit = 0
        output_results.append([line[0], line[1], line[2], line[3], line[4], line[5], round(team_one_arbitrage,2), round(team_two_arbitrage,2), round(cost,2), profitable, round(profit,2), current_time])
    return output_results


# Combining lists together
all_results = tabResults + bet365Results + pinnacleResults + pointsbetResults + ladbrokesResults + unibetResults + tonybetResults
tennis_all_results = tennis_tabResults + tennis_bet365Results + tennis_pinnacleResults + tennis_pointbetResults + tennis_ladbrokesResults + tennis_unibetResults + tennis_tonybetResults

all_results = all_results + tennis_all_results

#Splits via ","
new_all_results = []
for item in all_results:
    new_all_results.append(item.split(","))

all_results = remove_empty_lists(new_all_results)

# Find all teams that have been found in easily splittable sites and check if they
# are in the not easily splittable sites.
list_of_all_teams = []
for team in all_results:
    list_of_all_teams.append(team[1].strip())
    list_of_all_teams.append(team[2].strip())

# This updates the master team lists so that I can save all teams that are ever on
# Tab, pointsbet or Ladbrokes.
master_team_list_file = open("masterTeamList.txt", "a")
if list_of_all_teams:
    for team in list_of_all_teams:
        if team not in master_team_list:
            master_team_list_file.write(str(team))
            master_team_list_file.write(str("\n"))
master_team_list_file.close()


matching_games = find_same_games(all_results)
list_to_arbitrage = (get_best_odds(matching_games))

arbitrageResults = "TxtFiles/arbitrageResults.txt"
arbitrageResults_file = open(arbitrageResults, "a")

profitableArbitrageResults = "TxtFiles/profitableArbitrageResults.txt"
profitableArbitrageResults_file = open(profitableArbitrageResults, "a")

profitable_odds = []
has_profitable_result = False
profitable_odds = []

results = arbitrage(list_to_arbitrage)
for result in results:
    arbitrageResults_file.write(str(result) + '\n')
print(results)
print("----")
print("Profitable: ")
for result in results:
    if result[9] == "YES":
        profitableArbitrageResults_file.write(str(result) + '\n')
        #if system_name == "Linux":
        has_profitable_result = True
        profitable_odds.append(result)
        
        print(result)

if has_profitable_result and system_name == "Linux":
    repo = git.Repo(repo_path)
    profitable_file_path = 'BettingSiteOdds/TxtFiles/profitableArbitrageResults.txt'
    repo.index.add([profitable_file_path])
    
    commit_message = "AUTOMATIC: Arbitrage Found\nOdds:{}".format(profitable_odds)
    print(commit_message)
    repo.index.commit(commit_message)
    
    origin = repo.remote('origin')
    origin.push()
    has_profitable_result = False

arbitrageResults_file.close()
profitableArbitrageResults_file.close()
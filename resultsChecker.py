import re

file_path = "tabResults.txt"
file = open(file_path,"r")
tabResults = file.read()
file.close()

wordsToRemove  = ["Summer","League3", "Tomorrow","Options","Boston","Brooklyn", "New York", "Philadelphia", "Toronto", "Chicago", "Detroit", "Indiana", "Milwaukee", "Atlanta", "Charlotte", "Miami", "Orlando", "Washington", "Denver", "Minnesota", "Oklahoma City", "Portland", "Utah", "Golden State", "LA", "Los Angeles", "Phoenix", "Sacramento", "Dallas", "Houston", "Memphis", "New Orleans", "San Antonio"]
listOfTeams = ["Celtics", "Nets", "Knicks", "76ers", "Raptors", "Bulls", "Cavaliers", "Pistons", "Pacers", "Bucks", "Hawks", "Hornets", "Heat", "Magic", "Wizards", "Nuggets", "Timberwolves", "Thunder", "Trail Blazers", "Jazz", "Warriors", "Clippers", "Lakers", "Suns", "Kings", "Mavericks", "Rockets", "Grizzlies", "Pelicans", "Spurs"]

def tidyOdds(strings):
    firstItemResults = [] # 0 = team1, 1 = team1 odds, 3 = team2, 4 = team2 odds

    for string in strings:
        for team in listOfTeams:
            string = string.replace(team, team + " ")
        string = string.replace("Trail Blazers", "Trailblazers")
        string = string.replace("HeadHandicapTotal", "Head Handicap Total")

        findDecimalNumbers = re.findall(r'\d+\.\d+', string)


        for line in string.split("\n"):
            words = line.split()
            if words:
                first_team = words[0]
                second_team = words[2]
                odds = findDecimalNumbers[:2]
                firstItemResults.append([first_team, second_team, *odds])
    
    return firstItemResults



for word in wordsToRemove:
    tabResults = tabResults.replace(word, "")
tabResults = tabResults.split("NBA")

tabResults = [string.lstrip() for string in tabResults]
tabResults.pop()
tabCount = len(tabResults)

print("-------------")
print(tidyOdds(tabResults))




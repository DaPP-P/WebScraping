file_path = "tabResults.txt"
file = open(file_path,"r")
tabResults = file.read()
file.close()

wordsToRemove  = ["Summer","League3", "Tomorrow","Options","Los Angeles","Miami","Philadelphia","Memphis","Charlotte","San Antonio","Oklahoma City","Utah","Sacramento","Golden State"]

for word in wordsToRemove:
    tabResults = tabResults.replace(word, "")

tabResults = tabResults.split("NBA")
print("-------------")
print(tabResults)
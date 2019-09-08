import csv
import json
import pandas as pd

awardsJson = open('awards.json', 'r')
medalsJson = open('medals.json', 'r')
sectionsJson = open('sections.json', 'r')

awards = pd.read_json(awardsJson)
medals = pd.read_json(medalsJson)
sections = pd.read_json(sectionsJson, encoding="utf-8")

awards = awards.drop(columns="section")
isGold = medals['medal_awarded'] == "Gold"
medals = medals[isGold]

# # Get sites to scrape
# for team in medals['team_name']:
#     new = team.replace(" ", "_")
#     scrape = medals.replace(team,new)
# scrape['wiki_link'] = "http://2018.igem.org/Team:"+scrape['team_name']
# scrape.to_csv('toScrape.csv')

#print(medals.to_string())
combined = pd.DataFrame.merge(medals,awards,how="left")
#print(combined.to_string())
sections = sections.rename(columns={'Team':'team_name'})
# Format names
for team in combined['team_name']:
    new = team.replace(" ","_")
    combined = combined.replace(team,new)

#print(combined[['team_name']])
combined = pd.DataFrame.merge(sections[['team_name','Section','Year']],combined,how="right")
combined['wiki_link'] = "http://2018.igem.org/Team:"+combined['team_name']
print(combined.to_string())
combined.to_csv('medal_awards_data.csv')
import csv
import json

csvfile = open('2018_Team_List.csv', 'r')
jsonfile = open('sections.json', 'w')

fieldnames = ("ID","Team","Region","Country", "Track", "Section", "Size", "Status", "Year")
reader = csv.DictReader(csvfile, fieldnames)
out = json.dumps([row for row in reader])
jsonfile.write(out)
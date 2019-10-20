import csv
from summarizer import Summarizer


with open(r"Data/initial_data.csv", encoding="utf-8-sig") as data, open(r"Data/bert_summary_full.csv", "w", newline='', encoding = 'utf-8-sig') as out:
    reader = csv.DictReader(data)
    writer = csv.writer(out, delimiter = ',')
    #tweak greediness, settings for model we can train, and layers
    model = Summarizer(greedyness = 0.48)
    writer.writerow(['team_name'] + ['page'] + ['header'] + ['original'] + ['summarized'])
    for row in reader:
        content = ' '.join(row['body'].split())
        team = row['team_name']
        #minlength, maxlength, ratio
        try:
            result = model(content, min_length = 60)
            full = "".join(result)
            print("Original:")
            print(content)
            print("="*38)
            print("Summarized:")
            print(full)
            print("-"*38)
            writer.writerow([team] + [row['page']] + [row['header']] + [content] + [full])
        except:
            print("*"*38)
            print("ERROR")
            print("*"*38)
            writer.writerow([team] + [row['page']] + [row['header']] + [content] + [content])
    
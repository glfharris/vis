from requests import get
from bs4 import BeautifulSoup

import re
import pickle
import csv
import dateutil.parser

def grab_feed_page(i):
    return get("https://gov.uk/drug-safety-update", params={"page": i})

def parse_feed_page(page):
    pages = []
    soup = BeautifulSoup(page, "html.parser")
    for x in soup.find_all("li", class_="document"):
        pages.append("https://gov.uk" + x.h3.a["href"])
    return pages

def collect_updates():
    pages = []
    for i in range(1, 10):
        res = grab_feed_page(i)
        pages += parse_feed_page(res.text)
    return pages

def build_drugs(path="./bnf_codes.csv"):
    drugs = {}
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["BNF Chemical Substance Code"] not in drugs.keys():
                drugs[row["BNF Chemical Substance Code"]] = [row["BNF Chemical Substance"], row["BNF Product"]]
            else:
                drugs[row["BNF Chemical Substance Code"]] += [row["BNF Chemical Substance"], row["BNF Product"]]
    for k in drugs.keys():
        drugs[k] = list(set(drugs[k]))
    return drugs

def identify_drug(text, drugs):
    alerts = []
    date = None
    soup = BeautifulSoup(text, "html.parser")
    if soup.find("time"):
        stamp = soup.find("time")["datetime"]
        date = dateutil.parser.parse(stamp)

    for k in drugs.keys():
        for name in drugs[k]:
            if name in soup.get_text():
                if date:
                    alerts.append((k, date.date()))
                    print(k + " - " + str(date.date()))
    return alerts

drugs = build_drugs()
alerts = []
for x in collect_updates():
    tmp = identify_drug(get(x).text, drugs)
    alerts += tmp

alerts = list(set(alerts))

collated_alerts = {}
for (drug, date) in alerts:
    if drug in collated_alerts.keys():
        collated_alerts[drug] += [date]
    else:
        collated_alerts[drug] = [date]

with open("alerts.pickle", "wb") as f:
    pickle.dump(collated_alerts, f, pickle.HIGHEST_PROTOCOL)

print(collated_alerts)
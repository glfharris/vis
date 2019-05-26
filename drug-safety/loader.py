import pickle
import datetime
import json

def load():
    with open("alerts.pickle", "rb") as f:
        data = pickle.load(f)
    return data

if __name__ == "__main__":
    data = load()
    for k in data.keys():
        tmp = data[k]
        new = []
        for x in tmp:
            new.append(str(x))
        data[k] = new
    with open("alerts.json", "w") as f:
        json.dump(data, f)
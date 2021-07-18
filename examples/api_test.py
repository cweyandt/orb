import json
from pprint import pprint

import requests


def printResponse(res):
    print("Response:\t" + str(res))
    print("Reason:\t\t" + str(res.reason))
    print("Headers:\t" + str(res.headers))
    print("Content:\t _____________________________" )
    # print(res.content)
    pprint(json.loads(res.content), width=120)

# url = 'http://localhost/api/v1/models/binseg_rbf'
headers = {'Content-type': 'application/json'}


# wifiData = pd.read_pickle('../data/cleaned/' + 'wifi_ap_data.pkl')
# wifiTotals = wifiData.sum(axis=1).replace(0, np.nan).fillna(method='ffill')
# wifiTotals.index = wifiTotals.index.tz_localize(None)
#
# vals = np.array(wifiTotals["2020-6-21 00:00":"2020-6-28 00:00"])
# ts = np.array(wifiTotals["2020-6-21 00:00":"2020-6-28 00:00"].index)
# data= {"ts": ts.tolist(), "val": vals.tolist()}

# response = requests.put(url, headers=headers, json=data, params=params)
#
# print(response.json())


url = 'http://localhost/api/v1/models/kernel/l2/json'
url = 'http://localhost/api/v1/analyze/json'
dataFile = "../01_ETL/skyspark_grid.json"
dataFile = "../examples/wifi_sample.json"

# Open the skyspark_grid.json file
with open(dataFile) as file:
    # Load its content and make a new dictionary
    data = json.load(file)

params = {"groupby": "date"}
# params = {"groupby": "day"}

response = requests.post(url, headers=headers, json=data, params=params)
printResponse(response)

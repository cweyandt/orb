from datetime import datetime

import requests
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

url = 'http://localhost/api/v1/models/binseg_rbf'
headers = {'Content-type': 'application/json'}
params = {"breakpoints": "10"}

wifiData = pd.read_pickle('../data/cleaned/' + 'wifi_ap_data.pkl')
wifiTotals = wifiData.sum(axis=1)
wifiTotals = wifiTotals.replace(0, np.nan)
wifiTotals = wifiTotals.fillna(method='ffill')
wifiTotals.index = wifiTotals.index.tz_localize(None)

vals = np.array(wifiTotals["2020-6-21 00:00":"2020-6-28 00:00"])
ts = np.array(wifiTotals["2020-6-21 00:00":"2020-6-28 00:00"].index)
data= {"ts": ts.tolist(), "val": vals.tolist()}

print(data)

# plt.figure(figsize=(20, 8))
# plt.title("Wifi Connections - This Week Last Year")
# plt.plot(wifiTotals["2020-6-22 00:00":"2020-6-23 00:00"])

response = requests.put(url, headers=headers, json=data, params=params)

print(response.json())
# print(response.url)
# print(response.request.headers)
from datetime import datetime

import requests
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

url = 'http://localhost/api/v1/models/binseg_rbf'
headers = {'Content-type': 'application/json'}
params = {"breakpoints": "10"}

wifiData = pd.read_pickle('../data/cleaned/' + 'wifi_ap_data.pkl')
wifiTotals = wifiData.sum(axis=1).replace(0, np.nan).fillna(method='ffill')
wifiTotals.index = wifiTotals.index.tz_localize(None)

vals = np.array(wifiTotals["2020-6-21 00:00":"2020-6-28 00:00"])
ts = np.array(wifiTotals["2020-6-21 00:00":"2020-6-28 00:00"].index)
data= {"ts": ts.tolist(), "val": vals.tolist()}

response = requests.put(url, headers=headers, json=data, params=params)

print(response.json())

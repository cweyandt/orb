from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
from fastapi import APIRouter

from ..parsers.haystackGridJson import GridJson, gridToDataframe, seriesToHaystackGrid
from ..orb_functions.orb_functions import normalize, timeFinder, analyze


router = APIRouter(
    prefix="/analyze",
    tags=["analyze"]
)


@router.post("/json")
def analyze_json(data: GridJson,
                 level: Optional[str] = "stream",
                 groupby: Optional[str] = "date",
                 dailyThreshold: Optional[float] = 0.9,
                 overallThreshold: Optional[float] = 0.9
                 ):
    data_df = gridToDataframe(data)

    try:
        results = analyze(data_df, level, groupby, dailyThreshold, overallThreshold)
    except Exception as error:
        return {"error_text": str(error)}

    changepoints = pd.Series()

    # if results != {}:
    for date, start in results["start"].items():
        changepoints[str(date) + "T" + str(start)] = "true"
    for date, end in results["end"].items():
        changepoints[str(date) + "T" + str(end)] = "false"

    changepoints = changepoints.sort_index()

    return seriesToHaystackGrid(data, changepoints)
    # return changepoints


#
# def normalize(sensorData):
#     for idx, date in sensorData.groupby(sensorData.index.date):
#         dateString = date.index[0].strftime('%Y-%m-%d')
#         sensorData[dateString] = sensorData[dateString] - date.min()
#     return sensorData
#
#
# def timeFinder(points, dailyThreshold=0.9):
#     sums, lens, ratios = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
#
#     for i in range(points.size):
#         try:
#             sums[points.index[i]] = points[i:].cumsum()
#         except ValueError:
#             print(str(ValueError) + " in timeFinder")
#             return {"start": None, "end": None}
#
#         lens[points.index[i]] = ([0] * i) + list(range(0, points.size - i))
#
#     lens.index = lens.columns
#     lens.replace(0, np.nan, inplace=True)
#
#     ratios = sums / sums.iloc[-1][0]
#     ratios[ratios < dailyThreshold] = np.nan
#     ratios = (lens / sums.shape[0]) / ratios
#
#     startTime = ratios.min().idxmin()
#     endTime = ratios.min(axis=1).idxmin()
#
#     return {"start": startTime, "end": endTime}
#
#
# def analyze(sensorData,
#             groupby="day",
#             dailyThreshold=0.9,
#             overallThreshold=0.9):
#     sensorData = normalize(sensorData)
#
#     startDatetimes = {}
#     endDatetimes = {}
#
#     for idx, date in sensorData.groupby(sensorData.index.date):
#         if groupby == "date":
#             dateString = date.index[0].strftime('%Y-%m-%d')
#         elif groupby == "day":
#             dateString = date.index[0].dayofweek
#         else:
#             raise ValueError('Illegal group argument: must be "day" or "date" to proceed.')
#
#         times = timeFinder(date, dailyThreshold)
#
#         if times["start"] != None:
#             if dateString not in startDatetimes:
#                 startDatetimes[dateString] = []
#                 endDatetimes[dateString] = []
#             startDatetimes[dateString].append(times["start"])
#             endDatetimes[dateString].append(times["end"])
#
#     if startDatetimes == {}:
#         return {"error": "No breakpoints found"}
#
#     if groupby == "date":
#         results = pd.concat([pd.DataFrame(startDatetimes), pd.DataFrame(endDatetimes)]).transpose()
#
#     elif groupby == "day":
#         startDatetimes = pd.DataFrame.from_dict(startDatetimes, orient='index')
#         endDatetimes = pd.DataFrame.from_dict(endDatetimes, orient='index')
#
#         startTimes = startDatetimes.applymap(lambda x: pd.NaT if pd.isnull(x) else x.time())
#         endTimes = endDatetimes.applymap(lambda x: pd.NaT if pd.isnull(x) else x.time())
#
#         startPercentiles = startTimes.applymap(
#             lambda x: pd.NaT if pd.isnull(x) else datetime.combine(datetime.min, x) - datetime.min).quantile(
#             1 - overallThreshold, axis=1, numeric_only=False).apply(lambda x: (datetime.min + x).time())
#         endPercentiles = endTimes.applymap(
#             lambda x: pd.NaT if pd.isnull(x) else datetime.combine(datetime.min, x) - datetime.min).quantile(
#             overallThreshold, axis=1, numeric_only=False).apply(lambda x: (datetime.min + x).time())
#
#         results = pd.concat([startPercentiles, endPercentiles], axis=1)
#     else:
#         results = None
#
#     results.columns = ["start", "end"]
#     return results

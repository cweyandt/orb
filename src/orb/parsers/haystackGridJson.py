'''
---From https://project-haystack.org/doc/docHaystack/Kinds#grid
Grid is a two dimensional tabular data type. Grids are essentially a list of dicts.
However grids may include grid level and column level meta data which is modeled as
a dict. Grids are the fundamental unit of data exchange over the HTTP API

This should do the trick
https://github.com/clarsen/pyhaystack/blob/master/pyhaystack/client/ops/his.py
https://pint.readthedocs.io/en/stable/
https://github.com/widesky/hszinc
'''
from datetime import datetime
from typing import Dict, Union, Optional, List

# TODO: Redo this entire set of functions using hszinc and pyhaystack
# import hszinc
# import pyhaystack
import numpy as np
import pandas as pd
from pydantic import BaseModel


class GridMeta(BaseModel):
    ver: str
    dis: str
    view: Optional[str]
    hisStart: Dict[str, str]
    hisEnd: Dict[str, str]
    hisLimit: Optional[int]

class GridCols(BaseModel):
    name: str
    meta: Optional[Dict[str, Union[str, int, Dict]]]

class GridTS(BaseModel):
    _kind: str
    tz: str
    val: datetime

class GridVal(BaseModel):
    _kind: str
    val: Union[int, float, str]
    unit: Optional[str] = None

class GridRows(BaseModel):
    ts: GridTS
    v0: Union[GridVal, float]

class GridJson(BaseModel):
    _kind: str
    meta: GridMeta
    cols: List[GridCols]
    rows: List[GridRows]

    # Example Haystack Grid object as JSON
    # TODO: Fix example GRID so that it works in Swagger/Redoc
    class Config:
        schema_extra = {
            "example": {
                "_kind": "grid",
                "meta": {"ver":"3.0", "dis":"Sample WiFi Data for one day",
                         "hisStart": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-06-22T00:00:00-07:00"},
                         "hisEnd": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-06-23T00:00:00-07:00"},
                         },
                "cols": [
                    {"name": "ts",
                     "meta": {"tz": "Los_Angeles"}},
                    {"name": "v0",
                     "meta": {
                         "navName": "WiFi Connections"}}
                        ],
                "rows": [
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T00:00:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T00:15:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T00:30:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T00:45:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T01:00:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T01:15:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T01:30:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T01:45:00-07:00"}, "v0": 2},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T02:00:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T02:15:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T02:30:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T02:45:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T03:00:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T03:15:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T03:30:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T03:45:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T04:00:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T04:15:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T04:30:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T04:45:00-07:00"}, "v0": 3},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T05:00:00-07:00"}, "v0": 3},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T05:15:00-07:00"}, "v0": 3},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T05:30:00-07:00"}, "v0": 3},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T05:45:00-07:00"}, "v0": 3},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T06:00:00-07:00"}, "v0": 4},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T06:15:00-07:00"}, "v0": 8},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T06:30:00-07:00"}, "v0": 4},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T06:45:00-07:00"}, "v0": 4},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T07:00:00-07:00"}, "v0": 4},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T07:15:00-07:00"}, "v0": 4},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T07:30:00-07:00"}, "v0": 6},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T07:45:00-07:00"}, "v0": 5},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T08:00:00-07:00"}, "v0": 6},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T08:15:00-07:00"}, "v0": 7},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T08:30:00-07:00"}, "v0": 12},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T08:45:00-07:00"}, "v0": 13},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T09:00:00-07:00"}, "v0": 22},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T09:15:00-07:00"}, "v0": 24},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T09:30:00-07:00"}, "v0": 26},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T09:45:00-07:00"}, "v0": 27},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T10:00:00-07:00"}, "v0": 32},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T10:15:00-07:00"}, "v0": 37},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T10:30:00-07:00"}, "v0": 36},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T10:45:00-07:00"}, "v0": 32},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T11:00:00-07:00"}, "v0": 32},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T11:15:00-07:00"}, "v0": 34},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T11:30:00-07:00"}, "v0": 35},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T11:45:00-07:00"}, "v0": 38},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T12:00:00-07:00"}, "v0": 38},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T12:15:00-07:00"}, "v0": 26},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T12:30:00-07:00"}, "v0": 27},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T12:45:00-07:00"}, "v0": 27},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T13:00:00-07:00"}, "v0": 31},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T13:15:00-07:00"}, "v0": 34},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T13:30:00-07:00"}, "v0": 35},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T13:45:00-07:00"}, "v0": 32},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T14:00:00-07:00"}, "v0": 37},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T14:15:00-07:00"}, "v0": 38},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T14:30:00-07:00"}, "v0": 46},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T14:45:00-07:00"}, "v0": 33},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T15:00:00-07:00"}, "v0": 38},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T15:15:00-07:00"}, "v0": 36},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T15:30:00-07:00"}, "v0": 33},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T15:45:00-07:00"}, "v0": 35},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T16:00:00-07:00"}, "v0": 34},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T16:15:00-07:00"}, "v0": 36},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T16:30:00-07:00"}, "v0": 34},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T16:45:00-07:00"}, "v0": 27},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T17:00:00-07:00"}, "v0": 26},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T17:15:00-07:00"}, "v0": 27},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T17:30:00-07:00"}, "v0": 25},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T17:45:00-07:00"}, "v0": 16},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T18:00:00-07:00"}, "v0": 18},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T18:15:00-07:00"}, "v0": 21},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T18:30:00-07:00"}, "v0": 15},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T18:45:00-07:00"}, "v0": 10},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T19:00:00-07:00"}, "v0": 11},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T19:15:00-07:00"}, "v0": 7},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T19:30:00-07:00"}, "v0": 5},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T19:45:00-07:00"}, "v0": 5},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T20:00:00-07:00"}, "v0": 5},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T20:15:00-07:00"}, "v0": 5},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T20:30:00-07:00"}, "v0": 5},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T20:45:00-07:00"}, "v0": 4},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T21:00:00-07:00"}, "v0": 4},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T21:15:00-07:00"}, "v0": 4},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T21:30:00-07:00"}, "v0": 3},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T21:45:00-07:00"}, "v0": 4},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T22:00:00-07:00"}, "v0": 2},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T22:15:00-07:00"}, "v0": 3},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T22:30:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T22:45:00-07:00"}, "v0": 1},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T23:00:00-07:00"}, "v0": 2},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T23:15:00-07:00"}, "v0": 2},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T23:30:00-07:00"}, "v0": 2},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-07-29T23:45:00-07:00"}, "v0": 2}
                        ]
            }
        }

# Pull (ts,val) from a univariate haystack grid
def parseHaystackGrid(data: GridJson):
    ts = []
    val = []
    for row in data.rows:
        ts.append(row.ts.val)
        try:
            val.append(row.v0.val)
        except AttributeError:  # Deal with unitless value columns
            val.append(row.v0)
    ts = np.array(ts)
    val = np.array(val)
    return ts, val

# Convert univariate haystack grid to dataframe
# TODO: rename func and vars to reflect that this converts to pandas Series, not Dataframe
def gridToDataframe(data: GridJson):
    ts = []
    val = []
    for row in data.rows:
        ts.append(row.ts.val)
        try:
            val.append(row.v0.val)
        except AttributeError:  # Deal with unitless value columns
            val.append(row.v0)
    df = pd.Series(val)
    df.index = pd.DatetimeIndex(pd.to_datetime(ts, utc=True)).tz_convert("US/Pacific").tz_localize(None)
    df = df.replace(0, np.nan).fillna(method='ffill')
    return df

# Convert results from Ruptures CPD methods to haystack grid with alternating True/False values
# TODO: This is just plain lazy. It was a first attempt and should be discarded.
def buildHaystackGrid(data: GridJson, bkps_i: List[int], ts):
    grid = {"_kind": "grid", "meta": {"ver": "3.0", "hisStart": data.meta.hisStart, "hisEnd": data.meta.hisEnd},
            "cols": [{"name": "ts"}, {"name": "v0", "kind": "Bool"}],
            "rows": [{"ts": data.meta.hisStart, "v0": "false"}]}  # Initialize first point from hisStart

    # Toggle true/false for each event TODO: make this smarter
    toggle = True
    for i in bkps_i[:-1]:
        grid["rows"].append({"ts": {"_kind": "dateTime", "tz": data.meta.hisStart["tz"], "val": ts[i]},
                             "v0": str(toggle).lower()})
        toggle = False if toggle else True

    grid["rows"].append({"ts": data.meta.hisEnd, "v0": str(toggle).lower()})  # Initialize last point from hisEnd
    return grid


# Convert pandas Series to haystack Grid
# TODO: Replace this with hszinc library implemented as a dependency
def seriesToHaystackGrid(data: GridJson, changepoints):
    hisStart = data.meta.hisStart
    hisEnd = data.meta.hisEnd
    tz = data.meta.hisStart["tz"]
    grid = {"_kind": "grid", "meta": {"ver": "3.0", "hisStart": hisStart, "hisEnd": hisEnd},
            "cols": [{"name": "ts"}, {"name": "v0", "kind": "Bool"}],
            "rows": []
            }

    for ts, val in changepoints.sort_index().items():
        grid["rows"].append({"ts": {"_kind": "dateTime", "tz": tz, "val": ts},
                             "v0": val})
    return grid

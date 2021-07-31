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
                "meta": {"hisStart": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-06-22T00:00:00-07:00"},
                         "hisEnd": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-06-23T00:00:00-07:00"},
                         },
                "cols": [
                    {"name": "ts",
                     "meta": {"tz": "Los_Angeles"}},
                    {"name": "v0",
                     "meta": {
                         "id": {"_kind": "ref", "dis": "B74 Floor 1 Rm 107C Supply VAV-011 Zone Temperature",
                                "val": "p:lbnl:r:2391ddb2-7b4413e5"}, "tz": "Los_Angeles", "unit": "\u00b0F",
                         "locationRef": {"_kind": "ref", "dis": "B74 Floor 1", "val": "p:lbnl:r:239070b4-f416c9da"},
                         "navName": "Zone Temperature",
                         "spaceRef": {"_kind": "ref", "dis": "B74 Floor 1 Rm 107C",
                                      "val": "p:lbnl:r:23909712-0e6c5a3e"},
                         "siteRef": {"_kind": "ref", "dis": "74", "val": "p:lbnl:r:22c912f0-91f6badd"},
                     }
                     }
                ],
                "rows": [
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-06-21T23:55:00-07:00"},
                     "v0": {"_kind": "number", "val": 67.01000213623047, "unit": "\u00b0F"}},
                    {"ts": {"_kind": "dateTime", "tz": "Los_Angeles", "val": "2021-06-22T00:00:00-07:00"},
                     "v0": {"_kind": "number", "val": 66.98999786376953, "unit": "\u00b0F"}}
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

import pandas as pd
import ruptures as rpt
import numpy as np
from fastapi import APIRouter, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
from enum import Enum
from datetime import datetime
from matplotlib import pyplot as plt
import mpld3

router = APIRouter(
    prefix="/models",
    tags=["models"]
)


class ModelName(str, Enum):
    pelt_rbf = "pelt_rbf"
    kmeans = "kmeans"
    firstevent = "firstevent"


class RawData(BaseModel):
    ts: List[datetime]
    val: List[float]


@router.put("/binseg_rbf")
def binseg_rbf(breakpoints: int, data: RawData):
    points = np.array(data.val)
    # Binary segmentation search method, RBF segment model
    algo = rpt.Binseg(model="rbf").fit(points)
    bkps_i = algo.predict(n_bkps=breakpoints)
    bkps_ts = []
    for i in bkps_i[:-1]:
        bkps_ts.append(data.ts[i])
    return {"bkps_i": bkps_i, "bkps_ts": bkps_ts}


@router.put("/binseg_rbf/plot")
def binseg_rbf(breakpoints: int, data: RawData):
    points = np.array(data.val)
    # Binary segmentation search method, RBF segment model
    algo = rpt.Binseg(model="rbf").fit(points)
    bkps_i = algo.predict(n_bkps=breakpoints)
    bkps_ts = []
    for i in bkps_i[:-1]:
        bkps_ts.append(data.ts[i])
    fig, ax_array = rpt.display(points, bkps_i)
    plt.title('Binary Segmentation Search Method, RBF Segment Model')
    html_str = mpld3.fig_to_html(fig)
    html_file = open("index.html", "w")
    html_file.write(html_str)
    html_file.close()
    return {html_str}


class GridMeta(BaseModel):
    ver: str
    dis: str
    view: str
    hisStart: Dict[str, str]
    hisEnd: Dict[str, str]
    hisLimit: int


class GridCols(BaseModel):
    name: str
    meta: Dict[str, Union[str, int, Dict]]


class GridTS(BaseModel):
    _kind: str
    tz: str
    val: datetime


class GridVal(BaseModel):
    _kind: str
    val: Union[int,float,str]
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
                         "spaceRef": {"_kind": "ref", "dis": "B74 Floor 1 Rm 107C", "val": "p:lbnl:r:23909712-0e6c5a3e"},
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


@router.put("/binseg_rbf/json")
def binseg_rbf(breakpoints: int, data: GridJson):
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
    # Binary segmentation search method, RBF segment model
    algo = rpt.Binseg(model="rbf").fit(val)
    bkps_i = algo.predict(n_bkps=breakpoints)
    bkps_ts = []
    for i in bkps_i[:-1]:
        bkps_ts.append(ts[i])
    return {"bkps_ts": bkps_ts}


@router.post("/binseg_rbf/json")
def binseg_rbf(breakpoints: int, data: GridJson):
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
    # Binary segmentation search method, RBF segment model
    algo = rpt.Binseg(model="rbf").fit(val)
    bkps_i = algo.predict(n_bkps=breakpoints)
    grid = {"_kind": "grid", "meta": {"ver":"3.0", "hisStart": data.meta.hisStart, "hisEnd": data.meta.hisEnd},
            "cols":[{"name":"ts"},{"name":"v0"}],
            "rows":[{"ts": data.meta.hisStart, "v0": "false"}]}
    toggle = True
    for i in bkps_i[:-1]:
        grid["rows"].append( {"ts": {"_kind":"dateTime", "tz":"Los_Angeles", "val":ts[i]}, "v0": str(toggle).lower()} )
        toggle = False if toggle else True
    grid["rows"].append({"ts": data.meta.hisEnd, "v0": str(toggle).lower()})
    return grid


# @router.put("/binseg_rbf/csv")
# async def binseg_rbf(breakpoints: int, file: bytes = UploadFile(...)):
#     rawdata = await file.read()
#     data = pd.read_csv(rawdata)
#     points = np.array(data.val)
#     # Binary segmentation search method, RBF segment model
#     algo = rpt.Binseg(model="rbf").fit(points)
#     bkps_i = algo.predict(n_bkps=breakpoints)
#     bkps_ts = []
#     for i in bkps_i[:-1]:
#         bkps_ts.append(data.ts[i])
#     return {"bkps_i": bkps_i, "bkps_ts": bkps_ts}


@router.get("/{model_name}")
def run_model(model_name: ModelName,
              ):
    return {
        "model_name": model_name,
        "message": "Model is not defined"
    }


# Example of returning an HTML response with form to upload a file.
@router.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

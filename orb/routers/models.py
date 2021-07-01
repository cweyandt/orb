from datetime import datetime
from enum import Enum
import pandas as pd
import ruptures as rpt
import numpy as np
from fastapi import FastAPI, Query, Request, APIRouter, Body, File, UploadFile
from fastapi.responses import HTMLResponse
from matplotlib import pyplot as plt
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
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
    Html_file = open("index.html", "w")
    Html_file.write(html_str)
    Html_file.close()
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
    meta: Dict[str,Union[str,int,Dict]]

class GridTS(BaseModel):
    _kind: str
    tz: str
    val: datetime

class GridVal(BaseModel):
    _kind: str
    val: float
    unit: Optional[str] = None

class GridRows(BaseModel):
    ts: GridTS
    v0: GridVal


class JsonData(BaseModel):
    _kind: str
    meta: GridMeta
    cols: List[GridCols]
    rows: List[GridRows]

@router.put("/binseg_rbf/json")
def binseg_rbf(breakpoints: int, data: JsonData):
    ts = []
    val = []
    for row in data.rows:
        ts.append(row.ts.val)
        val.append(row.v0.val)
    ts = np.array(ts)
    val = np.array(val)
    # # Binary segmentation search method, RBF segment model
    algo = rpt.Binseg(model="rbf").fit(val)
    bkps_i = algo.predict(n_bkps=breakpoints)
    bkps_ts = []
    for i in bkps_i[:-1]:
        bkps_ts.append(ts[i])
    return {"bkps_ts": bkps_ts}

@router.put("/binseg_rbf/csv")
async def binseg_rbf(breakpoints: int, file: bytes = UploadFile(...)):
    rawData = await file.read()
    data = pd.read_csv(rawData)

    points = np.array(data.val)
    # Binary segmentation search method, RBF segment model
    algo = rpt.Binseg(model="rbf").fit(points)
    bkps_i = algo.predict(n_bkps=breakpoints)
    bkps_ts = []
    for i in bkps_i[:-1]:
        bkps_ts.append(data.ts[i])
    return {"bkps_i": bkps_i, "bkps_ts": bkps_ts}


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


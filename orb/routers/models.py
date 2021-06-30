from datetime import datetime
from enum import Enum
from typing import Optional
import ruptures as rpt
import numpy as np
from fastapi import FastAPI, Query, Request, APIRouter, Body
from matplotlib import pyplot as plt
from pydantic import BaseModel
from typing import List
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


@router.get("/{model_name}")
def run_model(model_name: ModelName,
              ):
    return {
        "model_name": model_name,
        "message": "Model is not defined"
    }




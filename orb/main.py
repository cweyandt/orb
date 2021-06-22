from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel
import pandas as pd


class ModelName(str, Enum):
    changepoint = "changepoint"
    kmeans = "kmeans"
    firstevent = "firstevent"


class OrbModel(BaseModel):
    name: ModelName.changepoint
    description: Optional[str] = "Basic changepoint detection model"
    agg_first: Optional[bool] = True
    threshold: Optional[float] = None


class OrbDataFrame(BaseModel):
    df: pd.DataFrame


app = FastAPI(root_path="/api")


@app.get("/api")
def read_root():
    return {"Help": "try /api/docs for documentation"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/analyze/{model_name}")
def load_model(model_name: ModelName, q: Optional[str] = None):
    return {"model_name": model_name, "q": q}


@app.get("api/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.changepoint:
        return {"model_name": model_name, "message": "Implement Changepoint Detection"}

    if model_name.value == "kmeans":
        return {"model_name": model_name, "message": "Estimate occupied/vacant by k-means clustering"}

    return {"model_name": model_name, "message": "Returns first event of the day"}

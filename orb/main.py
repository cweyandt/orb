from fastapi import FastAPI, Query, Request
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
import numpy as np
import pandas as pd


class ModelName(str, Enum):
    changepoint = "changepoint"
    kmeans = "kmeans"
    firstevent = "firstevent"
#
#
# class OrbModel(BaseModel):
#     name: ModelName.changepoint
#     description: Optional[str] = "Basic change point detection model"
#     agg_first: Optional[bool] = True
#     threshold: Optional[float] = None
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "changepoint",
#                 "description": "Basic change point detection model",
#                 "agg_first": True,
#                 "threshold": 3.2,
#             }
#         }


class OrbDataFrame(BaseModel):
    df: List[int] = [1, 2, 3, 4, 5]

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])


app = FastAPI(
    title='Occupant Responsive Buildings API',
    description='Estimate periods of occupancy in buildings',
    docs_url='/docs',
    root_path="/v1")


@app.get("/api")
def read_root(request: Request):
    return {"Help": "try /api/docs for documentation", "root_path": request.scope.get("root_path")}


@app.get("/api/items/{item_id}")
def read_item(item_id: int,
              request: Request,
              q: Optional[str] = Query(
                  None,
                  title="Query string",
                  description="Query string for the items to search in the database that have a good match",
                  min_length=3,
                )
              ):
    return {"item_id": item_id, "q": q, "root_path": request.scope.get("root_path")}


@app.get("/api/analyze/{model_name}")
def load_model(model_name: ModelName,
               q: Optional[str] = Query(
                  None,
                  title="Query string",
                  description="Query string for the items to search in the database that have a good match",
                  min_length=3),
               m: Optional[OrbDataFrame] = None):
    return {"model_name": model_name, "q": q, "m": m}


@app.get("/api/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.changepoint:
        return {"model_name": model_name, "message": "Implement Changepoint Detection"}

    if model_name.value == "kmeans":
        return {"model_name": model_name, "message": "Estimate occupied/vacant by k-means clustering"}

    return {"model_name": model_name, "message": "Returns first event of the day"}


class SensorType(str, Enum):
    occ = "occ_sensor"
    co2 = "co2_sensor"
    cardkey = "cardkey_access_log"
    wifi = "wifi_ap_connections"
    freezer = "freezer_door"
    fumeHood = "fumehood_flow"
    sound = "sound_level_sensor"
    binary = "generic_binary"
    analog = "generic_analog"


class SensorModel(BaseModel):
    """Data model to parse the request body JSON."""
    id: str
    zone: str
    sensor_type: SensorType = SensorType.binary
    scaling: List[float] = [0, 1]
    data_tz: str = 'UTC'
    display_tz: str = 'US/Pacific'
    agg_func: str = 'sum'
    rollup_func: str = 'max'
    data: OrbDataFrame

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])


@app.post('/predict')
async def predict(sensor: SensorModel):
    """Predict house prices in California."""
    data = sensor.data.to_df()
    y_pred = np.mean(data)
    return {'predicted_price': y_pred}

from fastapi import FastAPI, Query, Request, APIRouter
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
import numpy as np
import pandas as pd
from routers import models

app = FastAPI(
    title='Occupant Responsive Buildings API',
    description='Estimate periods of occupancy in buildings',
    docs_url='/docs',
    root_path="/api/v1")

app.include_router(models.router)

#
# class SensorType(str, Enum):
#     occ = "occ_sensor"
#     co2 = "co2_sensor"
#     cardkey = "cardkey_access_log"
#     wifi = "wifi_ap_connections"
#     freezer = "freezer_door"
#     fumeHood = "fumehood_flow"
#     sound = "sound_level_sensor"
#     binary = "generic_binary"
#     analog = "generic_analog"


@app.get("/")
def read_root(request: Request):
    return {"Help": "try visiting /v1/docs for documentation", "root_path": request.scope.get("root_path")}


# @app.get("/api/items/{item_id}")
# def read_item(item_id: int,
#               request: Request,
#               q: Optional[str] = Query(
#                   str,
#                   title="Query string",
#                   description="Query string for the items to search in the database that have a good match",
#                   min_length=3
#                 )
#               ):
#     return {"item_id": item_id, "q": q, "root_path": request.scope.get("root_path")}

#
# class SensorModel(BaseModel):
#     """Data model to parse the request body JSON."""
#     id: str
#     zone: str
#     sensor_type: SensorType = SensorType.binary
#     scaling: List[float] = [0, 1]
#     data_tz: str = 'UTC'
#     display_tz: str = 'US/Pacific'
#     agg_func: str = 'sum'
#     rollup_func: str = 'max'
#     data: str = None
#
#     def to_df(self):
#         """Convert pydantic object to pandas dataframe with 1 row."""
#         return pd.DataFrame([dict(self)])

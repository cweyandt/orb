from enum import Enum
from typing import Optional
from fastapi import FastAPI, Query, Request, APIRouter, Body

router = APIRouter(
    prefix="/models",
    tags=["models"]
)


class ModelName(str, Enum):
    pelt_rbf = "pelt_rbf"
    kmeans = "kmeans"
    firstevent = "firstevent"


@router.get("/{model_name}")
def run_model(model_name: ModelName,
              ):
    return {"model_name": model_name}



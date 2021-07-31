import pandas as pd
from fastapi import APIRouter
from typing import Optional
from ..orb_functions.orb_functions import analyze
from ..parsers.haystackGridJson import GridJson, gridToDataframe, seriesToHaystackGrid

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

    for date, start in results["start"].items():
        if not pd.isnull(start):
            ts = pd.to_datetime(str(start))
            changepoints[ts] = "true"
    for date, end in results["end"].items():
        if not pd.isnull(end):
            ts = pd.to_datetime(str(end))
            changepoints[ts] = "false"

    changepoints.index = pd.DatetimeIndex(pd.to_datetime(changepoints.index)).tz_localize("US/Pacific")

    return seriesToHaystackGrid(data, changepoints)

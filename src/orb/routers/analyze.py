from typing import Optional

import pandas as pd
from fastapi import APIRouter, Query

from ..orb_functions.orb_functions import analyze
from ..parsers.haystackGridJson import GridJson, gridToDataframe, seriesToHaystackGrid

router = APIRouter(
    prefix="/analyze",
    tags=["analyze"]
)


@router.post("/json", summary="TimeFinder Change Point Method")
def analyze_json(data: GridJson,
                 level: Optional[str] = Query("stream",
                                              title="Analysis level",
                                              description="level (required): \"stream\" if passing in a Pandas Series "
                                                          "with timestamp index and one data column or \"stamp\" if "
                                                          "passing in a Pandas Dataframe with datestring index and "
                                                          "two data columns containing suggested start and end times "
                                                          "(\"start\" and \"end\")"),
                 groupby: Optional[str] = Query("date",
                                                title="Groupby parameter",
                                                description="groupby (\"day\"): \"date\" to return results aggregated "
                                                            "by date or \"day\" to return results aggregated by day "
                                                            "of week"),
                 dailyThreshold: Optional[float] = Query(0.9,
                                                         title="Minimum daily AUC",
                                                         description="dailyThreshold (0.9): minimum percentage of "
                                                                     "timeseries area under curve (AUC) to be covered "
                                                                     "by the suggested start and end times for each "
                                                                     "day"),
                 overallThreshold: Optional[float] = Query(0.9,
                                                           title="Minimum overall AUC",
                                                           description="overallThreshold (0.9): percentile of "
                                                                       "suggested start and end times for each day to "
                                                                       "return as suggestion for that day of week if "
                                                                       "groupby = \"day\""),
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

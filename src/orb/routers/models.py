from enum import Enum
from typing import Optional

import ruptures as rpt
from fastapi import APIRouter, Query, Body, Path
from fastapi.responses import HTMLResponse

from ..parsers.haystackGridJson import GridJson, parseHaystackGrid, buildHaystackGrid

router = APIRouter(
    prefix="/models",
    tags=["models"]
)


class SearchMethod(str, Enum):
    binseg = "binseg"
    window = "window"
    dynamic = "dynamic"
    bottomup = "bottom_up"
    kernel = "kernel"


class ModelName(str, Enum):
    rbf = "rbf"
    l2 = "l2"
    l1 = "l1"
    linear = "linear"


@router.post("/{search_method}/{model}/json")
def ruptures_change_point_methods(breakpoints: int = Query(2, title="Expected breakpoints",
                                                 description="Number of breakpoints to compute for input data."),
                        search_method: SearchMethod = Path(None, title="Ruptures detection search method",
                                                           description="see https://centre-borelli.github.io/ruptures"
                                                                       "-docs/code-reference/"),
                        model: ModelName = Path(None, title="Ruptures detection search method",
                                                description="available methods differ by search_method. See "
                                                            "https://centre-borelli.github.io/ruptures-docs/code"
                                                            "-reference/"),
                        data: GridJson = Body(None, title="Timeseries input",
                                              description="Datetime indexed numerical series, modeled as a Haystack "
                                                          "Grid"),
                        width: Optional[int] = Query(40, title="Window length",
                                                     description="**for search_method=window**: `width` determines the "
                                                                 "length of the segmentation window "
                                                                 "instance (in number of samples)"),
                        min_size: Optional[int] = Query(3, title="Min distance",
                                                        description="**for search_method=dynamic|bottomup|kernel**: "
                                                                    "`min_size` "
                                                                    "controls the minimum distance between change "
                                                                    "points; for instance, if `min_size=10`, "
                                                                    "all change points will be at least 10 samples "
                                                                    "apart."),
                        jump: Optional[int] = Query(5, title="change point grid",
                                                    description="**for search_method=dynamic|bottomup|kernel**: `jump` "
                                                                "controls the grid of possible change points; for "
                                                                "instance, if `jump=k`, only changes at k, 2*k, 3*k,"
                                                                "... are considered.")):
    (ts, val) = parseHaystackGrid(data)

    # Determine which search method to use from [Binseg, Window, Dynamic, BottomUp, Kernel]
    if search_method == SearchMethod.binseg:
        algo = rpt.Binseg(model=model).fit(val)
    elif search_method == SearchMethod.window:
        algo = rpt.Window(model=model, width=width).fit(val)
    elif search_method == SearchMethod.dynamic:
        algo = rpt.Dynp(model=model, min_size=min_size, jump=jump).fit(val)
    elif search_method == SearchMethod.bottomup:
        algo = rpt.BottomUp(model=model, min_size=min_size, jump=jump).fit(val)
    elif search_method == SearchMethod.kernel:
        if model in [ModelName.rbf, ModelName.linear]:
            algo = rpt.KernelCPD(kernel=model, min_size=min_size, jump=jump).fit(val)
        else:
            algo = rpt.KernelCPD(kernel="rbf", min_size=min_size, jump=jump).fit(val)
    else:
        algo = rpt.Binseg(model=model).fit(val)

    # Run Ruptures Changepoint Detection with predefined number of breakpoints
    bkps_i = algo.predict(n_bkps=breakpoints)

    # Convert results to a Haystack grid
    return buildHaystackGrid(data, bkps_i, ts)


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


# Example of returning an HTML response with form to upload a file.
@router.get("/")
async def html_upload():
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

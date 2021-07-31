from enum import Enum
from typing import Optional

import ruptures as rpt
from fastapi import APIRouter
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
def changepoint_methods(breakpoints: int,
                        search_method: SearchMethod,
                        model: ModelName,
                        data: GridJson,
                        width: Optional[int] = 40,
                        min_size: Optional[int] = 3,
                        jump: Optional[int] = 5):
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

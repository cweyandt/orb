from fastapi import FastAPI, Request
from orb.routers import models, analyze, predict

app = FastAPI(
    title='Occupant Responsive Buildings API',
    description='Estimate periods of occupancy in buildings',
    docs_url='/docs',
    root_path="/api/v1")

# Add endpoints to the FastAPI app
app.include_router(models.router) # Basic CPD Methods
app.include_router(analyze.router) # Custom analysis method
# app.include_router(predict.router) # Prophet prediction endpoint

@app.get("/")
def default(request: Request):
    return {"Help": "try visiting /api/v1/docs or /api/v1/redoc for documentation", "root_path": request.scope.get("root_path")}

from fastapi import FastAPI

app = FastAPI(root_path="/api")


@app.get("/api")
def read_root():
    return {"Hello": "World"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
from typing import Optional, List

from fastapi import FastAPI

app = FastAPI()

@app.post("/api/predict")
def read_item(items: List[str]):
    return {"status": "ok", "items": ["1", "2", "3"]}

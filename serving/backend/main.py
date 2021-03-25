import random
from typing import Optional, List
from glob import glob
from time import sleep

from fastapi import FastAPI
import imagesize

app = FastAPI()

available_footage = list(glob("/footage/*.jpg")) + list(glob("../footage/*.jpg"))
available_footage = [i for i in available_footage if "lazy" not in i]

FIXED_WIDTH = 400

def _compute_height(width, height):
    return int(height / width * FIXED_WIDTH)

def generate_items_from_item_ids(item_ids: List["str"]):
    image_uris = random.sample(available_footage, len(item_ids))
    result = []
    for i, item_id in enumerate(item_ids):
        try:
            width, height = imagesize.get(image_uris[i])
            result.append({
                "item_id": item_id,
                "url": image_uris[i], 
                "lazy_url": image_uris[i].replace(".jpg", ".lazy.jpg"), 
                "height": _compute_height(width, height), 
                "title": "Top western road trips", 
                "subtitle": "lat: -10.03, long: 123.04",
                "outlined": False,
            })
        except:
            pass
    return result

@app.get("/api")
def read_root():
    return {"status": "ok", "message": "it works"}

@app.get("/api/options")
def read_item():
    return {"status": "ok", "items": generate_items_from_item_ids(range(70))}

@app.post("/api/recommend")
def read_item(items: List[str]):
    sleep(1.3)
    return {"status": "ok", "items": generate_items_from_item_ids(range(70))}

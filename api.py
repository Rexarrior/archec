

from map_border_converter import *

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from uvicorn import run

import os
app = FastAPI()

@app.get("/process_text/")
async def process_text(text: str):
    coordinates = coords_from_text(text) 
    url = make_url(coordinates)
    return {"url": url}



app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    file_path = os.path.join("static", "index.html")
    return FileResponse(file_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)



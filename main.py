from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from rembg import remove
import uuid
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

OUTPUT_FOLDER = "static/outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    input_bytes = await file.read()

    output_bytes = remove(input_bytes)

    output_filename = f"{uuid.uuid4()}.png"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    with open(output_path, "wb") as f:
        f.write(output_bytes)

    return FileResponse(output_path, media_type="image/png", filename="no_background.png")

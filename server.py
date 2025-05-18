import json
import os
import random
import string
import threading
import time
import webbrowser

import uvicorn
from fastapi import BackgroundTasks, FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from models_analysis.main import analyze_video

app = FastAPI()

ORIGINS = ["*"]
HOST = "localhost"
PORT = 8000

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Reactでビルドしたファイルを配信するための設定
app.mount("/static", StaticFiles(directory="frontend.backup/build/static"), name="static")
app.mount("/uploads", StaticFiles(directory="frontend.backup/build/uploads"), name="uploads")

UPLOAD_DIR = "frontend.backup/build/uploads"

# 進捗状況
progress = {}


def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


@app.get("/")
def read_root():
    return FileResponse("frontend.backup/build/index.html")


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    while True:
        file_name = f"{randomname(32)}.mp4"
        if not os.path.exists(f"{UPLOAD_DIR}/{file_name}"):
            break
    try:
        with open(f"{UPLOAD_DIR}/{file_name}", "wb") as f:
            content = await file.read()
            f.write(content)
        return {"status": "ok", "file_name": file_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def predict_background(file_name: str):
    global progress
    for response in analyze_video(f"{UPLOAD_DIR}/{file_name}", "models"):
        # print(response)
        progress = response


@app.post("/predict/{file_name}")
def predict(file_name: str, background_tasks: BackgroundTasks):
    if not os.path.exists(f"{UPLOAD_DIR}/{file_name}"):
        return {"status": "error", "message": "file not found"}
    background_tasks.add_task(predict_background, file_name)
    return {"status": "ok"}


@app.get("/events")
async def sse_endpoint():
    async def event_generator():
        global progress
        if not progress:
            yield f"{json.dumps({'progress': 0})}\n\n"
        else:
            yield f"{json.dumps(progress)}\n\n"
            progress = {}

    return EventSourceResponse(event_generator())


def open_browser():
    time.sleep(1)
    webbrowser.open(f"http://{HOST}:{PORT}")


if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    uvicorn.run("server:app", host=HOST, port=PORT, reload=True)

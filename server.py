import os
import random
import string
import threading
import time
import webbrowser

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from models_analysis.main import analyze_video

app = FastAPI()

ORIGINS = ["*"]
HOST = "localhost"
PORT = 8000

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,  # リクエストを許可するオリジンのリスト
    allow_credentials=True,  # 認証情報の共有を許可
    allow_methods=["*"],    # すべてのHTTPメソッドを許可
    allow_headers=["*"],    # すべてのHTTPヘッダーを許可
)


# Reactでビルドしたファイルを配信するための設定
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")
app.mount("/uploads", StaticFiles(directory="frontend/build/uploads"), name="uploads")

# TODO: /frontend/build/uploadsに変更
UPLOAD_DIR = "frontend/build/uploads"


def randomname(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


@app.get("/")
def read_root():
    # /frontend/build/index.htmlを返す
    return FileResponse("frontend/build/index.html")


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    """
    クライアントから受け取った動画ファイルを保存する
    """
    # ファイル名は32桁のランダムな数字
    while True:
        file_name = f"{randomname(32)}.mp4"
        if not os.path.exists(f"{UPLOAD_DIR}/{file_name}"):
            break
    try:
        # ファイルを保存
        with open(f"{UPLOAD_DIR}/{file_name}", "wb") as f:
            content = await file.read()  # ファイル内容を読み込み
            f.write(content)
        return {"status": "ok", "file_name": file_name}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.get("/predict/{file_name}")
def predict(file_name: str):
    """
    ランダムフォレストによる推論を行うエンドポイント
    """
    if not os.path.exists(f"{UPLOAD_DIR}/{file_name}"):
        return {"status": "error", "message": "file not found"}

    # ダミーの推論結果
    # time_lines = [
    #     {"time": "00:00:00", "result": "start"},
    #     {"time": "00:00:10", "result": "death"},
    #     {"time": "00:00:20", "result": "kill"},
    #     {"time": "00:00:30", "result": "kill"},
    #     {"time": "00:04:50", "result": "kill"},
    #     {"time": "00:05:00", "result": "finish"},
    # ]
    try:
        time_lines = analyze_video(f"{UPLOAD_DIR}/{file_name}", "models")
        return {
            "status": "ok",
            "file_name": file_name,
            "time_lines": time_lines,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def open_browser():
    time.sleep(1)  # 少し待機してからブラウザを開く
    webbrowser.open(f"http://{HOST}:{PORT}")


if __name__ == "__main__":
    # ブラウザを開くスレッドを開始
    threading.Thread(target=open_browser).start()

    # サーバーを起動
    uvicorn.run("server:app", host=HOST, port=PORT, reload=True)

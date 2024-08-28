import os
import random
import string
import threading
import time
import webbrowser

import uvicorn
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
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
TIME_LINE = []


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


def predict_background(file_name: str):
    """
    ランダムフォレストによる推論をバックグラウンドで行う
    """
    global TIME_LINE
    time_lines = analyze_video(f"{UPLOAD_DIR}/{file_name}", "models")
    TIME_LINE = time_lines


@app.get("/predict/{file_name}")
def predict(file_name: str, background_tasks: BackgroundTasks):
    """
    ランダムフォレストによる推論を行うエンドポイント
    """
    if not os.path.exists(f"{UPLOAD_DIR}/{file_name}"):
        return {"status": "error", "message": "file not found"}
    background_tasks.add_task(predict_background, file_name)
    return {"status": "ok"}


@app.get("/result")
def get_result():
    """
    解析結果を取得する
    """
    return {"status": "ok", "time_line": TIME_LINE}


def open_browser():
    time.sleep(1)  # 少し待機してからブラウザを開く
    webbrowser.open(f"http://{HOST}:{PORT}")


if __name__ == "__main__":
    # ブラウザを開くスレッドを開始
    threading.Thread(target=open_browser).start()

    # サーバーを起動
    uvicorn.run("server:app", host=HOST, port=PORT, reload=True)

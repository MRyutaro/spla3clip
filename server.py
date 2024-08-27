import threading
import time
import webbrowser

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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


@app.get("/")
def read_root():
    # /frontend/build/index.htmlを返す
    return FileResponse("frontend/build/index.html")


def open_browser():
    time.sleep(1)  # 少し待機してからブラウザを開く
    webbrowser.open(f"http://{HOST}:{PORT}")


if __name__ == "__main__":
    # ブラウザを開くスレッドを開始
    threading.Thread(target=open_browser).start()

    # サーバーを起動
    uvicorn.run("server:app", host=HOST, port=PORT, reload=True)

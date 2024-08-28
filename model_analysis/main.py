"""
クライアントから送られてきた動画を解析し、キル・デスをした時刻を返す
"""
import os
import pickle
import sys

import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.preprocess_data import process_image


def calculate_time(msec: int) -> str:
    """
    ミリ秒を受け取り、hh:mm:ss形式に変換して返す
    """
    # intにして2桁にする
    h = int(msec / 1000 / 60 / 60)
    m = int(msec / 1000 / 60 % 60)
    s = int(msec / 1000 % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def analyze_video(video_path: str) -> list:
    """
    1. 動画のパスを受け取る
    2. kill_model.pickleを読み込む
    3. 動画をフレームごとに読み込み、モデルに入力する
    4. モデルの出力を保存する
    5. キル・デスがあった時刻をリスト形式
    """
    # kill_model.pickleを読み込む
    with open(r"..\\model_build\\data\\processed\\kill_model.pickle", "rb") as f:
        kill_model = pickle.load(f)

    # 動画を開く
    cap = cv2.VideoCapture(video_path)

    results = []

    is_killing = False

    # 動画をフレームごとに読み込む
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 画像の前処理
        processed_image = process_image(frame)
        flattenned_image = processed_image.flatten()

        # モデルに入力
        pred = kill_model.predict([flattenned_image])

        if pred[0] == 1:
            # is_killigがFalseの時はTrueにしてデータを保存、Trueの時は保存しない
            if not is_killing:
                print("killしました")
                results.append({
                    "time": calculate_time(cap.get(cv2.CAP_PROP_POS_MSEC)),
                    "results": "kill"
                })
                print(results)
                is_killing = True
        # キルしていないときis_killingをFalseにする
        else:
            is_killing = False

        # 確認のために画像を表示
        cv2.imshow("image", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    # 使用例
    video_path = r"..\model_analysis\data\hoko.mp4"
    analyze_video(video_path)

"""
クライアントから送られてきた動画を解析し、キル・デスをした時刻を返す
"""
import os
import pickle
import sys
from pprint import pprint

import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.preprocess_data import process_kill_image  # noqa: E402


def calculate_time(msec: int) -> str:
    """
    ミリ秒を受け取り、hh:mm:ss形式に変換して返す
    """
    # intにして2桁にする
    h = int(msec / 1000 / 60 / 60)
    m = int(msec / 1000 / 60 % 60)
    s = int(msec / 1000 % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def analyze_video(video_path: str, pickle_dir_path: str) -> list:
    """
    動画を解析し、キル・デスをした時刻を返す
    """
    # kill_model.pickleを読み込む
    if not os.path.exists(os.path.join(pickle_dir_path, "kill_model.pickle")):
        print(f"pickleファイル {pickle_dir_path} が存在しません。パスを確認してください。")
        return []
    try:
        with open(os.path.join(pickle_dir_path, "kill_model.pickle"), "rb") as f:
            kill_model = pickle.load(f)
    except Exception as e:
        print(f"pickleファイルの読み込みに失敗しました。エラー: {e}")
        return []

    # 動画を開く
    if not os.path.exists(video_path):
        print(f"動画ファイル {video_path} が存在しません。パスを確認してください。")
        return
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"動画ファイル {video_path} を開けませんでした。動画が正しい形式か確認してください。")
        return

    results = []

    is_killing = False

    # 動画をフレームごとに読み込む
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 画像の前処理
        processed_image = process_kill_image(frame)

        # モデルに入力
        pred = kill_model.predict([processed_image])

        if pred[0] == 1:
            # is_killigがFalseの時はTrueにしてデータを保存、Trueの時は保存しない
            if not is_killing:
                print("killしました")
                results.append({
                    "time": calculate_time(cap.get(cv2.CAP_PROP_POS_MSEC)),
                    "results": "kill"
                })
                pprint(results)
                is_killing = True
        # キルしていないときis_killingをFalseにする
        else:
            is_killing = False

        # 確認のために画像を表示
        cv2.imshow("image", processed_image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    return results


if __name__ == "__main__":
    # 使用例
    # カレントディレクトリが/の場合
    # pickle_dir_path = r"models"
    # video_path = r"uploads/hoko.mp4"
    # カレントディレクトリが/models_analysisの場合
    pickle_dir_path = r"..\models"
    video_path = r"..\uploads\hoko.mp4"
    analyze_video(video_path, pickle_dir_path)

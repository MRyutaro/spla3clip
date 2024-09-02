"""
クライアントから送られてきた動画を解析し、キル・デスをした時刻を返す
"""
import os
import pickle
import sys
from pprint import pprint

from collections import deque

import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.preprocess_data import process_image  # noqa: E402


def calculate_time(msec: int) -> str:
    """
    ミリ秒を受け取り、hh:mm:ss形式に変換して返す
    """
    # intにして2桁にする
    h = int(msec / 1000 / 60 / 60)
    m = int(msec / 1000 / 60 % 60)
    s = int(msec / 1000 % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def analyze_video(video_path: str, pickle_dir_path: str, debug=False) -> list:
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
    FPS = cap.get(cv2.CAP_PROP_FPS)
    if not cap.isOpened():
        print(f"動画ファイル {video_path} を開けませんでした。動画が正しい形式か確認してください。")
        return

    results = []

    is_killing = False

    # ラベルを繰り返し格納するためのキュー
    MAX_LEN = 20
    label_queue = deque(maxlen=MAX_LEN)

    # 動画をフレームごとに読み込む
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 画像の前処理
        processed_image = process_image(frame)

        # モデルに入力
        pred = kill_model.predict([processed_image])

        # ラベルをキューに格納
        label_queue.append(pred[0])

        # キューの中身が全て1の時にkillと判定
        if all([label == 1 for label in label_queue]):
            # is_killigがFalseの時はTrueにしてデータを保存、Trueの時は保存しない
            if not is_killing:
                results.append({
                    "time": calculate_time(cap.get(cv2.CAP_PROP_POS_MSEC) - 1000 / FPS * MAX_LEN),
                    "result": "kill"
                })
                if debug:
                    print(label_queue)
                    print("killしました")
                    pprint(results)
                is_killing = True

        # キューの中身が全て0の時にis_killingをFalseにする
        elif all([label == 0 for label in label_queue]):
            is_killing = False

        # 確認のために画像を表示
        if debug:
            cv2.imshow("image", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    if debug:
        cv2.destroyAllWindows()

    return results


if __name__ == "__main__":
    # 使用例
    # カレントディレクトリが/の場合
    # pickle_dir_path = r"models"
    # video_path = r"uploads/hoko.mp4"
    # カレントディレクトリが/models_analysisの場合
    pickle_dir_path = r"..\models"
    video_path = r"..\models_analysis\data\video\area.mp4"
    analyze_video(video_path, pickle_dir_path, debug=True)

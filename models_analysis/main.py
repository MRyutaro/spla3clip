"""
クライアントから送られてきた動画を解析し、キル・デスをした時刻を返す
"""
import os
import pickle
import sys

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


def analyze_video(video_path: str, pickle_file_path: str) -> list:
    """
    1. 動画のパスを受け取る
    2. kill_model.pickleを読み込む
    3. 動画をフレームごとに読み込み、モデルに入力する
    4. モデルの出力を保存する
    5. キル・デスがあった時刻をリスト形式
    """
    # kill_model.pickleを読み込む
    if not os.path.exists(pickle_file_path):
        print(f"モデルファイル {pickle_file_path} が存在しません。パスを確認してください。")
        return
    with open(pickle_file_path, "rb") as f:
        kill_model = pickle.load(f)

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
        processed_image = process_image(frame)

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
    # カレントディレクトリが/の場合
    # pickle_file_path = r"models/kill_model.pickle"
    # video_path = r"uploads/hoko.mp4"
    # カレントディレクトリが/models_analysisの場合
    pickle_file_path = r"..\models\kill_model.pickle"
    video_path = r"..\models_analysis\data\video\スプラ3_3280kill.mp4"
    analyze_video(video_path, pickle_file_path)

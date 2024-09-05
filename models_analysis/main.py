"""
クライアントから送られてきた動画を解析し、キル・デスをした時刻を返す
"""
import os
import pickle
import sys
from collections import deque
from pprint import pprint

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


def process_queue_event(queue, is_event_active, event_name, max_len, cap, FPS, results, debug=False):
    """
    キューの中身がすべて1、またはすべて0の場合の処理を行う関数
    :param queue: イベントごとのキュー（deque）
    :param is_event_active: イベントが現在有効かどうかのフラグ（True/False）
    :param event_name: 検知するイベント名（例: "kill", "death" など）
    :param max_len: キューの最大長（int）
    :param cap: 動画キャプチャオブジェクト（cv2.VideoCapture）
    :param FPS: 動画のフレームレート（float）
    :param results: 結果を格納するリスト
    :param debug: デバッグモードのフラグ（bool）
    :return: is_event_active（イベントが検知されたかどうかを返す）
    """
    # キューの中身がすべて1の場合の処理（イベント発生）
    if all([label == 1 for label in queue]):
        if not is_event_active:
            # イベントが発生した時刻を記録
            results.append({
                "time": calculate_time(cap.get(cv2.CAP_PROP_POS_MSEC) - 1000 / FPS * max_len),
                "result": event_name
            })
            if debug:
                print(f"{event_name}イベント発生しました")
                pprint(results)
            is_event_active = True

    # キューの中身がすべて0の場合の処理（イベント終了）
    elif all([label == 0 for label in queue]):
        is_event_active = False

    return is_event_active


def analyze_video(video_path: str, pickle_dir_path: str, debug=False) -> list:
    """
    動画を解析し、キル・デスをした時刻を返す
    """

    model_files = ["kill_model.pickle", "death_model.pickle",
                   "start_model.pickle", "finish_model.pickle"]
    models = {}

    # pickleファイルが存在するか確認
    for model_file in model_files:
        model_path = os.path.join(pickle_dir_path, model_file)
        if not os.path.exists(model_path):
            print(f"pickleファイル: {model_file} が存在しません。パスを確認してください。")
            return []
        try:
            with open(model_path, "rb") as f:
                # ファイル名から拡張子を取り除いて辞書に格納する
                # []で囲むことで、pickleファイルの名前をキーにしてモデルを取得できる
                models[model_file.split(".")[0]] = pickle.load(f)

        except Exception as e:
            print(f"pickleファイル: {model_file} の読み込みに失敗しました。エラー：{e}。")
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
    is_dying = False
    is_starting = False
    is_finishing = False

    # ラベルを繰り返し格納するためのキュー
    KILL_LEN = 20
    DEATH_LEN = 2
    START_LEN = 3
    FINISH_LEN = 5

    kill_queue = deque(maxlen=KILL_LEN)
    death_queue = deque(maxlen=DEATH_LEN)
    start_queue = deque(maxlen=START_LEN)
    finish_queue = deque(maxlen=FINISH_LEN)

    # 動画をフレームごとに読み込む
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 画像の前処理
        processed_image = process_image(frame)

        # モデルに入力して予測結果を取得
        kill_pred = models['kill_model'].predict([processed_image])
        death_pred = models['death_model'].predict([processed_image])
        start_pred = models['start_model'].predict([processed_image])
        finish_pred = models['finish_model'].predict([processed_image])

        # 各キューに予測結果を格納
        kill_queue.append(kill_pred[0])
        death_queue.append(death_pred[0])
        start_queue.append(start_pred[0])
        finish_queue.append(finish_pred[0])

        # キューの中身がすべて1、またはすべて0の場合の処理
        is_killing = process_queue_event(
            kill_queue, is_killing, "kill", KILL_LEN, cap, FPS, results, debug)
        is_dying = process_queue_event(
            death_queue, is_dying, "death", DEATH_LEN, cap, FPS, results, debug)
        is_starting = process_queue_event(
            start_queue, is_starting, "start", START_LEN, cap, FPS, results, debug)
        is_finishing = process_queue_event(
            finish_queue, is_finishing, "finish", FINISH_LEN, cap, FPS, results, debug)

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

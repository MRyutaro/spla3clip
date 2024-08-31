"""
データの前処理を行うスクリプト

server.pyでimportして、model_analysis/main.pyやmodel_build/main.pyに関数渡しをして使う
"""

# import os
import cv2
# from sklearn.model_selection import train_test_split
import numpy as np

WIDTH = 320
HEIGHT = 180


def load_image(image_path: str) -> np.ndarray:
    """
    画像を読み込む
    """
    image = cv2.imread(image_path)
    return image


def process_kill_image(image: np.ndarray) -> np.ndarray:
    # サイズの確認
    aspect_ratio = image.shape[1] / image.shape[0]
    if abs(aspect_ratio - 16 / 9) > 0.01:
        print(f"アスペクト比が16:9ではない為、スキップしました。: {image_path}")
        return None

    # グレースケール変換
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # グレースケール変換

    # リサイズ
    image = cv2.resize(image, (WIDTH, HEIGHT))

    # # 加工した画像を開いて確認
    # print(image)
    # print(type(image))
    # print(image.shape)
    # cv2.imshow("image", image)
    # cv2.waitKey(0)

    # フラット化
    image = image.flatten()

    return image


if __name__ == "__main__":
    # 画像のパス
    image_path = r'..\models_build\data\raw\image\kill\sample_kill_image0.png'
    image = load_image(image_path)
    process_kill_image(image)

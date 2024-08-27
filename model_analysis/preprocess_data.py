"""
データの前処理を行うスクリプト

server.pyでimportして、model_analysis/main.pyやmodel_build/main.pyに関数渡しをして使う
"""

# import os
import cv2
# from sklearn.model_selection import train_test_split
import numpy as np


def process_image(image: np.ndarray) -> np.ndarray:
    # サイズの確認
    aspect_ratio = image.shape[1] / image.shape[0]
    if abs(aspect_ratio - 16 / 9) > 0.01:
        print(f"アスペクト比が16:9ではない画像: {image_path}")
        return None

    # グレースケール変換
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # グレースケール変換

    # リサイズ
    WIDTH = 320
    HEIGHT = 180
    image = cv2.resize(image, (WIDTH, HEIGHT))

    # # 加工した画像を開いて確認
    # print(image)
    # print(type(image))
    # print(image.shape)
    # cv2.imshow("image", image)
    # cv2.waitKey(0)

    return image


if __name__ == "__main__":
    # 画像のパス
    image_path = r'..\model_build\data\raw\image\kill\sample_kill_image.png'
    process_image(image_path)

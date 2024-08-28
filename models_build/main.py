"""
決定木モデルの構築

構築した決定木モデルはdata/processed/clf_model.pickleに保存する
"""
import os
import pickle
import sys

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# scriptsの中にあるprocess_data.pyの中のprocess_image関数をインポート
from scripts.preprocess_data import load_image, process_image  # noqa: E402

# 訓練用データのディレクトリ
TRAIN_DATA_DIR = "../models_build/data/raw/image"
# モデルの保存先ディレクトリ
MODELS_DIR = "../models"


def build_kill_model():
    """
    killを学習するモデルを構築する関数
    """

    # 正解データのパス
    kill_image_dir = os.path.join(TRAIN_DATA_DIR, "kill")
    # 不正解データのパス
    other_image_dir = os.path.join(TRAIN_DATA_DIR, "other")

    processed_images = []

    # killディレクトリから画像を繰り返し取得
    for image_name in os.listdir(kill_image_dir):
        image_path = os.path.join(kill_image_dir, image_name)  # 画像のパスを作成

        # 画像の前処理
        try:
            image = load_image(image_path)
            processed_image = process_image(image)
            # ラベル「１」を付与してappend
            processed_images.append([processed_image, 1])
        except Exception as e:
            print(f"{image_name}の前処理に失敗しました")
            print(e)
            continue

    # otherディレクトリから画像を繰り返し取得
    for image_name in os.listdir(other_image_dir):
        image_path = os.path.join(other_image_dir, image_name)  # 画像のパスを作成

        # 画像の前処理
        try:
            image = load_image(image_path)
            processed_image = process_image(image)
            # ラベル「０」を付与してappend
            processed_images.append([processed_image, 0])

            print(f"{image_name}を処理しました")
        except Exception as e:
            print(f"{image_name}の前処理に失敗しました")
            print(e)
            continue

    # processed_imagesをテストデータと訓練データに分割
    X = [image[0] for image in processed_images]
    Y = [image[1] for image in processed_images]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # print("訓練データ数：", len(X_train))
    # print("テストデータ数：", len(X_test))

    # 決定木モデルの構築
    clf = DecisionTreeClassifier()
    clf.fit(X_train, Y_train)

    # モデルの評価
    accuracy = clf.score(X_test, Y_test)
    print("モデルの精度：", accuracy)

    # モデルの保存
    picke_name = "kill_model.pickle"
    with open(os.path.join(MODELS_DIR, picke_name), "wb") as f:
        pickle.dump(clf, f)


def build_death_model():
    """
    デスを学習するモデルを構築する関数
    """


def build_start_model():
    """
    スタートを学習するモデルを構築する関数
    """


def build_finish_model():
    """
    フィニッシュを学習するモデルを構築する関数
    """


if __name__ == "__main__":
    build_kill_model()
    build_death_model()
    build_start_model()
    build_finish_model()

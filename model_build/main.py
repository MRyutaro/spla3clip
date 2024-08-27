"""
決定木モデルの構築

構築した決定木モデルはdata/processed/clf_model.pickleに保存する
"""

# scriptsの中にあるprocess_data.pyの中のprocess_image関数をインポート
from preprocess_data import process_image
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import os
import pickle


def build_kill_model():
    """
    killを学習するモデルを構築する関数
    """

    # 正解データのパス
    kill_image_dir = '../model_build/data/raw/image/kill'
    # 不正解データのパス
    other_image_dir = '../model_build/data/raw/image/other'

    processed_images = []

    # killディレクトリから画像を繰り返し取得
    for image_name in os.listdir(kill_image_dir):
        image_path = os.path.join(kill_image_dir, image_name)  # 画像のパスを作成

        # 画像の前処理
        try:
            processed_image = process_image(image_path)
            # processed_imageをフラット化して１次元ベクトルに変換
            flattenned_image = processed_image.flatten()
            # ラベル「１」を付与してappend
            processed_images.append([flattenned_image, 1])
        except Exception as e:
            print(f"{image_name}の前処理に失敗しました")
            print(e)
            continue

    # otherディレクトリから画像を繰り返し取得
    for image_name in os.listdir(other_image_dir):
        image_path = os.path.join(other_image_dir, image_name)  # 画像のパスを作成

        # 画像の前処理
        try:
            processed_image = process_image(image_path)
            # processed_imageをフラット化して１次元ベクトルに変換
            flattenned_image = processed_image.flatten()
            # ラベル「０」を付与してappend
            processed_images.append([flattenned_image, 0])

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
    with open('../model_build/data/processed/kill_model.pickle', 'wb') as f:
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

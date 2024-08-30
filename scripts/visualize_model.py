import pickle
import sys

import cv2
import matplotlib.pyplot as plt


def visualize_model(model_path: str, sample_image_path: str):
    WIDTH = 320
    HEIGHT = 180

    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        print(f'モデルの読み込みに失敗しました: {e}')
        sys.exit()

    try:
        image = cv2.imread(sample_image_path)
        # OpenCVはBGR形式なので、RGBに変換
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (WIDTH, HEIGHT))
    except Exception as e:
        print(f'サンプル画像の読み込みに失敗しました: {e}')
        sys.exit()

    # モデルのfeature_importancesを取得
    try:
        feature_importances = model.feature_importances_
    except AttributeError:
        print('モデルにfeature_importances_が含まれていません。')
        sys.exit()

    # ヒートマップのサイズを画像に合わせてリサイズ
    feature_importances = feature_importances.reshape(HEIGHT, WIDTH)

    # 画像の表示
    plt.imshow(image, aspect='auto')
    # feature_importancesを重ねて表示
    plt.imshow(
        feature_importances, cmap='hot', alpha=0.8, interpolation='nearest')

    # カラーバーの追加.。高さを画像の高さに合わせる
    plt.colorbar(shrink=0.6)

    # 表示
    plt.axis('off')  # 軸を非表示にする
    plt.show()


if __name__ == '__main__':
    # 引数を受け取る
    args = sys.argv
    # 引数が1つであることを確認
    if len(args) != 3:
        print('python visualize_model.py <model_path> <sample_image_path>')
        sys.exit()

    # 引数を受け取る
    model_path = args[1]
    sample_image_path = args[2]
    # モデルの可視化
    visualize_model(model_path, sample_image_path)

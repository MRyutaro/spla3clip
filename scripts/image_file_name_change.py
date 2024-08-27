"""
C:/Users/recod/programs/splatoon3_highlight_collector/model_build/data/raw/image/killの中の.pngファイルの名前を変更するスクリプト
"""

import os

# 画像データのパス
image_dir = r"C:\Users\recod\programs\splatoon3_highlight_collector\model_build\data\raw\image\other"

# killディレクトリから画像を繰り返し取得して、sample_kill_image+繰り返し取得した数.pngにリネーム
for i, image_name in enumerate(os.listdir(image_dir)):
    image_path = os.path.join(image_dir, image_name)  # 画像のパスを作成
    os.rename(image_path, os.path.join(image_dir, f"sample_other_image{i}.png"))
    print(f"{image_name}をsample_other_image{i}.pngにリネームしました")

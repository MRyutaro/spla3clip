import os

import cv2


def extract_frames_from_video(video_path, output_dir):
    # 動画ファイルの名前を取得して拡張子を除去
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # 保存ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 動画を読み込む
    cap = cv2.VideoCapture(video_path)

    # 動画が正しく読み込めているか確認
    if not cap.isOpened():
        print(f"動画ファイル {video_path} を開けませんでした。パスを確認してください。")
        return

    frame_count = 1
    saved_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break  # フレームが取得できなかった場合、ループを抜ける

        # 10フレームごとに保存
        if frame_count % 1 == 0:
            frame_filename = f"{video_name}({saved_count + 1}).png"
            frame_path = os.path.join(output_dir, frame_filename)
            cv2.imwrite(frame_path, frame)
            # 画像の表示
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
            saved_count += 1

        frame_count += 1

    # リソースを解放
    cap.release()
    print(f"保存が完了しました。保存されたフレーム数: {saved_count}")


# 使用例
video_path = r'C:\Users\recod\programs\splatoon3_highlight_collector\models_build\data\raw\video\【(⁎⁍̴̛ᴗ⁍̴̛⁎)】(⁎⁍̴̛ᴗ⁍̴̛⁎)(⁎⁍̴̛ᴗ⁍̴̛⁎)(⁎⁍̴̛ᴗ⁍̴̛⁎)(⁎⁍̴̛ᴗ⁍̴̛⁎)(⁎⁍̴̛ᴗ⁍̴̛⁎)(⁎⁍̴̛ᴗ⁍̴̛⁎)(⁎⁍̴̛ᴗ⁍̴̛⁎)１位　XP4855~.mp4'
output_dir = r'C:\Users\recod\programs\splatoon3_highlight_collector\models_build\data\raw\image'

extract_frames_from_video(video_path, output_dir)

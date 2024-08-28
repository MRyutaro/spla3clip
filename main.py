import os
import sys

from models_analysis.main import analyze_video

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    models_dir = os.path.join(current_dir, "models")

    # python main.py uploads/hoko.mp4 out.csvで実行
    try:
        video_path = sys.argv[1]
        time_lines = analyze_video(video_path, models_dir)
        # 出力結果をCSVに保存
        try:
            csv_output_path = sys.argv[2]
        # それ以外ならout.csvに保存
        except IndexError:
            csv_output_path = "out.csv"

        with open(csv_output_path, "w", encoding="utf-8") as f:
            f.write("time,result\n")
            for time_line in time_lines:
                f.write(f"{time_line['time']},{time_line['result']}\n")

    except IndexError:
        print("python main.py {video_path}で実行してください")
        sys.exit(1)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        sys.exit(1)

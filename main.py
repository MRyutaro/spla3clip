import os
import sys

from models_analysis.main import analyze_video

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    models_dir = os.path.join(current_dir, "models")

    # python main.py uploads/hoko.mp4みたいな感じで実行
    try:
        video_path = sys.argv[1]
        time_lines = analyze_video(video_path, models_dir)
    except IndexError:
        print("python main.py {video_path}で実行してください")
        sys.exit(1)

    print(time_lines)

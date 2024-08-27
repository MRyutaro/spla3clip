# splatoon3_highlight_collector

TODO: ここにgifを入れる

スプラトゥーン3でキル・デスした時刻を自動で集めるツール

## 想定している利用者
- スプラ3のキル集を作りたい人
- スプラ3動画投稿者でデスしているときだけ早送りorカットしたい人

## 対応しているハイライト
- キル
- デス

## インストール方法・使い方
### exeファイルを使う場合

### pythonスクリプトを使う場合
1. このリポジトリをクローンする
```bash
git clone 
```

2. 必要なライブラリをインストールする
```bash
pip install -r requirements.txt
```

3. スプラ3のゲーム画面を録画する

4. 以下のコマンドを実行する
```bash
python main.py -i <input_video_path> -o <output_csv_path>
```

# splatoon3_highlight_collector

TODO: ここにgifを入れる

スプラトゥーン3でキル・デスした時刻を自動で集めるツールです。

以下の2つの方法で利用できます。
| 方法 | 説明 | おすすめ度 |
| --- | --- | --- |
| ブラウザ版 | ブラウザ上でボタン操作でキル・デスした時刻を自動で集める方法です。キル・デスした時刻を動画で確認することができます。プログラミングの知識が必要です。 | ★★ |
| コマンド版 | Pythonコマンドを使ってキル・デスした時刻を自動で集める方法です。 | ★☆ |

## 想定している利用者
- スプラ3のキル集を作りたい人
- スプラ3動画投稿者でデスしているときだけ早送りorカットしたい人

## 対応しているイベント
- キル
- デス
- スタート
- フィニッシュ

## インストール方法
### ◎ブラウザ版
1. Python, Node.jsをインストールする。

2. レポジトリをクローンする。
```bash
git clone https://github.com/MRyutaro/splatoon3_highlight_collector
```

3. 仮想環境を作成する。
```bash
python -m venv .venv
```

4. 仮想環境を有効化する。
```bash
source .venv/bin/activate
```

5. 依存パッケージをインストールする。
```bash
pip install -r requirements.txt
```

6. フロントエンドの依存パッケージをインストールし、ビルドする。
```bash
cd frontend
npm install
npm run build
```

### ◎コマンド版
1. Pythonをインストールする。

2. レポジトリをクローンする。
```bash
git clone https://github.com/MRyutaro/splatoon3_highlight_collector
```

3. 仮想環境を作成する。
```bash
python -m venv .venv
```

4. 仮想環境を有効化する。
```bash
source .venv/bin/activate
```

5. 依存パッケージをインストールする。
```bash
pip install -r requirements.txt
```

## 使い方
### ◎ブラウザ版
1. コマンドを実行する。
```bash
python server.py
```

2. ブラウザで`http://localhost:8000`にアクセスする。

3. 動画ファイルを選択し、アップロードする。

4. 解析開始ボタンを押す。

5. キル・デスした時刻をクリックして動画上で確認する。

### ◎コマンド版
1. コマンドを実行する。
```bash
python main.py <movie_file_path> <output_file_path>
```
コマンドの詳細は以下の通りです。
| 引数 | 説明 | 必須/任意 | デフォルト値 |
| --- | --- | --- | --- |
| movie_file_path | 動画ファイルのパスを指定してください。mp4形式のみ対応しています。 | 必須 | なし |
| output_file_path | 出力ファイルのパスを指定したい場合はcsv形式で指定してください。指定しない場合は`out.csv`に出力されます。 | 任意 | out.csv |

例）
```bash
python main.py movie.mp4
```

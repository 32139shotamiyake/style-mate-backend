#.envファイルからキーと値のペアを読み込むライブラリ
from dotenv import load_dotenv
# .envファイルを読み込み、環境変数としてロードする
load_dotenv()
# Flask本体
from flask import Flask
# CORS対策（フロントと別ポート通信するため）
from flask_cors import CORS
# db（SQLAlchemy）を外部ファイルから読み込む
from extensions import db, migrate
# ルーティング登録関数
from routes import register_routes
# 設定クラス
from config import Config
import os

def create_app():
    """
    Flaskアプリを生成して初期設定を行う関数
    """
    # Flaskアプリ生成
    app = Flask(__name__)

    # 設定ファイルを読み込む
    app.config.from_object(Config)

    # CORSを有効化
    CORS(app)

    # SQLAlchemyをFlaskアプリに紐付け
    db.init_app(app)
    
    #Migrate初期化
    migrate.init_app(app, db)

    # Blueprint（ルーティング）を一括登録
    register_routes(app)

    return app


# アプリ生成
app = create_app()


# python app.py で直接実行された場合のみ起動
if __name__ == "__main__":
    # 画像保存用ディレクトリを作成（なければ）
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 開発用サーバ起動
    app.run(debug=True, port=5000)

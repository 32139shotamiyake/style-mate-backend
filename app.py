# Flask本体
from flask import Flask
# CORS対策（フロントと別ポート通信するため）
from flask_cors import CORS
# db（SQLAlchemy）を外部ファイルから読み込む
from extensions import db
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

    # Blueprint（ルーティング）を一括登録
    register_routes(app)

    # アプリ起動時にテーブルを自動生成
    with app.app_context():
        db.create_all()

    return app


# アプリ生成
app = create_app()


# python app.py で直接実行された場合のみ起動
if __name__ == "__main__":
    # 画像保存用ディレクトリを作成（なければ）
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # 開発用サーバ起動
    app.run(debug=True, port=5000)

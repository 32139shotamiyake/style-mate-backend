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
from config import DevelopmentConfig,ProductionConfig
import os

def create_app():
    """
    Flaskアプリを生成して初期設定を行う関数
    """
    # Flaskアプリ生成
    app = Flask(__name__)

    # 設定ファイルを読み込む
    env=os.getenv("FLASK_ENV","development")

    if env=="production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # 画像保存用ディレクトリを作成（なければ）
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # CORSを有効化
    CORS(app)

    # SQLAlchemyをFlaskアプリに紐付け
    db.init_app(app)

    #DB初期化時のみコメントを外す！！
    #with app.app_context():
    #    db.create_all()
    
    #Migrate初期化
    migrate.init_app(app, db)

    # Blueprint（ルーティング）を一括登録
    register_routes(app)

    return app


# アプリ生成
app = create_app()
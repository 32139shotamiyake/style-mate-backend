import os

class BaseConfig:
    """
    Flaskアプリ共通の設定をまとめたクラス
    """
    # JSONの日本語文字化け防止
    JSON_AS_ASCII = False
    
    # 追跡機能をオフ（おまじない）
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 画像アップロード先ディレクトリ
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__), "static", "images"
    )

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # MySQL接続設定
    SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{os.getenv('DEV_DB_USER')}:"
    f"{os.getenv('DEV_DB_PASSWORD')}@"
    f"{os.getenv('DEV_DB_HOST')}/"
    f"{os.getenv('DEV_DB_NAME')}?charset=utf8"
)
    
class ProductionConfig(BaseConfig):
    DEBUG=False
    # MySQL接続設定
    SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{os.getenv('PRO_DB_USER')}:"
    f"{os.getenv('PRO_DB_PASSWORD')}@"
    f"{os.getenv('PRO_DB_HOST')}/"
    f"{os.getenv('PRO_DB_NAME')}?charset=utf8"
)
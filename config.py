import os

class Config:
    """
    Flaskアプリ全体の設定をまとめたクラス
    """
    # JSONの日本語文字化け防止
    JSON_AS_ASCII = False

    # MySQL接続設定
    SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}?charset=utf8"
)
    
    # 追跡機能をオフ（おまじない）
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 画像アップロード先ディレクトリ
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__), "static", "images"
    )

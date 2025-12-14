import os

class Config:
    """
    Flaskアプリ全体の設定をまとめたクラス
    """
    # JSONの日本語文字化け防止
    JSON_AS_ASCII = False

    # MySQL接続設定
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': "mysql",
      'password': "NewPassword",
      'host': "localhost",
      'db_name': "clothes"
  })
    
    # 追跡機能をオフ（おまじない）
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 画像アップロード先ディレクトリ
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__), "static", "images"
    )

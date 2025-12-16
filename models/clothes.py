from datetime import datetime, timezone
from extensions import db

class Clothes(db.Model):
    """
    clothes テーブルに対応するモデル
    """
    __tablename__ = "clothes"
    #主キー
    id = db.Column(db.Integer, primary_key=True)
    #画像の相対パス
    image_path = db.Column(db.String(255), nullable=False)
    #ジャンル
    genre = db.Column(db.String(50), nullable=False)
    #色
    color = db.Column(db.String(7), nullable=False)
    #作られた日
    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    #アップデートされた日
    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
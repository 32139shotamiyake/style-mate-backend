from extensions import db

class Memo(db.Model):
    """
    memos テーブルに対応するモデル
    """
    __tablename__ = "memos"
    #主キー
    id = db.Column(db.Integer, primary_key=True)
    #メモ本文
    memo = db.Column(db.String(255))

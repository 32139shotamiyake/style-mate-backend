from flask import Blueprint, request, jsonify
from models import Memo
from extensions import db

# Memo関連API用 Blueprint
memo_bp = Blueprint("memo", __name__)

@memo_bp.route("/insert", methods=["POST"])
def insert():
    """
    メモを1件追加するAPI
    """
    memo = Memo(memo=request.form["memo"])
    db.session.add(memo)
    db.session.commit()
    return jsonify({"message": "Inserted successfully"})

@memo_bp.route("/select", methods=["GET"])
def select():
    """
    メモ一覧を取得するAPI
    """
    memos = Memo.query.all()
    return jsonify([
        {"id": m.id, "memo": m.memo} for m in memos
    ])

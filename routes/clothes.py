from flask import Blueprint, jsonify
from models import Clothes
from extensions import db

# clothes API用 Blueprint
clothes_bp = Blueprint("clothes", __name__)

# 仮データ
mock_data = {
    "tops": [
        {"id": 1, "name": "白Tシャツ", "color": "#ffffff"},
        {"id": 2, "name": "黒パーカー", "color": "#333333"},
        {"id": 3, "name": "青シャツ",   "color": "#aaccff"},
        {"id": 4, "name": "赤ニット",   "color": "#ffcccc"},
    ],
    "bottoms": [
        {"id": 1, "name": "デニム",     "color": "#336699"},
        {"id": 2, "name": "チノパン",   "color": "#ddccaa"},
        {"id": 3, "name": "スカート",   "color": "#ffaaaa"},
    ]
    }

@clothes_bp.route("/api/clothes", methods=["GET"])
def get_clothes():
    """
    服データを取得するAPI
    """
    clothes = Clothes.query.all()
    return jsonify([
        {"id": c.id, "image_path": c.image_path, "genre": c.genre, "color": c.color, "created_at": c.created_at, "updated_at":c.updated_at} for c in clothes
    ])

from flask import Blueprint, request, jsonify
from models import Clothes
from extensions import db

# Suggest関連API用 Blueprint
suggest_bp = Blueprint("suggest", __name__)

@suggest_bp.route("/api/suggest", methods=["GET"])
def select():
    """
    Clothes一覧を取得するAPI
    """
    #いったんid1を返す
    clothes = Clothes.query.get(1)
    if clothes is None:
        return jsonify({"error": "not found"}), 404
    
    return jsonify({
        "id": clothes.id,
        "name": clothes.name,
        "color": clothes.color,
        "image": clothes.image
    })

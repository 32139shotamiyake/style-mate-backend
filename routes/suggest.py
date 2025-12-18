from flask import Blueprint, request, jsonify, url_for
from models import Clothes
from extensions import db
from sqlalchemy.sql import func

# Suggest関連API用 Blueprint
suggest_bp = Blueprint("suggest", __name__)

@suggest_bp.route("/api/suggest", methods=["GET"])
def suggest():
    """
    Clothes一覧を取得するAPI
    """
    print(Clothes.query.count())
    #ランダムなidを返す
    clothes = Clothes.query.order_by(func.rand()).first()

    if clothes is None:
        return jsonify({"error": "not found"}), 404
    
    return jsonify({
        "id": clothes.id,
        "genre":clothes.genre,
        "color": clothes.color,
        "image_path": url_for(
            "static",
            filename=clothes.image_path,
            _external=True
            )
    })

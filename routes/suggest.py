from flask import Blueprint, request, jsonify, url_for
from models import Clothes
from extensions import db
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
from sqlalchemy import or_, select

# Suggest関連API用 Blueprint
suggest_bp = Blueprint("suggest", __name__)

@suggest_bp.route("/api/suggest/<int:id>", methods=["POST"])
def suggest(id):
    """
    服の提案をするAPI
    """
    clothes = Clothes.query.get(id)

    if clothes is None:
        return jsonify({"error": "not found"}), 404

    # genreを取得
    genre = clothes.genre

    bottoms=None
    tops = None
    #ジャンルがtopのとき
    if genre == "Top":
        bottoms = (
            Clothes.query.filter_by(genre="bottom")
            .order_by(func.rand())
            .first()
        )
        if bottoms is None:
            return jsonify({"error":"not found"}),404
        return jsonify({
            "id": bottoms.id,
            "genre":bottoms.genre,
            "color": bottoms.color,
            "image_path": url_for(
            "static",
            filename=bottoms.image_path,
            _external=True
            )
        })
    
    #ジャンルがbottomのとき
    if genre == "Bottom":
        tops=(
            Clothes.query.filter_by(genre="top")
            .order_by(func.rand())
            .first()
        )
        if tops is None:
            return jsonify({"error":"not found"}),404
        return jsonify({
        "id": tops.id,
        "genre":tops.genre,
        "color": tops.color,
        "image_path": url_for(
            "static",
            filename=tops.image_path,
            _external=True
            )
        })
    return jsonify({"error":"genre is not fine"}),400
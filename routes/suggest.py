from flask import Blueprint, request, jsonify, url_for
from models import Clothes
from extensions import db
import uuid
import os
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
from sqlalchemy import or_, select

# Suggest関連API用 Blueprint
suggest_bp = Blueprint("suggest", __name__)

@suggest_bp.route("/api/suggest", methods=["POST"])
def suggest():
    """
    Clothes一覧を取得するAPI
    """
    # リクエストに画像があるか確認
    file = request.files.get("image")

    #リクエストにジャンルがあるか確認
    genre=request.form.get("genre")

    #リクエストに色があるか確認
    color=request.form.get("color")

    #ファイル名が空か確認
    if not file or not genre or not color or file.filename == "":
        return jsonify({"error": "image, genre, color are required"}), 400

    # 安全なファイル名に変換
    filename = secure_filename(file.filename)

    # ファイル名の衝突を回避
    ext = os.path.splitext(filename)[1].lower()
    filename = f"{uuid.uuid4().hex}{ext}"

    #拡張子なしファイル対策
    if not ext:
        return jsonify({"error": "invalid file extension"}), 400

    #画像ファイル以外をはじく
    ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif"}

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "unsupported file type"}), 400
    
    bottoms=None
    tops = None
    #ジャンルがtopのとき
    if genre == "top":
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
    if genre == "bottom":
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
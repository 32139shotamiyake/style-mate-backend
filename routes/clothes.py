from flask import Blueprint, jsonify,request, current_app, url_for
from models import Clothes
from extensions import db
from werkzeug.utils import secure_filename
from pathlib import Path
import uuid
import os

# clothes API用 Blueprint
clothes_bp = Blueprint("clothes", __name__)

@clothes_bp.route("/api/clothes",methods=["POST"])
def post_clothes():
    """
    画像をアップロードするAPI
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
    
    # 保存先パスを生成
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    #ファイル保存
    file.save(save_path)

    # DBに保存するパスを生成
    relative_path = str(
        Path(current_app.config["RELATIVE_UPLOAD_FOLDER"]) / filename
    )

    cloth=Clothes(image_path=relative_path,genre=genre,color=color)

    db.session.add(cloth)

    db.session.commit()

    return jsonify({
        "genre": genre,
        "color": color,
        "image_url": url_for(
            "static",
            filename=relative_path,
            _external=True
            )
    }), 201

@clothes_bp.route("/api/clothes", methods=["GET"])
def get_clothes():
    """
    服データを取得するAPI
    """
    clothes = Clothes.query.all()
    return jsonify([
        {"id": c.id, 
         "image_path": url_for(
            "static",
            filename=c.image_path,
            _external=True
            ), 
        "genre": c.genre, 
        "color": c.color, 
        "created_at": c.created_at.isoformat(), 
        "updated_at":c.updated_at.isoformat() if c.updated_at else None} for c in clothes
        ])

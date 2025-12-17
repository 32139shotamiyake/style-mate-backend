from flask import Blueprint, jsonify,request, current_app, url_for
from models import Clothes
from extensions import db
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
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
    relative_path = (Path(current_app.config["RELATIVE_UPLOAD_FOLDER"]) / filename).as_posix()

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

@clothes_bp.route("/api/clothes/<int:id>", methods=["DELETE"])
def delete_clothes(id):
    #対象レコード取得
    clothes = Clothes.query.get_or_404(id)
    
    try:
        #画像パスを退避
        image_path=clothes.image_path
        if image_path:
            #URL -> ファイルパスに変換
            filename=os.path.basename(image_path)
            file_path=os.path.join(current_app.config["UPLOAD_FOLDER"],filename)
            print(file_path)
        else:
            file_path = None

        #DB削除
        db.session.delete(clothes)
        db.session.flush()

        #画像削除
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        #両方成功したらcommit
        db.session.commit()

        return jsonify({"message":"deleted successfully"})
    
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error":str(e)}),500
    
    """
    #受け取ったidの行を取得
    clothes = Clothes.query.get(id)

    #なかったらエラー
    if clothes is None:
        return jsonify({"error": "not found"}), 404

    #画像ファイル削除
    if clothes.image_path:
        image_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            os.path.basename(clothes.image_path)
        )
        if os.path.exists(image_path):
            os.remove(image_path)
            
    #dbから削除
    db.session.delete(clothes)
    db.session.commit()

    return jsonify({"message": "deleted"})
"""
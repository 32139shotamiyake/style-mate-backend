from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

# アップロードAPI用 Blueprint
upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/api/upload", methods=["POST"])
def upload_file():
    """
    画像をアップロードするAPI
    """

    # リクエストに画像があるか確認
    file = request.files.get("image")
    if not file or file.filename == "":
        return jsonify({"error": "No file"}), 400

    # 安全なファイル名に変換
    filename = secure_filename(file.filename)

    # 保存先パスを生成
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    #ファイル保存
    file.save(path)

    return jsonify({
        "message": "File uploaded successfully",
        "url": f"http://localhost:5000/static/images/{filename}"
    })

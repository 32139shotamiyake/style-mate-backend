import os
import base64
import requests

from flask import Blueprint, request, jsonify, url_for, current_app
from models import Clothes
from extensions import db
from sqlalchemy.sql import func

# Suggest関連API用 Blueprint
suggest_bp = Blueprint("suggest", __name__)

# ★ここにAWSのAPIエンドポイントを設定してください
AWS_API_URL = "https://wcvdm75ex0.execute-api.ap-southeast-2.amazonaws.com/default/Fashion_API/recommend"


@suggest_bp.route("/api/suggest/<int:id>", methods=["POST"])
def suggest(id):
    """
    AIを使って服の提案をするAPI
    """
    # 1. 基準となる服（ユーザーが選んだ服）を取得
    target_cloth = Clothes.query.get(id)

    if target_cloth is None:
        return jsonify({"error": "not found"}), 404

    # 2. 画像ファイルをBase64文字列に変換する
    # ※ image_pathが 'img/photo.jpg' のような相対パスだと仮定し、
    # staticフォルダへの絶対パスを作ります
    image_file_path = os.path.join(
        current_app.root_path, "static", target_cloth.image_path
    )

    base64_string = ""

    try:
        with open(image_file_path, "rb") as img_file:
            base64_string = base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        # 画像がない場合はAI判定できないのでエラー、またはランダム処理へ
        print(f"Error: Image file not found at {image_file_path}")
        return jsonify({"error": "Image file missing"}), 500

    # 3. AWSのAIサーバーに問い合わせる
    # DBのジャンル(Top/Bottom)をAPIの形式(upper/lower)に変換
    api_target_type = "upper" if target_cloth.genre == "Top" else "lower"

    recommended_colors = []
    try:
        payload = {
            "image_base64": base64_string,
            "target_type": api_target_type,
        }

        # AI APIを叩く
        response = requests.post(AWS_API_URL, json=payload, timeout=10)

        if response.status_code == 200:
            data = response.json()
            # [{"color_name": "Beige", ...}, ...] のリストを取得
            recommended_colors = data.get("recommendations", [])
            print(f"AI Recommendations: {[r['color_name'] for r in recommended_colors]}")
        else:
            print(f"AI API Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"API Connection Failed: {e}")
        # AIが失敗しても止まらないように、空リストのまま進む（後でランダムになる）

    # 4. 提案するアイテム（相方）を決める
    suggested_item = None

    # 探すべきジャンル (TopならBottom, BottomならTop)
    target_genre = "Bottom" if target_cloth.genre == "Top" else "Top"

    # A. AIのおすすめ順にDBを探す
    for rec in recommended_colors:
        color_name = rec["color_name"]  # "Beige" や "Black" など

        # その色、かつターゲットジャンルの服をDBから探す
        # ※ランダムで1つ取得することで、同じ色の服が複数あっても毎回違うのが出るようにする
        candidate = (
            Clothes.query.filter_by(genre=target_genre, color=color_name)
            .order_by(func.rand())
            .first()
        )

        if candidate:
            suggested_item = candidate
            print(f"Found matching item! Color: {color_name}, ID: {candidate.id}")
            break  # 見つかったらループ終了

    # B. AIのおすすめで見つからなかった場合（またはAIがエラーだった場合）
    # 従来どおり、ジャンルだけでランダムに1枚選ぶ
    if suggested_item is None:
        print("Fallback to random selection")
        suggested_item = (
            Clothes.query.filter_by(genre=target_genre).order_by(func.rand()).first()
        )

    # それでもなければ404
    if suggested_item is None:
        return jsonify({"error": "not found"}), 404

    # 5. 結果を返す
    return jsonify(
        {
            "id": suggested_item.id,
            "genre": suggested_item.genre,
            "color": suggested_item.color,
            "image_path": url_for(
                "static",
                filename=suggested_item.image_path,
                _external=True,
            ),
            # デバッグ用にAIが選んだ色だったかを教えてあげるのも親切かも
            "ai_recommended": bool(recommended_colors),
        }
    )

import os
from flask import Flask,jsonify,request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

# Flaskアプリのインスタンスを作成（これがサーバーの本体になります）
app = Flask(__name__)

CORS(app)

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
#文字化け防止
app.config['JSON_AS_ASCII'] = False

# MySQLに接続するための情報
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': "mysql",
      'password': "NewPassword",
      'host': "localhost",
      'db_name': "clothes"
  })
# おまじない
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# dbの初期化
db = SQLAlchemy(app)

class Memo(db.Model):
    __tablename__ = "memos"

    id = db.Column(db.Integer, primary_key=True)
    memo = db.Column(db.String(255), nullable=True)


class tops(db.Model):
    __tablename__ = "tops"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(7), nullable=False)
    image = db.Column(db.String(255), nullable=True)


class bottoms(db.Model):
    __tablename__ = "bottoms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    color = db.Column(db.String(7), nullable=False)
    image = db.Column(db.String(255), nullable=True)
# テーブルの生成
with app.app_context():
    db.create_all()

UPLOAD_FOLDER=os.path.join(os.path.dirname(__file__),'static','images')
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
# --- ルーティングの設定 ---

# 「/api/clothes」にGETリクエストが来たら動く
@app.route('/api/clothes', methods=['GET'])
def get_clothes():
    # Pythonの辞書(mock_data)を、JSON形式の文字列に変換して返す
    return jsonify(mock_data)

@app.route("/insert", methods=["POST"])
def insert():
    # postの受け取り
    memo_txt = request.form["memo"]
    # Memoの生成
    memo = Memo(memo=memo_txt)
    # MemoをDBに反映
    db.session.add(memo)
    db.session.commit()
    return jsonify({"message": "Inserted successfully"})

@app.route("/select", methods=["GET"])
def select():
    memos = Memo.query.all()
    memos_json = [
        {"id": memo.id, "memo": memo.memo}
        for memo in memos
    ]
    return jsonify(memos_json)

@app.route('/api/upload',methods=['POST'])
def upload_file():
    #1.リクエストの中に「image」というデータがあるか
    if 'image' not in request.files:
        return jsonify({"error":"No image part"}),

    file = request.files['image']

    #2.ファイル名が空っぽじゃないかチェック
    if file.filename == '':
        return jsonify({"error":"No selected file"})
    
    #3.ファイルがあれば保存処理へ
    filename=secure_filename(file.filename)
    save_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    #4.フロントエンドに「ここに保存したよ」とURLを送信する
    image_url=f"http://localhost:5000/static/images/{filename}"

    print(f"保存成功：{save_path}")
    return jsonify({
        "message":"File uploaded successfully",
        "url":image_url
    })
# 「http://〜/」というルートURLにアクセスが来た時の処理
@app.route('/')
def home():
    return "Hello, StyleMate Backend!"

# --- サーバーの起動 ---
# python app.py で実行された時だけ動くおまじない
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)
    # debug=True にすると、コードを保存するたびに自動で再起動してくれます
    # port=5000 はデフォルトですが、明示的に書いておきます
    app.run(debug=True, port=5000)

# StyleMate Backend

Flask + MySQL を用いた **StyleMate** のバックエンドリポジトリです。
2人開発を前提とし、`develop` ブランチで開発、`main` ブランチを安定版として管理します。

---

## 📌 概要

- フレームワーク：Flask
- DB：MySQL
- ORM：SQLAlchemy
- マイグレーション：Flask-Migrate
- 開発人数：2人

---

## 📂 ディレクトリ構成

```
style-mate-backend/
├── migrations/         #マイグレーション(Git管理)
├── models              #SQLAlchemyモデル
│   ├── __init__.py
│   └── memo.py
├── routes              #ルーティング(Blueprint)
│   ├── __init__.py
│   ├── clothes.py
│   ├── memo.py
│   └── upload.py
├── .env.example        #環境変数テンプレート
├── .gitignore          #gitで管理しないものの定義
├── app.py              #アプリ起動点
├── config.py           #設定(DB等)
├── extensions.py       #db / migrate 定義
├── readme.md
├── requirements.txt    #依存関係
└── test_upload.html    #画像アップロードテスト用
```

---

## 🚀 環境構築手順

### 1️⃣ リポジトリをクローン

```bash
git clone <repository-url>
cd style-mate-backend
```

---

### 2️⃣ 仮想環境の作成・有効化

```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# macOS / Linux
source venv/bin/activate
```

---

### 3️⃣ 依存関係のインストール

```bash
pip install -r requirements.txt
```

---

### 4️⃣ .env の作成

`.env.example` をコピーして `.env` を作成してください。

```env
DB_USER=mysql
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=clothes
```

※ `.env` は **Git に追加しません**

---

### 5️⃣ DB マイグレーション

```bash
flask db upgrade
```

---

### 6️⃣ サーバー起動

```bash
python app.py
```

ブラウザで以下にアクセスできれば成功です。

```
http://localhost:5000/
```

---

## 🌱 ブランチ運用ルール

- `main` ：安定版（直接 push 禁止）
- `develop` ：開発用ブランチ
- `feature/*` ：機能ごとの作業ブランチ

### 作業手順

1. `develop` から `feature/*` を作成
2. 機能実装
3. `feature/*` → `develop` に Pull Request
4. 動作確認後マージ

---

## 🧬 マイグレーション運用ルール

### モデルを変更した人

```bash
flask db migrate -m "説明"
flask db upgrade
git add migrations
git commit
```

### それ以外の人

```bash
git pull
flask db upgrade
```

---

## 🗃 データ同期について

- **DB構造（models / migrations）のみ同期**
- INSERT したデータ（行）は同期しない
- 初期データが必要な場合は `seed.py` を使用

---

## ⚠️ 注意事項

- `db.create_all()` は使用しません
- `migrations/` フォルダは必ず Git 管理します
- `debug=True` は develop まで

---

## 🧪 よくあるトラブル

### Q. DB接続エラーが出る
- MySQL が起動しているか
- `.env` の値が正しいか
- `flask db upgrade` を実行したか

---

## 📌 補足

- 本リポジトリは学習・課題用途を想定しています
- 本番運用時は設定・セキュリティの見直しが必要です

---

## 👥 開発メンバー

- 三宅翔太
- 櫻井唯人


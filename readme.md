# StyleMate Backend

Flask + MySQL を用いた **StyleMate** のバックエンドリポジトリです。
2人開発を前提とし、`develop` ブランチで開発、`main` ブランチを安定版として管理します。

---

## 📌 概要

* フレームワーク：Flask
* DB：MySQL
* ORM：SQLAlchemy
* マイグレーション：Flask-Migrate
* 開発人数：2人

---

## 📂 ディレクトリ構成

```
style-mate-backend/
│
├─ app.py              # アプリ起動点
├─ config.py           # 設定（DB等）
├─ extensions.py       # db / migrate 定義
├─ models.py           # SQLAlchemy モデル
├─ routes/             # ルーティング（Blueprint）
│   ├─ __init__.py
│   ├─ clothes.py
│   └─ memo.py
│
├─ migrations/         # マイグレーション（Git管理）
├─ requirements.txt    # 依存関係
├─ .env.example        # 環境変数テンプレート
└─ README.md
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
   waitress-serve --listen=127.0.0.1:5000 wsgi:app
```

ブラウザで以下にアクセスできれば成功です。

```
http://localhost:5000/
```

---

## 🌱 ブランチ運用ルール

* `main` ：安定版（直接 push 禁止）
* `develop` ：開発用ブランチ
* `feature/*` ：機能ごとの作業ブランチ

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

* **DB構造（models / migrations）のみ同期**
* INSERT したデータ（行）は同期しない
* 初期データが必要な場合は `seed.py` を使用

---

## ⚠️ 注意事項

* `db.create_all()` は使用しません
* `migrations/` フォルダは必ず Git 管理します
* `debug=True` は develop まで

---

## 🧪 よくあるトラブル

### Q. DB接続エラーが出る

* MySQL が起動しているか
* `.env` の値が正しいか
* `flask db upgrade` を実行したか

---

## 📌 補足

* 本リポジトリは学習・課題用途を想定しています
* 本番運用時は設定・セキュリティの見直しが必要です

---

## 👥 開発メンバー

* 名前1
* 名前2

---

## 起動方法（重要）

### 開発環境（Windows / macOS 共通）

本プロジェクトでは **app.run は使用しません**。
WSGI サーバー（waitress / gunicorn）経由で起動します。

```bash
# 仮想環境を有効化後
waitress-serve --listen=127.0.0.1:5000 wsgi:app
```

ブラウザで以下にアクセスしてください：

```
http://localhost:5000
```

---

## ディレクトリ構成（抜粋）

```text
style-mate-backend/
├── app.py          # Flask アプリ生成（create_app）
├── wsgi.py         # WSGI エントリーポイント
├── routes/         # ルーティング（Blueprint）
├── models/         # DB モデル
├── extensions.py   # db などの拡張機能
├── static/images/  # 画像アップロード先（自動生成）
├── .env.example    # 環境変数サンプル
└── README.md
```

---

## 開発ルール（2人開発）

* **main** : 安定版のみ（直接 push しない）
* **develop** : 開発統合ブランチ
* **feature/** : 機能ごとに作成し、完了後は削除

```bash
git checkout develop
git checkout -b feature/add-upload-api
```

---

## データベース初期化手順（重要）

### 新しいデータベースを使い始める場合

Flask-Migrate を使用しているため、**DB 名を変更しただけではテーブルは作成されません**。
以下の手順で初期化してください。

---

### 1. MySQL にデータベースを作成

```sql
CREATE DATABASE stylemate_db;
```

※ データベース名は `.env` の `DB_NAME` と一致させてください。

---

### 2. 環境変数を設定（.env）

```env
DB_USER=mysql
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=stylemate_db
```

---

### 3. 初期テーブルを作成（初回のみ）

新しい DB は Alembic の履歴を持たないため、
**現在のモデル構造でテーブルを作成し、履歴を同期します。**

```bash
# 初回のみ実行
flask db stamp head
```

※ この時点で DB にはテーブルが存在している必要があります。

---

### 4. 以降の運用

モデルを変更した場合は、以下の手順で反映します。

```bash
flask db migrate -m "describe change"
flask db upgrade
```

---

### 注意事項

* `flask db upgrade` は **既存 DB には実行してOK**
* **空の新 DB に直接 upgrade するとエラーになります**
* insert されたデータ（行）は migrate では同期されません

---

## 環境変数について

`.env` ファイルを作成し、以下を設定してください。

```env
DB_USER=mysql
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=clothes
```

※ `.env` は **GitHub に push しません**

---

## 備考

* DB スキーマ変更時は Flask-Migrate を使用
* 画像保存ディレクトリは起動時に自動生成されます

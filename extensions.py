from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# SQLAlchemyのインスタンスを作成
# app.py で init_app() される
db = SQLAlchemy()
migrate = Migrate()
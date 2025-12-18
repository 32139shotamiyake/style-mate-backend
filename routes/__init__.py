from .memo import memo_bp
from .clothes import clothes_bp
from .upload import upload_bp
from .suggest import suggest_bp

def register_routes(app):
    """
    全てのBlueprintをFlaskアプリに登録
    """
    app.register_blueprint(memo_bp)
    app.register_blueprint(clothes_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(suggest_bp)

    # トップページ
    @app.route("/")
    def home():
        return "Hello, StyleMate Backend!"

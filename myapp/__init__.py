import os
from flask import Flask
from .extensions import db, login_manager, csrf


def create_app(config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-ganti-di-produksi")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    if config:
        app.config.update(config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Ke mana pengguna diarahkan jika belum login
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Silakan login untuk mengakses halaman ini."
    login_manager.login_message_category = "warning"

    from .auth import bp as auth_bp
    from .main import bp as main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app

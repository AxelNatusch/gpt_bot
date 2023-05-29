from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secretkey"

    from .views import views
    from .chat import chat

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(chat, url_prefix="/")

    return app

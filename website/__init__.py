from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    if not path.exists("website/" + DB_NAME):
        create_database(app)
        init_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    try:
        db.create_all(app=app)
        print("Created Database!")
    except Exception as e:
        raise (e)


def init_database(app):
    from .models import UserLevel

    with app.app_context():
        admin = UserLevel(level=1, name="admin")
        manager = UserLevel(level=2, name="manager")
        employee = UserLevel(level=3, name="employee")
        try:
            db.session.add(admin)
            db.session.add(manager)
            db.session.add(employee)
            db.session.commit()
            print("Database Initialized")
        except Exception as e:
            raise (e)

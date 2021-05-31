from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from datetime import datetime

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.cfg")

    db.init_app(app)

    from .view import view
    from .auth import auth

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    if not path.exists("website/" + app.config.get("DB_NAME")):
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
    from .models import AppointmentTimes

    with app.app_context():
        userlevels = []
        userlevels.append(UserLevel(level=1, name="admin"))
        userlevels.append(UserLevel(level=2, name="manager"))
        userlevels.append(UserLevel(level=3, name="employee"))
        strptime = datetime.strptime
        timeslots = []
        timeslots.append(
            AppointmentTimes(timeslot=strptime("2021-06-01 12:00", "%Y-%m-%d %H:%M"))
        )
        timeslots.append(
            AppointmentTimes(timeslot=strptime("2021-06-01 13:00", "%Y-%m-%d %H:%M"))
        )
        timeslots.append(
            AppointmentTimes(timeslot=strptime("2021-06-01 14:00", "%Y-%m-%d %H:%M"))
        )
        try:
            for userlevel in userlevels:
                db.session.add(userlevel)

            for timeslot in timeslots:
                db.session.add(timeslot)

            db.session.commit()
            print("Database Initialized")
        except Exception as e:
            raise (e)

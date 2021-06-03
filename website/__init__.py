from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from datetime import datetime
import subprocess
from os import environ

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.update(
        MAIL_SERVER=environ["MAIL_SERVER"],
        MAIL_USERNAME=environ["MAIL_USERNAME"],
        MAIL_PASSWORD=environ["MAIL_PASSWORD"],
        MAIL_PORT=environ["MAIL_PORT"],
        MAIL_USE_SSL=environ["MAIL_USE_SSL"],
        MAIL_USE_TSL=environ["MAIL_USE_TSL"],
        DB_NAME=environ["DB_NAME"],
        SECRET_KEY=environ["SECRET_KEY"],
        SQLALCHEMY_DATABASE_URI=environ["SQLALCHEMY_DATABASE_URI"],
        SQLALCHEMY_TRACK_MODIFICATIONS=environ["SQLALCHEMY_TRACK_MODIFICATIONS"],
        ACCOUNT_EXPIRE_VERIFY_TIME=environ["ACCOUNT_EXPIRE_VERIFY_TIME"],
        ADMIN_EMAIL=environ["ADMIN_EMAIL"],
        ADMIN_PASS=environ["ADMIN_PASS"],
    )

    db.init_app(app)

    from .view import view
    from .auth import auth

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    dbpath = "website/" + environ["DB_NAME"]
    if not path.exists(dbpath):
        create_database(dbpath)
        init_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(dbpath):
    subprocess.call(["sqlite3", dbpath, ".read initdb.sql"])
    return


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

        # create admin user if exists
        email = environ["ADMIN_EMAIL"]
        passwd = environ["ADMIN_PASS"]
        if email != "" and passwd != "":
            from .models import User
            from werkzeug.security import generate_password_hash

            admin = User(
                userLevelId=1,
                email=email,
                password=generate_password_hash(passwd, "sha256"),
                name="admin",
                verified=True,
            )
            try:
                db.session.add(admin)
                db.session.commit()
            except Exception as e:
                raise (e)

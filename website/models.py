from flask_login import UserMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from datetime import datetime
from . import db


class UserLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ulevel = db.Column(db.Integer, unique=True)
    uname = db.Column(db.String(64))


class ApptUsers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userlevelid = db.Column(db.Integer, ForeignKey(UserLevel.ulevel))
    email = db.Column(db.String(64), nullable=False, unique=True)
    upassword = db.Column(db.String(256), nullable=False)
    uname = db.Column(db.String(64), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    creationdate = db.Column(db.DateTime, default=datetime.now())


class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, ForeignKey(ApptUsers.id))
    email = db.Column(db.String(64), nullable=False)
    loginstatus = db.Column(db.String(64), nullable=False)
    logintime = db.Column(db.DateTime, default=datetime.now())


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(64), nullable=False)


class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sname = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Numeric(precision=6, scale=2), default=0)


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(64), nullable=False)
    serviceid = db.Column(db.Integer, ForeignKey(Services.id), nullable=True)
    employeeid = db.Column(db.Integer, ForeignKey(Employees.id), nullable=True)
    apptdatetime = db.Column(db.DateTime, default=datetime.now)
    tips = db.Column(db.Numeric(precision=6, scale=2), default=0)
    total = db.Column(db.Numeric(precision=6, scale=2), default=0)
    __table_args__ = (
        UniqueConstraint("employeeid", "apptdatetime", name="_employee_appt_uc"),
    )

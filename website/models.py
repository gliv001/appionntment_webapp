from flask_login import UserMixin
from sqlalchemy import ForeignKey
from datetime import datetime
from . import db


class UserLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(64))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userLevelId = db.Column(db.Integer, ForeignKey(UserLevel.level))
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64), nullable=False)


class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey(User.id))
    email = db.Column(db.String(64), nullable=False)
    status = db.Column(db.String(64), nullable=False)
    loginTime = db.Column(db.DateTime, default=datetime.now())


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Numeric, default=0)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(64), nullable=False)
    serviceId = db.Column(db.Integer, ForeignKey(Service.id), nullable=True)
    employeeId = db.Column(db.Integer, ForeignKey(Employee.id), nullable=True)
    apptDateTime = db.Column(db.DateTime, default=datetime.now)
    tips = db.Column(db.Numeric, default=0)
    total = db.Column(db.Numeric, default=0)

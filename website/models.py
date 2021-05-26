from . import db
from sqlalchemy import ForeignKey
from datetime import datetime


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

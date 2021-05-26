from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey
from datetime import datetime

db_path = "sqlite:///backend.db"
db = SQLAlchemy()


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


if __name__ == "__main__":
    engine = create_engine(db_path, echo=False)
    db.metadata.create_all(engine)

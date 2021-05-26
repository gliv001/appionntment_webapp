from flask import Blueprint, render_template, request, redirect
from .models import Appointment, Employee, Service, db
from datetime import datetime

views = Blueprint("views", __name__)


@views.route("/", methods=["POST", "GET"])
@views.route("/appointments", methods=["POST", "GET"])
def appointment_actions():
    if request.method == "POST":
        client = request.form["client"]
        service = request.form.get("service")
        employee = request.form.get("employee")
        date = request.form["appt_date"]
        time = request.form["appt_time"]
        appt = datetime.strptime(date + time, "%Y-%m-%d%H:%M")
        tip = request.form["tip"]
        new_appt = Appointment(
            client=client,
            serviceId=service,
            employeeId=employee,
            apptDateTime=appt,
            tips=tip,
        )
        try:
            db.session.add(new_appt)
            db.session.commit()
            return redirect("/appointments")
        except Exception as error:
            print(error)
            return "There was an issue adding a new appointment"
    else:
        employeeList = Employee.query.all()
        serviceList = Service.query.all()
        appointments = (
            db.session.query(
                Appointment,
                Service.name.label("service"),
                Employee.name.label("employee"),
            )
            .select_from(Appointment)
            .join(Service)
            .join(Employee)
            .all()
        )
        for appt, service, employee in appointments:
            print(appt.client, service, employee)

        return render_template(
            "appointments.html",
            employeeList=employeeList,
            serviceList=serviceList,
            appointments=appointments,
        )


@views.route("/appointments/update/<int:id>", methods=["POST", "GET"])
def appointment_update(id):
    select_appointment = Appointment.query.get_or_404(id)
    select_service = Service.query.get(select_appointment.serviceId)
    select_employee = Employee.query.get(select_appointment.employeeId)
    if request.method == "POST":
        select_appointment.client = request.form["client"]
        select_appointment.service = request.form["service"]
        select_appointment.employee = request.form["employee"]
        date = request.form["appt_date"]
        time = request.form["appt_time"]
        select_appointment.apptDateTime = datetime.strptime(
            date + time, "%Y-%m-%d%H:%M"
        )
        select_appointment.tips = request.form["tip"]
        try:
            db.session.commit()
            return redirect("/appointments")
        except Exception as error:
            print(error)
            return "There was an issue updating an appointment"
    else:
        employeeList = Employee.query.all()
        serviceList = Service.query.all()

        return render_template(
            "appointments_update.html",
            serviceList=serviceList,
            employeeList=employeeList,
            appointment=select_appointment,
            appt_date=datetime.strftime(select_appointment.apptDateTime, "%Y-%m-%d"),
            appt_time=datetime.strftime(select_appointment.apptDateTime, "%H:%M"),
            service=select_service,
            employee=select_employee,
        )


@views.route("/appointments/delete/<int:id>")
def appointment_delete(id):
    select_appointment = Appointment.query.get_or_404(id)
    try:
        db.session.delete(select_appointment)
        db.session.commit()
        return redirect("/appointments")
    except Exception as error:
        print(error)
        return "There was an issue deleting an appointment"


@views.route("/employees", methods=["POST", "GET"])
def employee_actions():
    if request.method == "POST":
        employee_name = request.form["name"]
        new_employee = Employee(name=employee_name)
        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect("/employees")
        except Exception as error:
            print(error)
            return "There was an issue adding a new employee"
    else:
        e = Employee.query.order_by(Employee.id).all()
        return render_template("employees.html", employees=e)


@views.route("/employees/update/<int:id>", methods=["POST", "GET"])
def employee_update(id):
    selected_employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        selected_employee.name = request.form["name"]
        try:
            db.session.commit()
            return redirect("/employees")
        except Exception as error:
            print(error)
            return "There was an issue updating an employee"
    else:
        return render_template("employees_update.html", employee=selected_employee)


@views.route("/employees/delete/<int:id>")
def employee_delete(id):
    selected_employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(selected_employee)
        db.session.commit()
        return redirect("/employees")
    except Exception as error:
        print(error)
        return "There was an issue deleting an employee"


@views.route("/services", methods=["POST", "GET"])
def service_actions():
    if request.method == "POST":
        service_name = request.form["name"]
        service_price = request.form["price"]
        new_service = Service(name=service_name, price=service_price)
        try:
            db.session.add(new_service)
            db.session.commit()
            return redirect("/services")
        except Exception as error:
            print(error)
            return "There was an issue adding a new service"
    else:
        s = Service.query.order_by(Service.id).all()
        return render_template("services.html", services=s)


@views.route("/services/update/<int:id>", methods=["POST", "GET"])
def service_update(id):
    selected_service = Service.query.get_or_404(id)
    if request.method == "POST":
        selected_service.name = request.form["name"]
        selected_service.price = request.form["price"]
        try:
            db.session.commit()
            return redirect("/services")
        except Exception as error:
            print(error)
            return "There was an issue updating an service"
    else:
        return render_template("services_update.html", service=selected_service)


@views.route("/services/delete/<int:id>")
def service_delete(id):
    selected_service = Service.query.get_or_404(id)
    try:
        db.session.delete(selected_service)
        db.session.commit()
        return redirect("/services")
    except Exception as error:
        print(error)
        return "There was an issue deleting an service"

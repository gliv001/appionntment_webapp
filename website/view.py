from website.forms import AppointmentForm, EmployeeForm, ServiceForm
from flask import Blueprint, render_template, request, redirect, flash
from flask.helpers import url_for
from .models import Appointment, Employee, Service, db
from datetime import datetime
from flask_login import login_required, current_user

view = Blueprint("view", __name__)


@view.route("/", methods=["POST", "GET"])
@view.route("/appointments", methods=["POST", "GET"])
@login_required
def appointment_home():
    form = AppointmentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            client = form.client.data
            service = form.service.data
            employee = form.employee.data
            appt_date = form.appt_date.data
            appt_time = form.appt_time.data
            tip = form.tip.data
            total = form.total.data
            if tip == "":
                tip = 0
            new_appt = Appointment(
                client=client,
                serviceId=service,
                employeeId=employee,
                apptDateTime=datetime.strptime(
                    f"{appt_date} {appt_time}", "%Y-%m-%d %H:%M:%S"
                ),
                tips=tip,
                total=total,
            )
            try:
                db.session.add(new_appt)
                db.session.commit()
            except Exception as error:
                print(error)
                flash("There was an issue adding a new appointment", category="error")
        return redirect("/appointments")

    employeeList = Employee.query.all()
    serviceList = Service.query.all()
    form.employee.choices = [(e.id, e.name) for e in employeeList]
    form.service.choices = [(s.id, f"{s.name} ${s.price}") for s in serviceList]

    if len(serviceList) < 1:
        flash("There are no services, Please add services first.", category="error")

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

    return render_template(
        "view/appointments.jinja2",
        form=form,
        appointments=appointments,
        user=current_user,
    )


@view.route("/appointments/update/<int:id>", methods=["POST", "GET"])
@login_required
def appointment_update(id):
    form = AppointmentForm()
    select_appointment = Appointment.query.get_or_404(id)
    if request.method == "POST":
        if form.validate_on_submit():
            select_appointment.client = form.client.data
            select_appointment.service = form.service.data
            select_appointment.employee = form.employee.data
            select_appointment.apptDateTime = datetime.strptime(
                f"{form.appt_date.data} {form.appt_time.data}", "%Y-%m-%d %H:%M:%S"
            )
            select_appointment.tips = form.tip.data
            try:
                db.session.commit()
            except Exception as error:
                print(error)
                flash("There was an issue updating an appointment", category="error")
        return redirect("/appointments")

    employeeList = Employee.query.all()
    serviceList = Service.query.all()
    form.employee.choices = [(e.id, e.name) for e in employeeList]
    form.service.choices = [(s.id, f"{s.name} ${s.price}") for s in serviceList]

    form.client.default = select_appointment.client
    form.service.default = select_appointment.serviceId
    form.employee.default = select_appointment.employeeId
    date = select_appointment.apptDateTime.date()
    time = select_appointment.apptDateTime.time()
    form.appt_date.default = date
    form.appt_time.default = time
    form.tip.default = select_appointment.tips
    form.total.default = select_appointment.total
    form.process()  # this is to set the default choices for services/employees

    return render_template(
        "view/appointment_update.jinja2",
        form=form,
        user=current_user,
        appointment=select_appointment,
    )


@view.route("/appointments/delete/<int:id>")
@login_required
def appointment_delete(id):
    select_appointment = Appointment.query.get_or_404(id)
    try:
        db.session.delete(select_appointment)
        db.session.commit()
    except Exception as error:
        print(error)
        flash("There was an issue deleting an appointment", category="error")
    return redirect("/appointments")


@view.route("/employees", methods=["POST", "GET"])
@login_required
def employee_home():
    form = EmployeeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            employee_name = form.name.data
            new_employee = Employee(name=employee_name)
            try:
                db.session.add(new_employee)
                db.session.commit()
            except Exception as error:
                print(error)
                flash("There was an issue adding a new employee", category="error")
        return redirect("/employees")
    e = Employee.query.order_by(Employee.id).all()
    return render_template(
        "view/employees.jinja2",
        form=form,
        employees=e,
        user=current_user,
    )


@view.route("/employees/update/<int:id>", methods=["POST", "GET"])
@login_required
def employee_update(id):
    form = EmployeeForm()
    selected_employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        if form.validate_on_submit():
            selected_employee.name = form.name.data
            try:
                db.session.commit()
            except Exception as error:
                print(error)
                flash("There was an issue updating an employee", category="error")
        return redirect("/employees")

    form.name.default = selected_employee.name
    return render_template(
        "view/employee_update.jinja2",
        form=form,
        employee=selected_employee,
        user=current_user,
    )


@view.route("/employees/delete/<int:id>")
@login_required
def employee_delete(id):
    selected_employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(selected_employee)
        db.session.commit()
    except Exception as error:
        print(error)
        flash("There was an issue deleting an employee", category="error")
    return redirect("/employees")


@view.route("/services", methods=["POST", "GET"])
@login_required
def service_home():
    form = ServiceForm()
    if request.method == "POST":
        if form.validate_on_submit():
            service_name = form.name.data
            service_price = form.price.data
            new_service = Service(name=service_name, price=service_price)
            try:
                db.session.add(new_service)
                db.session.commit()
            except Exception as error:
                print(error)
                flash("There was an issue adding a new service", category="error")
        return redirect("/services")

    s = Service.query.order_by(Service.id).all()
    return render_template(
        "view/services.jinja2",
        form=form,
        services=s,
        user=current_user,
    )


@view.route("/services/update/<int:id>", methods=["POST", "GET"])
@login_required
def service_update(id):
    form = ServiceForm()
    selected_service = Service.query.get_or_404(id)
    if request.method == "POST":
        if form.validate_on_submit():
            selected_service.name = form.name.data
            selected_service.price = form.price.data
            try:
                db.session.commit()
            except Exception as error:
                print(error)
                flash("There was an issue updating an service", category="error")
        return redirect("/services")

    form.name.default = selected_service.name
    form.price.default = selected_service.price
    return render_template(
        "view/service_update.jinja2",
        form=form,
        service=selected_service,
        user=current_user,
    )


@view.route("/services/delete/<int:id>")
@login_required
def service_delete(id):
    selected_service = Service.query.get_or_404(id)
    try:
        db.session.delete(selected_service)
        db.session.commit()
    except Exception as error:
        print(error)
        flash("There was an issue deleting an service", category="error")
    return redirect("/services")

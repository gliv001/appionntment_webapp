from website.forms import AppointmentForm, EmployeeForm, ServiceForm
from flask import Blueprint, render_template, request, redirect, flash
from flask.helpers import url_for
from .models import (
    Appointments,
    Employees,
    LoginHistory,
    Services,
    ApptUsers,
    UserLevel,
    db,
)
from datetime import datetime
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import simplejson as json

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
            new_appt = Appointments(
                client=client,
                serviceid=service,
                employeeid=employee,
                apptdatetime=datetime.strptime(
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

    employeeList = Employees.query.all()
    serviceList = Services.query.all()
    form.employee.choices = [(e.id, e.uname) for e in employeeList]
    form.service.choices = [(s.id, f"{s.sname} ${s.price}") for s in serviceList]

    if len(serviceList) < 1:
        flash("There are no services, Please add services first.", category="error")

    appointments = (
        db.session.query(
            Appointments,
            Services.sname.label("service"),
            Employees.uname.label("employee"),
        )
        .select_from(Appointments)
        .join(Services)
        .join(Employees)
        .filter(Appointments.employeeid == current_user.id)
        .all()
    )

    return render_template(
        "view/appointments.jinja2",
        form=form,
        appointments=appointments,
        user=current_user,
    )


@view.route("/appointments/table", methods=["GET"])
@login_required
def appointment_table():
    if request.args.get("viewall", default=0, type=int) == 0:
        results = (
            db.session.query(
                Appointments.id,
                Appointments.client,
                Appointments.serviceid,
                Appointments.employeeid,
                Appointments.apptdatetime,
                Appointments.tips,
                Appointments.total,
                Services.sname.label("service"),
                Employees.uname.label("employee"),
            )
            .select_from(Appointments)
            .join(Services)
            .join(Employees)
            .filter(Appointments.employeeid == current_user.id)
            .all()
        )
    else:
        results = (
            db.session.query(
                Appointments.id,
                Appointments.client,
                Appointments.serviceid,
                Appointments.employeeid,
                Appointments.apptdatetime,
                Appointments.tips,
                Appointments.total,
                Services.sname.label("service"),
                Employees.uname.label("employee"),
            )
            .select_from(Appointments)
            .join(Services)
            .join(Employees)
            .all()
        )

    appointments_dict_list = [r._asdict() for r in results]

    return json.dumps(appointments_dict_list, default=str)


@view.route("/appointments/update/<int:id>", methods=["POST", "GET"])
@login_required
def appointment_update(id):
    form = AppointmentForm()
    select_appointment = Appointments.query.get_or_404(id)
    if request.method == "POST":
        if form.validate_on_submit():
            select_appointment.client = form.client.data
            select_appointment.service = form.service.data
            select_appointment.employee = form.employee.data
            select_appointment.apptdatetime = datetime.strptime(
                f"{form.appt_date.data} {form.appt_time.data}", "%Y-%m-%d %H:%M:%S"
            )
            select_appointment.tips = form.tip.data
            try:
                db.session.commit()
            except Exception as error:
                print(error)
                flash("There was an issue updating an appointment", category="error")
        return redirect("/appointments")

    employeeList = Employees.query.all()
    serviceList = Services.query.all()
    form.employee.choices = [(e.id, e.uname) for e in employeeList]
    form.service.choices = [(s.id, f"{s.sname} ${s.price}") for s in serviceList]

    form.client.default = select_appointment.client
    form.service.default = select_appointment.serviceid
    form.employee.default = select_appointment.employeeid
    date = select_appointment.apptdatetime.date()
    time = select_appointment.apptdatetime.time()
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
    select_appointment = Appointments.query.get_or_404(id)
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
    if current_user.userlevelid >= 3:
        flash("Access denied: user privileges too low", category="error")
        return redirect("/")
    form = EmployeeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            userlevelid = form.employee_type.data
            new_employee = ApptUsers(
                userlevelid=userlevelid,
                uname=name,
                email=email,
                upassword=generate_password_hash(password, "sha256"),
                verified=True,
            )
            try:
                db.session.add(new_employee)
                db.session.commit()
                flash("New employee created!", category="success")
                return redirect("employees")
            except Exception as error:
                print(error)
                flash("There was an issue adding a new employee", category="error")

    userLevels = UserLevel.query.filter(UserLevel.ulevel >= 2)
    form.employee_type.choices = [(l.ulevel, l.uname) for l in userLevels]
    employee = Employees.query.order_by(Employees.id).all()
    return render_template(
        "view/employees.jinja2",
        form=form,
        employees=employee,
        user=current_user,
    )


@view.route("/employees/update/<int:id>", methods=["POST", "GET"])
@login_required
def employee_update(id):
    form = EmployeeForm()
    employee = ApptUsers.query.get_or_404(id)
    if request.method == "POST":
        if form.validate_on_submit():
            employee.name = form.name.data
            employee.email = form.email.data
            employee.upassword = generate_password_hash(form.password.data, "sha256")
            try:
                db.session.commit()
                return redirect("/employees")
            except Exception as error:
                print(error)
                flash("There was an issue updating an employee", category="error")

    return render_template(
        "view/employee_update.jinja2",
        form=form,
        employee=employee,
        user=current_user,
    )


@view.route("/employees/delete/<int:id>")
@login_required
def employee_delete(id):
    selected_employee = ApptUsers.query.get_or_404(id)
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
            new_service = Services(sname=service_name, price=service_price)
            try:
                db.session.add(new_service)
                db.session.commit()
                flash("New service created!", category="success")
                return redirect("services")
            except Exception as error:
                print(error)
                flash("There was an issue adding a new service", category="error")

    s = Services.query.order_by(Services.id).all()
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
    selected_service = Services.query.get_or_404(id)
    if request.method == "POST":
        if form.validate_on_submit():
            selected_service.sname = form.name.data
            selected_service.price = form.price.data
            try:
                db.session.commit()
            except Exception as error:
                print(error)
                flash("There was an issue updating an service", category="error")
        return redirect("/services")

    return render_template(
        "view/service_update.jinja2",
        form=form,
        service=selected_service,
        user=current_user,
    )


@view.route("/services/delete/<int:id>")
@login_required
def service_delete(id):
    selected_service = Services.query.get_or_404(id)
    try:
        db.session.delete(selected_service)
        db.session.commit()
    except Exception as error:
        print(error)
        flash("There was an issue deleting an service", category="error")
    return redirect("/services")


@view.route("/loginhistory")
@login_required
def login_history():
    if current_user.userlevelid > 1:
        flash("Access denied: user privileges too low", category="error")
        return redirect("/")

    logins = LoginHistory.query.order_by(LoginHistory.id.desc()).all()
    return render_template("view/loginhistory.jinja2", logins=logins, user=current_user)

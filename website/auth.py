from flask_mail import Message, Mail
from itsdangerous.exc import SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer
from website.forms import LoginForm, SignUpForm
from website.models import Employee, LoginHistory, User, UserLevel
from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    flash,
    url_for,
    current_app,
)
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        log = LoginHistory(email=email)
        user = User.query.filter_by(email=email).first()
        if user:
            is_authenticated = check_password_hash(user.password, password)
            if is_authenticated:
                flash(f"Login Success! Welcome back {user.name}", category="success")
                log.status = "login success"
                log.userId = user.id
                db.session.add(log)
                db.session.commit()
                login_user(user, remember=True)
                return redirect(url_for("view.appointment_home"))
        flash("Login Failed, Email/Password (or both) incorrect", category="error")
        log.status = "login failed"
        db.session.add(log)
        db.session.commit()
        return redirect("/login")
    return render_template(
        "auth/login.jinja2", form=form, template="form-template", user=current_user
    )


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout Successful!", category="success")
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = request.form["email"]
            name = request.form["name"]
            password = request.form["password"]
            password2 = request.form["password2"]
            user_exists = User.query.filter_by(email=email).first()
            if user_exists:
                flash("Email already exists!", category="error")
            elif email.find("@") <= 0 or email.find(".") <= 0 or len(email) <= 4:
                flash("Incorrect Email", category="error")
            elif len(name) < 2:
                flash("Name must be greater than 1", category="error")
            elif password != password2:
                flash("Passwords do not match", category="error")
            elif len(password) <= 6:
                flash("Password must be greater than 6", category="error")
            else:
                mail = Mail(current_app)
                s = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"))
                token = s.dumps(email, salt="email-confirm")
                flash("Account Pending Verification", category="success")
                email_msg = Message(
                    "Confirm Email for appointment webapp",
                    sender=current_app.config.get("MAIL_USERNAME"),
                    recipients=[current_app.config.get("MAIL_USERNAME")],
                )

                link = url_for("auth.confirm_email", token=token, _external=True)
                print(link)
                email_msg.body = f"please click on link for verification: {link}"

                mail.send(email_msg)

                return redirect(url_for("auth.login"))
                # new_user = User(
                #     name=name,
                #     email=email,
                #     userLevelId=3,
                #     password=generate_password_hash(password, method="sha256"),
                # )
                # try:
                #     db.session.add(new_user)
                #     db.session.add(LoginHistory(email=email, status="signup"))
                #     db.session.add(Employee(name=name))
                #     db.session.commit()
                #     flash("Account created", category="success")
                #     login_user(new_user, remember=True)
                #     return redirect(url_for("view.appointment_home"))
                # except Exception as e:
                #     flash("Account creation failed", category="error")
                #     print(e)

    return render_template(
        "auth/signup.jinja2", form=form, template="form-template", user=current_user
    )


@auth.route("/confirm_email/<token>")
def confirm_email(token):
    s = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"))
    try:
        email = s.loads(token, salt="email-confirm", max_age=30)
        return redirect(url_for("auth.login"))
    except SignatureExpired:
        flash("The token has expired please recreate account", category="error")
        return redirect(url_for("auth.signup"))

from flask_mail import Message, Mail
from itsdangerous.exc import SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer
from website.forms import LoginForm, SignUpForm
from website.models import LoginHistory, User
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
from datetime import datetime, timedelta

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
            if user.verified == True:
                if check_password_hash(user.password, password):
                    flash(
                        f"Login Success! Welcome back {user.name}", category="success"
                    )
                    log.status = "login success"
                    log.userId = user.id
                    try:
                        db.session.add(log)
                        db.session.commit()
                        login_user(user, remember=True)
                        return redirect(url_for("view.appointment_home"))
                    except Exception as e:
                        print(e)
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
    # clean up all expired users
    config_expire_time = int(current_app.config.get("ACCOUNT_EXPIRE_VERIFY_TIME"))
    expired_time = datetime.now() - timedelta(0, config_expire_time)
    expired_accounts = User.query.filter(
        User.creationDate <= expired_time, User.verified == False
    ).all()
    try:
        for account in expired_accounts:
            db.session.delete(account)
        db.session.commit()
    except Exception as e:
        print(f"error on deleting expired accounts: {e}")

    if request.method == "POST":
        if form.validate_on_submit():
            email = request.form["email"]
            name = request.form["name"]
            password = request.form["password"]
            user_exists = User.query.filter_by(email=email).first()
            if user_exists:
                flash("Email already exists!", category="error")
            else:
                mail = Mail(current_app)
                s = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"))
                token = s.dumps(email, salt="email-confirm")
                email_msg = Message(
                    "Confirm sign up request for appointment webapp",
                    sender=current_app.config.get("MAIL_USERNAME"),
                    recipients=[current_app.config.get("MAIL_USERNAME")],
                )

                link = url_for("auth.confirm_email", token=token, _external=True)
                email_msg.body = f"{name}, email: {email} is trying to create an account, please click on link for verification: \n{link}"

                mail.send(email_msg)

                new_user = User(
                    name=name,
                    email=email,
                    userLevelId=3,
                    password=generate_password_hash(password, method="sha256"),
                )
                try:
                    db.session.add(new_user)
                    db.session.add(LoginHistory(email=email, status="signup"))
                    db.session.commit()
                    expire_time = (
                        int(current_app.config.get("ACCOUNT_EXPIRE_VERIFY_TIME")) / 60
                    )
                    flash(
                        f"Account Pending Verification, token will expire in {expire_time} minute(s)",
                        category="success",
                    )
                    return render_template(
                        "auth/login.jinja2", form=form, user=current_user
                    )
                except Exception as e:
                    flash("Account creation failed", category="error")
                    print(e)
        return render_template("auth/signup.jinja2", form=form, user=current_user)
    else:  # request.method == "GET"
        unverified_users = User.query.filter_by(verified=False).all()
        if len(unverified_users) > 3:
            flash("Too many unverified accounts pending, contact admin")
            return redirect(url_for("auth.login"))
        return render_template("auth/signup.jinja2", form=form, user=current_user)


@auth.route("/confirm_email/<token>")
def confirm_email(token):
    s = URLSafeTimedSerializer(current_app.config.get("SECRET_KEY"))
    config_expire_time = int(current_app.config.get("ACCOUNT_EXPIRE_VERIFY_TIME"))
    try:
        email = s.loads(token, salt="email-confirm", max_age=config_expire_time)
        user = User.query.filter_by(email=email).first()
        if user:
            user.verified = True
            db.session.commit()
            flash("Account created, you can login now", category="success")
    except SignatureExpired:
        flash("The token has expired please recreate account", category="error")
        return redirect(url_for("auth.signup"))
    except Exception as e:
        flash("Account creation failed", category="error")
        print(e)
    return redirect(url_for("auth.login"))

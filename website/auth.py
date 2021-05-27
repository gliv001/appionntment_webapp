from flask import Blueprint, render_template, redirect, request
from flask.helpers import flash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    return redirect("/auth/login.html")


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        passwd = request.form["password"]
        passwd2 = request.form["password2"]

        if email.find("@") <= 0 or email.find(".") <= 0 or len(email) <= 4:
            flash("Incorrect Email", category="error")
        elif len(name) < 2:
            flash("Name must be greater than 1", category="error")
        elif passwd != passwd2:
            flash("Passwords do not match", category="error")
        elif len(passwd) <= 6:
            flash("Password must be greater than 6", category="error")
        else:
            flash("Account created", category="success")

    return render_template("auth/signup.html")

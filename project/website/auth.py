from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Username and password do not match!", category="error")
        else:
            flash("User with this username does not exist!", category="error")
    return render_template("login.html")

@auth.route("/register", methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("re-password")
        
        if len(email) < 4:
            flash("Email must be greater than 4 charecters!", category="error")
        elif len(username) <= 2:
            flash("Username must be greater than 2 charecters!", category="error")
        elif len(password) <= 7:
            flash("Password must be greater than 7 charecters!", category="error")
        elif password != repassword:
            flash("Passwords do not match!", category="error")
        elif User.query.filter_by(email=email).first():
            flash("User with this email already exist!", category="error")
        elif User.query.filter_by(username=username).first():
            flash("User with this username already exist!", category="error")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

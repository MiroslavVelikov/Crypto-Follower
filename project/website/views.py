from . import db
from .models import User
from .ScrapingInfo import MarketInfo, SliderInfo, CurrencyDetails
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, request, render_template, redirect, url_for

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
def home():
    type = CheckRequest()
    if type == "Login":
        Login()
    elif type == "Register":
        Register()

    market = []
    slider = []
    MarketInfo(market)
    SliderInfo(slider)
    return render_template("index.html", market=market, slider=slider)

@views.route("/details/<name>", methods=['GET', 'POST'])
def details(name):
    details = {}
    slider = []
    CurrencyDetails(name, details)
    SliderInfo(slider)
    return render_template("details.html", details=details, slider=slider)

def Login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            print("Logged in")
        else:
            print("Invalid email or password")
def Register():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    repassword = request.form.get("re-password")
    
    if len(email) < 4:
        pass
    elif len(username) < 2:
        pass
    elif len(password) < 7:
        pass
    elif password != repassword:
        pass
    else:
        pass

    new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))
    db.session.add(new_user)
    db.session.commit()
    print("Registered succesfully")

    return redirect(url_for("views.home"))
def CheckRequest():
    return request.form.get("request")

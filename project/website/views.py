from .models import User
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from .ScrapingInfo import MarketInfo, SliderInfo, CurrencyDetails

views = Blueprint('views', __name__)

@views.route("/")
@login_required
def home():
    market = []
    slider = []
    MarketInfo(market)
    SliderInfo(slider)
    return render_template("index.html", user=current_user, market=market, slider=slider)

@views.route("/details/<name>")
@login_required
def details(name):
    details = {}
    slider = []
    name = name.replace(" ", "-")
    CurrencyDetails(name, details)
    SliderInfo(slider)
    return render_template("details.html", user=current_user, details=details, slider=slider)

@views.route("/add-to-favorite")
@login_required
def favorite():
    # TODO 
    # Add currency to User currencies
    return redirect(url_for("views.home"))
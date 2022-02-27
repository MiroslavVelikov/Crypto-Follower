from . import db
from flask_login import login_required, logout_user, current_user
from .ScrapingInfo import MarketInfo, SliderInfo, CurrencyDetails
from flask import Blueprint, request, render_template, redirect, url_for, flash

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
    CurrencyDetails(name, details)
    SliderInfo(slider)
    return render_template("details.html", details=details, slider=slider)
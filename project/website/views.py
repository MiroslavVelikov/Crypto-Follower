from .models import Currency
from . import db
from flask import Blueprint, redirect, render_template, request
from flask_login import login_required, current_user
from .ScrapingInfo import MarketInfo, SliderInfo, CurrencyDetails

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        currency_name = request.form.get("name")
        currency = Currency.query.filter_by(name=currency_name).first()

        if not currency:
            new_currency = Currency(name=currency_name, user_id=current_user.id)
            db.session.add(new_currency)
        else: 
            db.session.delete(currency)

        db.session.commit()

    market = []
    slider = []
    MarketInfo(market)
    SliderInfo(slider)
    return render_template("index.html", user=current_user, market=market, slider=slider)

@views.route("/details/<name>", methods=['GET', 'POST'])
@login_required
def details(name):
    if request.method == "POST":
        currency_name = request.form.get("name")
        currency = Currency.query.filter_by(name=currency_name).first()

        if not currency:
            new_currency = Currency(name=currency_name, user_id=current_user.id)
            db.session.add(new_currency)
        else: 
            db.session.delete(currency)

        db.session.commit()
    details = {}
    slider = []
    name = name.replace(" ", "-")
    CurrencyDetails(name, details)
    SliderInfo(slider)
    if not details:
        details["name"] = "Invalid Currency"
        details["price"] = "-------"
        details["change"] = "-------"
        details["color_of_change"] = "-------"
        details["low"] = "-------"
        details["high"] = "-------"
        details["market_cap"] = "-------"
        details["volume"] = "-------"
        details["text"] = "-------"
    return render_template("details.html", user=current_user, details=details, slider=slider)
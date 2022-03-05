from .models import FollowedCurrency, MarketCurrency, SliderCurrency
from . import db
from flask import Blueprint, redirect, render_template, request
from flask_login import login_required, current_user
from .ScrapingInfo import MarketInfo, SliderInfo, CurrencyDetails
from datetime import datetime, timedelta  

views = Blueprint('views', __name__)
last_change = {"last_change":datetime.now()}

@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        currency_name = request.form.get("name")
        currency = FollowedCurrency.query.filter_by(name=currency_name).first()

        if not currency:
            new_currency = FollowedCurrency(name=currency_name, user_id=current_user.id)
            db.session.add(new_currency)
        else: 
            db.session.delete(currency)

        db.session.commit()
    CheckForNewChange(last_change)
    market = MarketCurrency.query.all()
    slider = SliderCurrency.query.all()
    return render_template("index.html", user=current_user, market=market, slider=slider)

@views.route("/details/<name>", methods=['GET', 'POST'])
@login_required
def details(name):
    if request.method == "POST":
        currency_name = request.form.get("name")
        currency = FollowedCurrency.query.filter_by(name=currency_name).first()

        if not currency:
            if currency_name != "Invalid Currency":
                new_currency = FollowedCurrency(name=currency_name, user_id=current_user.id)
                db.session.add(new_currency)
        else: 
            db.session.delete(currency)

        db.session.commit()
    details = {}
    slider = []
    name = name.replace(" ", "-")
    CurrencyDetails(name, details)
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
    CheckForNewChange()
    return render_template("details.html", user=current_user, details=details, slider=slider)

def CheckForNewChange(last_change):
    if MarketCurrency.query.all() == []:
        First_Load()
    now = datetime.now().strftime('%H:%M:%S')
    updated = ( last_change["last_change"] +
           timedelta( minutes=1 )).strftime('%H:%M:%S')
    if now > updated:
        last_change["last_change"] = datetime.now()
        print("Changed", last_change["last_change"])
    else:
        print("Now", now)
        print("Not updated yet", updated)
    
def First_Load():
    market = []
    slider = []
    MarketInfo(market)
    SliderInfo(slider)

    for currency in market:
        new_currency = MarketCurrency(name=currency["name"], price=currency["price"], change24h=currency["change24h"],
            color24h=currency["color24h"], change7d=currency["change7d"], color7d=currency["color7d"])
        db.session.add(new_currency)
    for currency in slider:
        new_currency = SliderCurrency(name=currency["name"], price=currency["price"], change=currency["change"], color=currency["color"])
        db.session.add(new_currency)

    db.session.commit()
    print(MarketCurrency.query.all())
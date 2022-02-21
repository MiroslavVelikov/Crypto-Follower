from flask import Flask, request, render_template
import ScrapingInfo

app = Flask(__name__)

@app.route("/")
def index():
    market = []
    slider = []
    ScrapingInfo.MarketInfo(market)
    ScrapingInfo.SliderInfo(slider)
    return render_template("index.html", market=market, slider=slider)

@app.route("/details/<name>")
def details(name):
    details = {}
    slider = []
    ScrapingInfo.CurrencyDetails(name, details)
    ScrapingInfo.SliderInfo(slider)
    return render_template("details.html", details=details, slider=slider)

if __name__ == "__main__":
    app.run(debug=True)
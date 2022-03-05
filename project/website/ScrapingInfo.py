import re
import requests
from bs4 import BeautifulSoup

def MarketInfo(currencies):
    url = "https://coinmarketcap.com/"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")

    tbody = doc.tbody
    trs = tbody.contents

    for tr in trs[:10]:
        rank, name, price, change24h, change7d = tr.contents[1:6]
        fixed_rank = rank.p.string
        fixed_name = name.p.string
        fixed_price = price.a.string
        fixed_change24h = change24h.span.find(text=re.compile("[0-9]+\.[0-9]+"))
        fixed_change7d = change7d.span.find(text=re.compile("[0-9]+\.[0-9]+"))
        fixed_color24h = re.findall("[a-z]+", str(change24h))[-4]
        fixed_color7d = re.findall("[a-z]+", str(change7d))[-4]
    
        currency = {
            "rank": fixed_rank,
            "name": fixed_name,
            "price": fixed_price,
            "change24h": fixed_change24h,
            "color24h": fixed_color24h,
            "change7d": fixed_change7d,
            "color7d": fixed_color7d
            }
            
        currencies.append(currency)

def GetText(name, info):
    url = f"https://www.coindesk.com/price/{ name }/"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")

    content = doc.find("div", class_="cQofyD")
    if content:
        start = 0
        end = 0
        count = 0
        for p in content:
            if end != 0:
                break
            elif "jFqdBZ" in str(p):
                if start == 0:
                    start = count + 1
                else:
                    end = count
            count += 1
        for p in content.contents[start:end]:
            info.append(p.text)

def CurrencyDetails(name, details):
    url = f"https://coinmarketcap.com/currencies/{ name }/"
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")

    price_section = doc.find("div", class_="priceSection")
    if price_section != "Invalid currency" and price_section != None:
        fixed_name = price_section.h1.text.rsplit(' ', 2)[0]
        fixed_price = price_section.find("div", class_="priceTitle").div.span.text
        fixed_change = price_section.find("div", class_="priceTitle").find_all("span")[1].text
        up_down_change = str(price_section.find("div", class_="priceTitle").find_all("span")[2])
        fixed_color = re.findall("[a-z]+", up_down_change)[-2]
        low_high = price_section.find_all("span", class_="dBJPYV")
        fixed_low = low_high[0].text
        fixed_high = low_high[1].text

        stat_values = doc.find_all("div", class_="statsValue")
        fixed_market_cap = stat_values[0].text
        fixed_volume = stat_values[2].text

        details["name"] = fixed_name
        details["price"] = fixed_price
        details["change"] = fixed_change
        details["color_of_change"] = fixed_color
        details["low"] = fixed_low
        details["high"] = fixed_high
        details["market_cap"] = fixed_market_cap
        details["volume"] = fixed_volume
        info = []
        GetText(name, info)
        if not info:
            info.append("Unfortunately the necessary data for this indicator is not available at the moment.")
        details["text"] = info

def SliderInfo(currencies, doc = ""):
    if not doc:
        url = "https://www.coindesk.com/"
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")
    
    curs = doc.find("div", class_="ioDFHO")
    for div in curs.contents:
        fixed_info = div.find_all("span", class_="dHSCiD")
        currency = {
            "name": fixed_info[0].text,
            "price": fixed_info[1].text,
            "change": fixed_info[2].text
        }
        if "-" in currency["change"]:
            currency["color"] = "down"
        else:
            currency["color"] = "up"
        currencies.append(currency)
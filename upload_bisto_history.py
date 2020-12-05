from datetime import datetime
import pandas as pd
import requests 
import json

df = pd.read_csv("btc-mxn.csv")

url = "http://127.0.0.1:8000/coinz/api/"


for row in df.iterrows():
    date = row[1]["date"]
    date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
    high = row[1]["high"].replace(".", "").replace(",", ".")
    low = row[1]["low"].replace(".", "").replace(",", ".")
    volume = row[1]["volume"]

    data = json.dumps({
        "book": "btc_mxn",
        "created_at": date,
        "high": high,
        "volume": volume,
        "low": low,
        "last": None,
        "vwap": None,
        "ask": None,
        "bid": None
    })

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(
        url,
        headers=headers,
        data=data
    )
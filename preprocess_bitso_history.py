from datetime import datetime
import pandas as pd
import requests
import json


df = pd.read_csv("Bitso_BTCMXN_1h.csv")
df.drop(columns=["Volume MXN"], inplace=True)


base_url = "http://127.0.0.1:8000/coinz/api/"

for row in df.iterrows():
    
    date = datetime.fromtimestamp(row[1]["Unix Timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

    data = json.dumps({
        "book": "btc_mxn",
        "volume": row[1]["Volume BTC"],
        "high": row[1]["High"],
        "low": row[1]["Low"],
        "created_at": date,
        "last": None,
        "vwap": None,
        "ask": None,
        "bid": None
    })

    headers = {
        "Content-Type": "application/json"
    }

    r = requests.post(
        base_url,
        headers=headers,
        data=data
    )
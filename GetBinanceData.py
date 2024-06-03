from binance import Client
from binance.enums import *
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime

# draw support and resistance line using 1hr time frame and and total of one month data, and end time is now
def get_historical_klines(symbol, interval, start_str, end_str=None):

    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}"
    if start_str:
        url += f"&startTime={int(pd.Timestamp(start_str).timestamp()*1000)}"
    if end_str:
        url += f"&endTime={int(pd.Timestamp(end_str).timestamp()*1000)}"
    data = json.loads(requests.get(url).text)
    
    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']).astype(float)

    # Clean up data
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    df = df[['Open time','Open', 'High', 'Low', 'Close', 'Volume']]

    return df 

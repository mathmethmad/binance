import pandas as pd
import numpy as np
from sklearn.neighbors import KernelDensity
from scipy.signal import find_peaks

def pivotid(df1, l, n1, n2): #n1 n2 before and after candle l
    if l-n1 < 0 or l+n2 >= len(df1):
        return 0
    
    pividlow=1
    pividhigh=1
    for i in range(l-n1, l+n2+1):
        if(df1.Low[l]>df1.Low[i]):
            pividlow=0
        if(df1.High[l]<df1.High[i]):
            pividhigh=0
    if pividlow and pividhigh:
        return 3
    elif pividlow:
        return 1
    elif pividhigh:
        return 2
    else:
        return 0

def mark_pivot_points(df):
    pivot_points_high = df[df["Pivot"] == 2]
    pivot_points_low = df[df["Pivot"] == 1]
    return pivot_points_high.index,pivot_points_low.index, pivot_points_high['High'], pivot_points_low['Low']

def support_and_resistance(data,bandwidthlength,hyperparameter_increase_interval):
    indicator  = True
    high_turning_points_prices = data[data['Pivot'] == 2]["High"].to_numpy().reshape(-1, 1)
    low_turning_points_prices = data[data['Pivot'] == 1]["Low"].to_numpy().reshape(-1, 1)
    turning_points_prices = np.concatenate([high_turning_points_prices, low_turning_points_prices]).reshape(-1, 1)
    log_turning_points_prices = np.log(turning_points_prices)
    current_price = data['Close'].iloc[-1]

    while indicator:
        kde = KernelDensity(kernel='gaussian', bandwidth=bandwidthlength).fit(log_turning_points_prices)
        low_interval,high_interval = min(log_turning_points_prices),max(log_turning_points_prices)
        price_ranges = np.linspace(low_interval, high_interval, 1000).reshape(-1, 1)
        pdf_turning_points = np.exp(kde.score_samples(price_ranges))
        peaks = find_peaks(pdf_turning_points)[0]
        support_and_resistance_levels = np.exp(price_ranges[peaks])
        
         # Sort peaks by their probabilities
        sorted_peaks = sorted(zip(support_and_resistance_levels, pdf_turning_points[peaks]), key=lambda x: x[1], reverse=True)

        # Get the top two peaks above and below the current price
        above = [peak[0] for peak in sorted_peaks if peak[0] > current_price][:2]
        below = [peak[0] for peak in sorted_peaks if peak[0] < current_price][:2]

        if len(above) >= 2 and len(below) >= 2:
            indicator = False
        else:
            bandwidthlength += hyperparameter_increase_interval
            if bandwidthlength > 100*hyperparameter_increase_interval:
                print("failed to find such criteria for support and resistance levels")
                break
        return above,below

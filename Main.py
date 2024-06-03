import pandas as pd
import numpy as np
import plotly.graph_objects as go
import GetBinanceData as gbd
import KernalSupportAndResistance as kdsr
from neuralprophet import NeuralProphet

#get data of pairs
end_time = pd.Timestamp.now()
start_time = end_time - pd.DateOffset(weeks=2) 
coin_df = gbd.get_historical_klines("BTCUSDT", "1h", start_time, end_time)

#get support and resistance
coin_df["Pivot"] = coin_df.apply(lambda x: kdsr.pivotid(coin_df,x.name,5,5),axis = 1)
resistance_above_current_prices, support_below_current_prices = kdsr.support_and_resistance(coin_df,0.001,0.001)

#identify the trend






#plot graphs
fig = go.Figure(data= [go.Candlestick(x = coin_df.index,
                       open = coin_df["Open"],
                       close = coin_df["Close"],
                       high = coin_df["High"],
                       low = coin_df["Low"])])
pivot_high_times,pivot_low_times, pivot_highs, pivot_lows = kdsr.mark_pivot_points(coin_df)

fig.add_traces(go.Scatter(x = pivot_high_times,y = pivot_highs, mode= "markers",name="PivotHigh",marker = dict(color = "Green")))
fig.add_traces(go.Scatter(x = pivot_low_times, y = pivot_lows,mode = "markers",name= "PivotLowTimes",marker = dict(color = "Red")))
resistance_and_support_levels = np.concatenate((resistance_above_current_prices,support_below_current_prices)).flatten()
for level in resistance_and_support_levels:
    fig.add_traces(go.Scatter(x = [coin_df.index.min(),coin_df.index.max()],y=[level,level],mode="lines",name="SupportAndResistance",
                              marker = dict(color = "blue")))

fig.show()
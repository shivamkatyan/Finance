# Import dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
yf.pdr_override()

# input
symbol = "AAPL"
start = dt.date.today() - dt.timedelta(days=365 * 2)
end = dt.date.today()

# Read data
df = yf.download(symbol, start, end)

df["sd"] = df["Adj Close"].rolling(5).std()
df["asd"] = df["sd"].rolling(10).mean()
df["DMI"] = 14 / (df["sd"] / df["asd"])
df = df.drop(["sd", "asd"], axis=1)

fig = plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df["Adj Close"])
ax1.set_title("Stock " + symbol + " Closing Price")
ax1.set_ylabel("Price")

ax2 = plt.subplot(2, 1, 2)
ax2.plot(df["DMI"], label="Dynamic Momentum Index")
ax2.grid()
ax2.legend(loc="best")
ax2.set_ylabel("Dynamic Momentum Index")
ax2.set_xlabel("Date")
plt.show()

# ## Candlestick with Dynamic Momentum Index
from matplotlib import dates as mdates

dfc = df.copy()
dfc["VolumePositive"] = dfc["Open"] < dfc["Adj Close"]
# dfc = dfc.dropna()
dfc = dfc.reset_index()
dfc["Date"] = mdates.date2num(dfc["Date"].tolist())
from mplfinance.original_flavor import candlestick_ohlc

fig = plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 1, 1)
candlestick_ohlc(ax1, dfc.values, width=0.5, colorup="g", colordown="r", alpha=1.0)
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
ax1.grid(True, which="both")
ax1.minorticks_on()
ax1v = ax1.twinx()
colors = dfc.VolumePositive.map({True: "g", False: "r"})
ax1v.bar(dfc.Date, dfc["Volume"], color=colors, alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3 * df.Volume.max())
ax1.set_title("Stock " + symbol + " Closing Price")
ax1.set_ylabel("Price")

ax2 = plt.subplot(2, 1, 2)
ax2.plot(df["DMI"], label="Dynamic Momentum Index")
ax2.grid()
ax2.legend(loc="best")
ax2.set_ylabel("Dynamic Momentum Index")
ax2.set_xlabel("Date")
plt.show()
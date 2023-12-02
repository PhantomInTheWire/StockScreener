import numpy as np
import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from alpha_vantage.fundamentaldata import FundamentalData

st.title("Stock Screener")
st.caption("By ~Karan Lokchandani")

today = datetime.datetime(2023, 5, 17)
lastyr = datetime.datetime(2022, 5, 17)

ticker = st.sidebar.text_input("Ticker", "MSFT")
start_date = st.sidebar.date_input("Start Date", lastyr)
end_date = st.sidebar.date_input("End Date", today)

data = yf.download(ticker, start=start_date, end=end_date)

fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
st.plotly_chart(fig)

pricing_data, fundamentals_data, news_data = st.tabs(['Pricing', "Fundamentals", "News"])

with pricing_data:
    st.header('Price Movement')
    data2 = data
    data2['% change'] = data['Adj Close'] / data['Adj Close'].shift(1) -1
    data2.dropna(inplace=True)
    st.write(data2)
with fundamentals_data:
    key = 'CVAHFSF4GAPVA90Q'
    fd = FundamentalData(key, output_format='pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)
with news_data:
    st.header('Top News')

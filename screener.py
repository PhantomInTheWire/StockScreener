import numpy as np
import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Stock Screener")
st.caption("By ~Karan Lokchandani")

ticker = "MSFT"
ticker = st.sidebar.text_input("Ticker")
start_date = "05072005"
end_date = "05012007"
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

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
    st.header('Fundamental Analysis')
with news_data:
    st.header('Top News')

import numpy as np
import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Stock Screener")
st.caption("By ~Karan Lokchandani")

ticker = st.sidebar.text_input("Ticker")
start_date = st.sidebar.date_input("Start Date")
end_date = st.sidebar.date_input("End Date")

data = yf.download(ticker, start=start_date, end=end_date)

fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
st.plotly_chart(fig)

pricing_data, fundamentals, news = st.tabs(['Pricing', "Fundamentals", "News"])



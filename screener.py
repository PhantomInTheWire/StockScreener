import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from stocknews import StockNews
from financetoolkit import Toolkit

st.title("Stock Screener")
st.caption("~By Karan Lokchandani and team")

today = datetime.date.today()
old = today - pd.DateOffset(years=3)

ticker = st.sidebar.text_input("Ticker", "AAPL")
s = st.sidebar.date_input("Start Date", old)
e = st.sidebar.date_input("End Date", today)

def get_data(t, start, end):
    return yf.download(t, start=start, end=end)

def load_data(ticker, start, end):
    data = get_data(ticker, start, end)
    data["SMA"] = data["Adj Close"].rolling(window=50).mean()
    return data

def get_news(ticker):
    return StockNews(ticker, save_news=True)

data = load_data(ticker, s, e)

fig = px.line(data, x=data.index, y=["Adj Close", "SMA"], title=ticker)
st.plotly_chart(fig)

pricing_data, fundamentals_data, news_data = st.tabs(["Pricing", "Fundamentals", "News"])

with pricing_data:
    st.header("Price Movement")
    data2 = data
    data2["% change"] = data["Adj Close"] / data["Adj Close"].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)

with fundamentals_data:
    st.header("Fundamentals")
    st.subheader("Balance Sheet")
    company = Toolkit(ticker, api_key="4477b5317cf6d0a5dd7259eac446d1cd", start_date=str(s), end_date=str(e))
    x = company.get_balance_sheet_statement();
    st.dataframe(x);

with news_data:
    st.header(f"Top News of {ticker}")
    sn = get_news(ticker)
    df_news = sn.read_rss()
    for i in range(5):
        st.subheader(f"News {i + 1}")
        st.write(df_news["published"][i])
        st.write(df_news["title"][i])
        st.write(df_news["summary"][i])

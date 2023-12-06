import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews

st.title("Stock Screener")
st.caption("By ~Karan and Shabbir")

today = datetime.datetime(2023, 5, 17)
lastyr = datetime.datetime(2022, 5, 17)

ticker = st.sidebar.text_input("Ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date", lastyr)
end_date = st.sidebar.date_input("End Date", today)


@st.cache_data
def get_data(t, start, end):
    return yf.download(t, start=start, end=end)


@st.cache_data
def load_data(ticker, start, end):
    data = get_data(ticker, start, end)
    data['SMA'] = data['Adj Close'].rolling(window=50).mean()
    return data


data = load_data(ticker, start_date, end_date)

fig = px.line(data, x=data.index, y=['Adj Close', 'SMA'], title=ticker)
st.plotly_chart(fig)

pricing_data, fundamentals_data, news_data = st.tabs(['Pricing', "Fundamentals", "News"])

with pricing_data:
    st.header('Price Movement')
    data2 = data
    data2['% change'] = data['Adj Close'] / data['Adj Close'].shift(1) - 1
    data2.dropna(inplace=True)
    st.write(data2)

with fundamentals_data:
    key = 'FBKRH19HGUCB6Z6D'
    fd = FundamentalData(key, output_format='pandas')
    st.subheader('Balance Sheet')
    balance_sheet = fd.get_balance_sheet_annual(ticker)[0]
    bs = balance_sheet.T[2:]
    bs.columns = list(balance_sheet.T.iloc[0])
    st.write(bs)

with news_data:
    st.header(f'Top News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i + 1}')
        st.write(df_news['published'][i])
        st.write(df_news['title'][i])
        st.write(df_news['summary'][i])
        t_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title Sentiment {t_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News Sentiment {news_sentiment}')

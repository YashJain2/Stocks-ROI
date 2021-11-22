import streamlit as st
import yfinance as yf
import pandas as pd


st.title('Compare ROI Of Stocks')

# creating a tuple
tickers = ('TSLA', 'AAPL', 'MSFT', 'BTC-USD', 'ETH-USD','TTM','RELIANCE.NS','TATAMOTORS.NS','SBIN.NS')

#dropdown lists of stocks
dropdown = st.multiselect('Choose your stocks', tickers)


start =st.date_input('Start',value=pd.to_datetime('2021-08-01'))
end=st.date_input('End', value =pd.to_datetime('2021-11-20'))

def relative_returns(df):
    rel=df.pct_change()
    # Calclating cummulative returns
    cumret = (1+rel).cumprod()-1
    cumret = cumret.fillna(0)
    return cumret




if len(dropdown)>0:
    # df=yf.download(dropdown,start,end)['Adj Close']
    df=relative_returns(yf.download(dropdown,start,end)['Adj Close'])
    st.header('Returns of {}'.format(dropdown))
    st.line_chart(df) 





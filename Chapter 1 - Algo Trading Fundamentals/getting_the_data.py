# loading the class data from the package pandas_datareader
from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd
import numpy as np


def get_ticker_data(start_date: str, end_date: str, symbols: list[str]):
    yf.pdr_override()
    goog_data = pdr.get_data_yahoo(symbols, start=start_date, end=end_date)
    print(goog_data)

    goog_data_signal = pd.DataFrame(index=goog_data.index)
    goog_data_signal['price'] = goog_data['Adj Close']
    goog_data_signal['daily_difference'] = goog_data_signal['price'].diff()
    goog_data_signal['signal'] = 0.0
    goog_data_signal['signal'] = np.where(
        goog_data_signal['daily_difference'] > 0, 1.0, 0.0)
    goog_data_signal['positions'] = goog_data_signal['signal'].diff()
    print(goog_data_signal.head())

    return simple_backtester(goog_data_signal)


def simple_backtester(signal):
    initial_capital = float(1000.0)
    positions = pd.DataFrame(index=signal.index).fillna(0.0)
    portfolio = pd.DataFrame(index=signal.index).fillna(0.0)
    positions['GOOG'] = signal['signal']
    portfolio['positions'] = (positions.multiply(signal['price'], axis=0))
    portfolio['cash'] = initial_capital - \
        (positions.diff().multiply(signal['price'], axis=0)).cumsum()

    return portfolio.head()


if __name__ == '__main__':
    start_date = '2014-01-01'
    end_date = '2018-01-01'
    y_symbols = ['GOOG']

    result = get_ticker_data(start_date, end_date, y_symbols)
    print(result)

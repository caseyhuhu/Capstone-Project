import pandas as pd
import datetime as dt
import numpy as np
from time import sleep
from alpha_vantage.timeseries import TimeSeries
import sys

def get_stock_data(symbol, startyear=2008, startmonth=1, endyear=2019, endmonth=10):
    
    """
    Obtains the stock data of the company identified by its stock symbol within the the given timeframe.
    Uses the AlphaVantage API: https://www.alphavantage.co/
    
    """
    
    key = 'BWT9OO9T59N87MUI'
    ts = TimeSeries(key)
    sleep(13)
    try:
        adjusted_results, meta = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
    except:
        return 0
    
    data_rows = []
    
    for year in range(startyear, endyear + 1):
        if year == startyear and startmonth != 1:
            for month in range(startmonth, 13):
                if year == endyear and month == endmonth + 1:
                    break
                for day in range(1, 32):
                    try:
                        dt.datetime(year, month, day)
                        date = f'{year}-{month:02}-{day:02}'
                        data_rows.append([year, month, day, adjusted_results[date]['5. adjusted close']])
                    except Exception as e:
                        continue
        else: 
            for month in range(1, 13):
                if year == endyear and month == endmonth + 1:
                    break
                for day in range(1, 32):
                    try:
                        dt.datetime(year, month, day)
                        date = f'{year}-{month:02}-{day:02}'
                        data_rows.append([year, month, day, adjusted_results[date]['5. adjusted close']])
                    except Exception as e:
                        continue
                        
    return pd.DataFrame(data_rows, columns=['Year', 'Month', 'Day', 'Adjusted close price'])
	
def add_stock_data(symbol_list):
    
    """
    Uses get_stock_data to add the stock data from the given companies 
    (in the form of a list of stock symbols) to 'Stock data.csv'
    
    """
    
    company_count = 0
    for symbol in symbol_list:
        if symbol in combined_df.columns:
            continue
        else:
            new_df = get_stock_data(symbol)
            if new_df is 0:
                continue
            else:
                new_data = new_df['Adjusted close price'].tolist()
                combined_df[symbol] = new_data
        company_count += 1
        if company_count % 5 == 0:
            sleep(65) # We are limited to 5 calls to AlphaVantage per minute
    combined_df.to_csv('/Users/rajatahuja/Documents/EE364D/Capstone-Project/mlapp/src/Stock_data.csv')
	
arg = sys.argv[1]
combined_df = pd.read_csv('/Users/rajatahuja/Documents/EE364D/Capstone-Project/mlapp/src/Stock_data.csv', index_col=0)

# Is input given in the form of a CSV of EDGAR data or as a list of comma-separated symbols?
if arg.lower().endswith('.csv'):
    df = pd.read_csv(arg) # New DataFrame with the users' companies' data. Stock prices are the last columns
    if df.columns.tolist()[0] == 'Unnamed: 0':
        df = pd.read_csv(arg, index_col=0)
    symbol_list = []
    for col in df.columns:
        if 'Stock price' in col:
            symbol_list.append(col.replace('Stock price_',''))
else:
    symbol_list = arg.split(',')
    for i in range(len(symbol_list)):
        symbol_list[i] = symbol_list[i].strip()

add_stock_data(symbol_list)
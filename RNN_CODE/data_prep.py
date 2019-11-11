from pandas import read_csv
from datetime import datetime

#load data
def parse(x):
    return datetime.strptime(x,'%Y %m')

dataset = read_csv('Combined_data_adjusted_full.csv', parse_dates = [['Year', 'Quarter']], index_col=0, date_parser=parse)
dataset.index.name = 'time'
dataset.to_csv('data.csv')

#python rnn_build.py NUM_COMPANIES
#change verbosity in line94 to 0 to get rid of all the epochs printing
#comment out all print statements for web
#inv_yhat is the variable that holds the prediction

import sys
import matplotlib
from math import sqrt
from numpy import concatenate
from matplotlib import pyplot 
from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from datetime import datetime
import os
cwd = os.getcwd()

# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	df = DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

train_num = 34
#NUM_COMPANIES = int(sys.argv[1])
#print("Total Number of Companies : " , NUM_COMPANIES)

def parse(x):
    return datetime.strptime(x,'%Y %m')

# Load dataset
cwd = cwd+'/src/'
target_company = sys.argv[1] # The symbol of the company we want to predict for
dataset = read_csv(cwd+'Combined_data_user_input.csv', parse_dates = [['Year', 'Quarter']], index_col=0, date_parser=parse)
dataset.index.name = 'time'

# Remove all EDGAR data from other companies, and remove all stock data from companies not in the same cluster
clusters_file = open(cwd+'clusters.txt', 'r')
clusters = clusters_file.readlines()
other_companies_in_cluster = []
for clus in clusters:
    if target_company in clus:
        other_companies_in_cluster = clus.split()
        other_companies_in_cluster.remove(target_company)
        break
        
columns_to_drop = []
for col in dataset.columns:
    if not any(term in col for term in ['Year_Quarter', target_company] + other_companies_in_cluster):
        columns_to_drop.append(col)
    elif not any(term in col for term in ['Year_Quarter', 'Stock price', target_company]):
            columns_to_drop.append(col)

dataset.drop(columns_to_drop, axis=1, inplace=True)

#Reordering columns to have the stock price of the company that user specified to be the last colun
cols = list(dataset)
cols.insert(len(cols),cols.pop(cols.index('Stock price_'+target_company)))
dataset = dataset.ix[:,cols]
values = dataset.values

#getting company names
NUM_COMPANIES = 0
for col in cols:
    if 'Stock price' in col:
        NUM_COMPANIES = NUM_COMPANIES + 1

TOTAL_FEATURES = (NUM_COMPANIES + 11)        
#print("Total Number of Companies : " , NUM_COMPANIES)
#print("Total Number of Features : " , TOTAL_FEATURES)
company_names = dataset.columns.tolist()
company_names = company_names[-NUM_COMPANIES:]

#ensure all data is float
values = values.astype('float32')
#normalize features
scaler = MinMaxScaler(feature_range=(0,1))
scaled = scaler.fit_transform(values)
reframed = series_to_supervised(scaled,1,1)

#drop columns 
drop_col = 11 + NUM_COMPANIES
reframed.drop(reframed.columns[[drop_col, drop_col+1, drop_col+2, drop_col+3, drop_col+4, drop_col+5, drop_col+6, drop_col+7, drop_col+8, drop_col+9, drop_col+10]],axis=1, inplace=True)
i=1
while(i<NUM_COMPANIES):
    reframed.drop(reframed.columns[[drop_col]],axis=1, inplace=True)
    i = i+1

#split into train and test sets
values = reframed.values
train = values[:train_num, :]
test = values[train_num-1: , :]
#split into input and outputs
train_X, train_y = train[:, :-1], train[:,-1]
test_X, test_y = test[:,:-1], test[:,-1]
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
#print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

# design network
model = Sequential()
model.add(LSTM(12, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=1024, batch_size=12, validation_data=None, verbose=0, shuffle=False)
# plot history
#pyplot.plot(history.history['loss'], label='train')
#pyplot.plot(history.history['val_loss'], label='test')
#pyplot.legend()
#pyplot.show()

#make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
#invert scaling for prediction
inv_yhat = concatenate((test_X[:,:-1],yhat),axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,-1]
print(target_company,"stock price prediction: $" + str(inv_yhat[0]))
#print(company_names)

#Save Stock Price graph
stockDate = 2957
myBottom = 10
if target_company == 'AAPL':
	stockDate = 2830
if target_company == 'AMD':
	myBottom = 1
figTitle = target_company + " Stock Price Over Time"
allStockPrices = read_csv(cwd+'Stock_data.csv',index_col=0)
StockPrices = allStockPrices.filter(items=[target_company])
actual = StockPrices.iloc[stockDate,0]
StockPrices = StockPrices.head(stockDate)
# StockPrices = StockPrices.tail(365)
prediction = inv_yhat
#prediction = 31.27
fig = pyplot.figure(figsize=(20,10))
ax = fig.add_axes([0,0,1,1])
ax.set_title(figTitle)
pyplot.yscale('linear')
pyplot.plot(StockPrices.index.tolist(),StockPrices.get(target_company).tolist(),label='Actual Stock Price')
pyplot.plot(stockDate,prediction,'ro',markersize=7,label='Predicted Stock Price')
pyplot.ylim(bottom=myBottom)
lgd = ax.legend(loc="upper left",fontsize =23)
figName = cwd+"/public/predGraph.png"
fig.savefig(figName,bbox_inches="tight")

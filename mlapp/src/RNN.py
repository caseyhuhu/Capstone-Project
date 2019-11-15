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
import json

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

train_num = 33
#NUM_COMPANIES = int(sys.argv[1])
#print("Total Number of Companies : " , NUM_COMPANIES)

def parse(x):
    return datetime.strptime(x,'%Y %m')

# Load dataset
target_company = sys.argv[1] # The symbol of the company we want to predict for
dataset = pd.read_csv('/Users/rajatahuja/Documents/EE364D/Capstone-Project/mlapp/src/Combined_data_user_input.csv', parse_dates = [['Year', 'Quarter']], date_parser=parse)
dataset.index.name = 'time'

# Remove all EDGAR data from other companies, and remove all stock data from companies not in the same cluster
clusters_file = open('clusters.txt', 'r')
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

values = dataset.values
#getting company names
NUM_COMPANIES = len(dataset.columns.tolist())
NUM_COMPANIES = int(NUM_COMPANIES/12)
TOTAL_FEATURES = (NUM_COMPANIES * 12)
#print("Total Number of Companies : " , NUM_COMPANIES)
#print("Total Number of Features : " , TOTAL_FEATURES)
company_names = dataset.columns.tolist()
company_names = company_names[-NUM_COMPANIES:]


#ensure all data is float
values = values.astype('float32')
#normalize features
scaler = MinMaxScaler(feature_range=(0,1))
scaled = scaler.fit_transform(values)
#print (values[0,0])
#Building Each Models
#model_num = 0
reframed = series_to_supervised(scaled,1,1)
#while (model_num < NUM_COMPANIES):
#	print("Building Model #" , model_num+1)
#drop columns 
i=0
while (i<NUM_COMPANIES):
	reframed.drop(reframed.columns[[108,109,110,111,112,113,114,115,116,117,118]],axis=1, inplace=True)
	i = i+1
#print(reframed.head())	

#split into train and test sets
values = reframed.values
train = values[:train_num, :]
test = values[train_num: , :]
#split into input and outputs
train_X, train_y = train[:, :(-1*NUM_COMPANIES)], train[:,TOTAL_FEATURES:]
test_X, test_y = test[:, :(-1*NUM_COMPANIES)], test[:,TOTAL_FEATURES:]
# reshape input to be 3D [samples, timesteps, features]
train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
#print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

# design network
model = Sequential()
model.add(LSTM(256, return_sequences=True, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(LSTM(128, return_sequences=True))
model.add(LSTM(64, return_sequences=True))
model.add(LSTM(32, return_sequences=True))
model.add(LSTM(16, return_sequences=True))
model.add(LSTM(9))
model.add(Dense(NUM_COMPANIES))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=200, batch_size=16, validation_data=(test_X, test_y), verbose=0, shuffle=False)
# plot history
pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
# pyplot.show()

#make a prediction
yhat = model.predict(test_X)
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
#invert scaling for prediction
inv_yhat = concatenate((yhat, test_X[:,NUM_COMPANIES:]), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,0:NUM_COMPANIES]

# print(inv_yhat)
# print(company_names)

listInv = []
for i in range(9):
	listInv.append(str(inv_yhat[0][i]))
	company_names[i] = company_names[i].replace('Stock price_', '')

dictionary = dict(zip(company_names, listInv))
json_string = json.dumps(dictionary)

print(json_string)


print('reached')
# from pandas import read_csv
# from math import sqrt
# from datetime import datetime
# from sklearn.preprocessing import MinMaxScaler
# from pandas import DataFrame
# from pandas import concat
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.layers import LSTM
# from matplotlib import pyplot
# from numpy import concatenate
# from math import sqrt
# from sklearn.metrics import mean_squared_error
# #import tensorflowjs as tfjs

# #convert series to supervised learning
# def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
#     n_vars = 1 if type(data) is list else data.shape[1]
#     df = DataFrame(data)
#     cols, names=list(), list()
#     #input sequence(t-n,...t-1)
#     for i in range(n_in, 0, -1):
#         cols.append(df.shift(i))
#         names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]    
#     # forecast sequence (t, t+1, ... t+n)
#     for i in range(0, n_out):
#         cols.append(df.shift(-i))
#         if i==0:
#             names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
#         else :
#             names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
#     #put it all together
#     agg = concat(cols, axis=1)
#     agg.columns = names
#     #drop rows with NaN values
#     if dropnan:
#         agg.dropna(inplace=True)
#     return agg

# def parse(x):
#     return datetime.strptime(x, '%Y %m')

# dataset = read_csv('Sample1.csv', parse_dates = [['Year', 'Quarter']], index_col=0, date_parser = parse)

# dataset.columns = ['Net income', 'Depreciation & Amortization' , 'Cash generated by operating activities', 'Cash at end of period' , 'Revenue', 'Cost of revenue', 'Earnings per share', 'Current assets', 'Total assets', 'Current liabilities', 'Shareholders equity', 'Stock price']
# dataset.index.name = 'date'

# dataset.to_csv('testing_sample.csv')

# #Load dataset
# dataset = read_csv('testing_sample.csv',header=0, index_col=0)
# values = dataset.values
# values = values.astype('float32')
# #normalize
# scaler = MinMaxScaler(feature_range=(0,1))
# scaled = scaler.fit_transform(values)
# #frame as supervised learning
# reframed = series_to_supervised(scaled,1, 1)
# #drop columns we don't want to predict
# reframed.drop(reframed.columns[[12,13,14,15,16,17,18,19,20,21,22]],axis=1, inplace = True)
# #print(reframed.head())

# #split into train and test sets
# values = reframed.values
# n_train_quarters = 31
# train = values[:n_train_quarters, :]
# test = values[n_train_quarters:, :]
# #split into input and outputs
# train_X, train_y = train[:, :-1],train[:,-1]
# test_X, test_y = test[:, :-1],test[:,-1]
# #reshape input to be 3D [samples, quartersteps, feaures]
# train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
# test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
# #print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)

# # design network
# model = Sequential()
# model.add(LSTM(256,return_sequences=True, input_shape=(train_X.shape[1], train_X.shape[2])))
# model.add(LSTM(128,return_sequences=True))
# model.add(LSTM(64, return_sequences=True))
# model.add(LSTM(32, return_sequences=True))
# model.add(LSTM(16, return_sequences=True))
# model.add(LSTM(8, return_sequences=True))
# model.add(LSTM(4, return_sequences=True))
# model.add(LSTM(2))
# model.add(Dense(1))
# model.compile(loss='mean_squared_error', optimizer='adam')
# # fit network
# history = model.fit(train_X, train_y, epochs=1024, batch_size=16, validation_data=(test_X, test_y), verbose=1, shuffle=False)
# # plot history
# pyplot.plot(history.history['loss'], label='train')
# pyplot.plot(history.history['val_loss'], label='test')
# pyplot.legend()
# pyplot.show()

# # make a prediction
# yhat = model.predict(test_X)
# test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
# # invert scaling for forecast
# inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
# inv_yhat = scaler.inverse_transform(inv_yhat)
# inv_yhat = inv_yhat[:,0]
# # invert scaling for actual
# test_y = test_y.reshape((len(test_y), 1))
# inv_y = concatenate(( test_X[:, 1:],test_y), axis=1)
# inv_y = scaler.inverse_transform(inv_y)
# inv_y = inv_y[:,0]

# # calculate RMSE
# rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
# print('Test RMSE: %.3f' % rmse)
# model.save('kerasModel.h5')
# #tfjs.converters.save_keras_model(model, 'kerasModel.json')


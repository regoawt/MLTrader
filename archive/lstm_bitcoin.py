# multivariate multi-step stacked lstm example
from numpy import array
from numpy import hstack
import pandas as pd
import requests
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

baseUrl = 'https://api.coindesk.com/v1/bpi/historical/close.json'

startDate = '2019-01-01'
endDate = '2019-05-15'
currency = 'GBP'

newUrl = baseUrl+'?start='+startDate+'&end='+endDate+'&currency='+currency
#print(newUrl)

historicalPrices = requests.get(newUrl).json()
historicalPrices = pd.DataFrame(historicalPrices)
historicalPrices = historicalPrices.bpi
historicalPrices.dropna(axis = 0, inplace = True)
#print(historicalPrices.tail())
input = array(historicalPrices)
output = input[1:len(historicalPrices)]
input = input[0:len(historicalPrices)-1]
input = input.reshape(len(input),1)
output = output.reshape(len(output),1)

data = hstack((input,output))


# split a multivariate sequence into samples
def split_sequences(sequences, n_steps_in, n_steps_out):
	X, y = list(), list()
	for i in range(len(sequences)):
		# find the end of this pattern
		end_ix = i + n_steps_in
		out_end_ix = end_ix + n_steps_out-1
		# check if we are beyond the dataset
		if out_end_ix > len(sequences):
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequences[i:end_ix, :-1], sequences[end_ix-1:out_end_ix, -1]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)

# choose a number of time steps
n_steps_in, n_steps_out = 5, 1
# covert into input/output
X, y = split_sequences(data[0:len(data)-n_steps_in,:], n_steps_in, n_steps_out)
# the dataset knows the number of features, e.g. 2
n_features = X.shape[2]
# define model
model = Sequential()
model.add(LSTM(100, activation='relu', return_sequences=True, input_shape=(n_steps_in, n_features)))
model.add(LSTM(100, activation='relu'))
model.add(Dense(n_steps_out))
model.compile(optimizer='adam', loss='mse')
# fit model
model.fit(X, y, epochs=200, verbose=0)
# demonstrate prediction
x_input = data[len(data)-n_steps_in:len(data),0]
x_input = x_input.reshape((1, n_steps_in, n_features))
yhat = model.predict(x_input, verbose=0)
print(yhat)
print(data[len(data)-n_steps_in:len(data),1])

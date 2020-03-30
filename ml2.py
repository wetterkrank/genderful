from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import SimpleRNN
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import numpy

# Read data; the characters are already converted into indexes (like "abc" => 1,2,3)
# MYFILE = 'test1_numeric.csv'
# WORD_LENGTH = 18
# UNIQUE_CHARS = 22
MYFILE = 'train_set_numeric.csv'
WORD_LENGTH = 34
UNIQUE_CHARS = 40

dataset = numpy.genfromtxt(MYFILE, delimiter=',', dtype=str, comments=None, encoding='utf-8')
data, labels = dataset[0:, 0:WORD_LENGTH], dataset[0:, WORD_LENGTH]

data = data.astype(int)
labels = labels.astype(int)

# One-hot encode data and labels
# Now the data will have shape [lines_number, word_length, unique_chars]
one_hot_data = to_categorical(data, num_classes=UNIQUE_CHARS)
one_hot_labels = to_categorical(labels, num_classes=3)

# Print some debug info
print('\n')
print('Data dimensions: ', data.shape)
print('Labels dimensions: ', labels.shape)
print('One-hot data dimensions: ', one_hot_data.shape)
print('One-hot labels dimensions: ', one_hot_labels.shape)
# print(data)
# print(labels)
# print(one_hot_labels)
print('\n')

# v1, SimpleRNN; accuracy ~0.5
# model = Sequential()
# model.add(SimpleRNN(32, input_shape=(WORD_LENGTH, UNIQUE_CHARS)))
# model.add(Dense(3, activation='softmax'))
# model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])

# v2
# model = Sequential()
# model.add(Dense(512, input_shape=(WORD_LENGTH, UNIQUE_CHARS)))
# model.add(LSTM(128))
# model.add(Dense(3, activation='softmax'))
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])

# v3
model = Sequential()
model.add(Dense(256, input_shape=(WORD_LENGTH, UNIQUE_CHARS)))
model.add(Bidirectional(LSTM(128, return_sequences=True)))
model.add(Bidirectional(LSTM(32)))
model.add(Dense(3, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])

model.summary()

# Train the model, iterating on the data in batches
model.fit(one_hot_data, one_hot_labels, epochs=10, batch_size=10)

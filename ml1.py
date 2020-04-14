from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import numpy

# Preprocess data
myfile = './/data//ml1_train_set_words.csv'

dataset = numpy.genfromtxt(myfile, delimiter=',', usecols=(0,1), dtype=str, comments=None, encoding='utf-8')
data, labels = dataset[:, 0], dataset[:, 1]

# Workaround to avoid the ragged tensor (converting to a "square" array right-filled with 0s)
lines = len(data)
cols = len(max(data, key=len))
data = numpy.array(data)
data = data.view(numpy.uint32)
data = data.reshape(lines,cols)
labels = labels.astype(int)

# Convert labels to categorical one-hot encoding
one_hot_labels = to_categorical(labels, num_classes=3)

# Printing some debug info
print('\n')
print('Data size: ', lines, 'x', cols)
print('Labels size: ', len(labels))
print('\n')

# A single-input model with 3 classes (categorical classification):
model = Sequential()
model.add(Dense(32, activation='relu'))
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model, iterating on the data in batches
model.fit(data, one_hot_labels, epochs=50, batch_size=16)
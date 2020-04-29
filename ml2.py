from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras import load_model
import numpy
import preprocess as prep

# Read data; the characters are already converted into indexes (like "abc" => 1,2,3)
WORD_LENGTH = prep.WORD_LENGTH
UNIQUE_CHARS = prep.UNIQUE_CHARS
DATA_FILE = './/data//dataset_3percent_num.csv'
dataset = numpy.genfromtxt(DATA_FILE, delimiter=',', dtype=int, comments=None, encoding='utf-8')

# Split dataset into train and test; BTW, dataset entries must be randomly ordered
set_length = dataset.shape[0]
trainset_length = int(set_length * 0.8)

data, labels = dataset[0:trainset_length, 0:WORD_LENGTH], dataset[0:trainset_length, WORD_LENGTH]
testdata, testlabels = dataset[trainset_length:, 0:WORD_LENGTH], dataset[trainset_length:, WORD_LENGTH]

# One-hot encode data and labels
# Now the data will have shape [lines_number, word_length, unique_chars]
one_hot_data = to_categorical(data, num_classes=UNIQUE_CHARS)
one_hot_labels = to_categorical(labels, num_classes=3)

oh_testdata = to_categorical(testdata, num_classes=UNIQUE_CHARS)
oh_testlabels = to_categorical(testlabels, num_classes=3)

def train_model():
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

    # Model v3
    model = Sequential()
    model.add(Dense(256, input_shape=(WORD_LENGTH, UNIQUE_CHARS)))
    model.add(Bidirectional(LSTM(128, return_sequences=True)))
    model.add(Bidirectional(LSTM(32)))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
    #model.summary()

    # Create callbacks
    callbacks = [EarlyStopping(monitor='val_loss', patience=5),
                ModelCheckpoint('.//models//model.h5', save_best_only=True, 
                save_weights_only=False)]

    # Train the model, iterating on the data in batches
    model.fit(one_hot_data, one_hot_labels,
            epochs=10, batch_size=10, 
            callbacks=callbacks, 
            validation_data=(oh_testdata, oh_testlabels))

    # Test on the validation data set
    model.evaluate(oh_testdata, oh_testlabels)

    # Test on some common words; try user input?
    # This Numpy.Reshape part looks a bit sketchy...
    words = ["gabel", "löffel", "messer", "mädchen", "fahrrad", "nation", "ausbildung", "junge"]
    words_enc = prep.chars_to_indexes(words, prep.ALPHABET_DE, WORD_LENGTH)

    for encoded, original in zip(words_enc, words):
        w_seq = numpy.fromstring(encoded, sep=",")
        w_seq_oh = to_categorical(w_seq, num_classes=UNIQUE_CHARS)
        w_seq_oh = numpy.reshape(w_seq_oh, (1, WORD_LENGTH, UNIQUE_CHARS))
        gender = model.predict_classes(w_seq_oh)
        print(original, gender)

if __name__ == "__main__":
    train_model()
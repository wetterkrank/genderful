from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import load_model
import numpy
import sys
import preprocess as prep

WORD_LEN = prep.WORD_LENGTH
UNIQUE_CHARS = prep.UNIQUE_CHARS
DATA_FILE = './/data//dataset_3percent_num.csv'
MODEL_FILE = './/models//model.h5'


class OH_Dataset:
    """Four one-hot encoded Keras sets of training/testing data and labels"""

    def __init__(self, csv_file):
        # Load preprocessed dataset (characters converted into indexes (like "abc" => 1,2,3))
        num_set = numpy.genfromtxt(csv_file, delimiter=',', dtype=int, encoding='utf-8')

        # Split dataset into train and test; BTW, dataset entries must be randomly ordered
        set_len = num_set.shape[0]
        trainset_len = int(set_len * 0.8)
        data, labels = num_set[0:trainset_len, 0:WORD_LEN], num_set[0:trainset_len, WORD_LEN]
        testdata, testlabels = num_set[trainset_len:, 0:WORD_LEN], num_set[trainset_len:, WORD_LEN]

        # One-hot encode data and labels
        # Now the data will have shape [lines_number, word_length, unique_chars]
        self.oh_data = to_categorical(data, num_classes=UNIQUE_CHARS)
        self.oh_labels = to_categorical(labels, num_classes=3)
        self.oh_testdata = to_categorical(testdata, num_classes=UNIQUE_CHARS)
        self.oh_testlabels = to_categorical(testlabels, num_classes=3)

        # Some debug info
        # print('\n')
        # print('Data dimensions: ', data.shape)
        # print('Labels dimensions: ', labels.shape)
        # print('One-hot data dimensions: ', self.oh_data.shape)
        # print('One-hot labels dimensions: ', self.oh_labels.shape)
        # print('\n')

def train_model(dset):

    # Model v3
    model = Sequential()
    model.add(Dense(256, input_shape=(WORD_LEN, UNIQUE_CHARS)))
    model.add(Bidirectional(LSTM(128, return_sequences=True)))
    model.add(Bidirectional(LSTM(32)))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
    # model.summary()

    # Create callbacks for early stopping and saving the model
    callbacks = [EarlyStopping(monitor='val_loss', patience=5),
                 ModelCheckpoint(MODEL_FILE, save_best_only=True,
                                 save_weights_only=False)]

    # Train the model, iterating on the data in batches
    model.fit(dset.oh_data, dset.oh_labels,
              epochs=10, batch_size=10, 
              callbacks=callbacks, 
              validation_data=(dset.oh_testdata, dset.oh_testlabels))

    # Evaluate the model
    model.evaluate(dset.oh_testdata, dset.oh_testlabels)

    return model

def predict(model, word):

    # That Numpy.Reshape part looks a bit sketchy...
    word_encoded = prep.chars_to_indexes(word, prep.ALPHABET_DE, WORD_LEN)

    w_seq = numpy.fromstring(word_encoded, sep=",")
    w_seq_oh = to_categorical(w_seq, num_classes=UNIQUE_CHARS)
    w_seq_oh = numpy.reshape(w_seq_oh, (1, WORD_LEN, UNIQUE_CHARS))

    probs = model.predict(w_seq_oh, verbose=1)
    print(probs)
    gender = prep.GENDERS.get(model.predict_classes(w_seq_oh, verbose=1)[0])
    return gender


if __name__ == "__main__":
    try:
        mode = sys.argv[1]
    except IndexError:
        sys.exit(f"Usage: {sys.argv[0]} <--train|--use>")
    
    if mode == "--train":
        dataset = OH_Dataset(DATA_FILE)
        genders_model = train_model(dataset)
    elif mode == "--use":
        genders_model = load_model(MODEL_FILE)
        print("Enter a German word, empty line to exit:")
        while True:
            line = input('> ')
            if not line: 
                break
            print(predict(genders_model, line))
    else:
        sys.exit(f"Usage: {sys.argv[0]} <--train|--use>")

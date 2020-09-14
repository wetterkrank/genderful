import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 for max verbosity

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model
import numpy
import preprocess as prep

WORD_LEN = prep.WORD_LENGTH
UNIQUE_CHARS = prep.UNIQUE_CHARS
DATA_FILE = './/data//dataset_3percent_num.csv'
MODEL_FILE = './/models//model.h5'

class Predictor():
    def __init__(self):
        self.model = load_model(MODEL_FILE)
        
    def predict(self, word):

        # That Numpy.Reshape part still looks a bit sketchy...
        word_encoded = prep.chars_to_indexes(word, prep.ALPHABET_DE, WORD_LEN)

        w_seq = numpy.fromstring(word_encoded, sep=",")
        w_seq_oh = to_categorical(w_seq, num_classes=UNIQUE_CHARS)
        w_seq_oh = numpy.reshape(w_seq_oh, (1, WORD_LEN, UNIQUE_CHARS))

        probs = self.model.predict(w_seq_oh, verbose=1)
        gender = prep.GENDERS.get(numpy.argmax(probs))

        result = {'word': word, 'gender': gender, 'probability': numpy.max(probs)}
        return result


if __name__ == "__main__":
    genders_model = Predictor()

    print("Enter a German word, or empty line to exit:")
    while True:
        line = input('> ')
        if not line: 
            break
        print(genders_model.predict(line))

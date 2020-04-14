# Take a CSV file with 2 columns (word,label), example: abcba,0
# Lowercase the word and convert it into a comma-separated sequence of integers
# Right pad it with zeros to the longest word and print, followed by label: 1,2,3,2,1,0

import preprocess as prep
import sys

ALPHABET = prep.ALPHABET_DE
WORD_LENGTH = prep.WORD_LENGTH

try:
    input_file = sys.argv[1]
except IndexError:
    sys.exit(f"Usage: {sys.argv[0]} <input file> [output file]")
try:
    output_file = sys.argv[2]
except IndexError:
    output_file = ""

# read file, split into 2 columns, convert the data column to lower case
with open(input_file, "rt", encoding="utf-8") as f:
    rows = f.read().splitlines()
data, labels = map(list, zip(*(row.split(",") for row in rows)))
data = [line.lower() for line in data]

print("Max data length:", WORD_LENGTH)
print("Unique characters:", len(ALPHABET))
print("Dictionary:", ALPHABET)

# uniq_freqs = prep.char_freqs(data)
# print("Char frequencies:", uniq_freqs)

# sorted_by_freq = [k for k, v in sorted(uniq_freqs.items(), key=lambda item: item[1], reverse=True)]
# print("Chars sorted by frequency:", sorted_by_freq)

if output_file:
    # convert chars to integers and write to file
    data = prep.chars_to_indexes(data, ALPHABET, WORD_LENGTH)

    with open(output_file, mode="wt", encoding="utf-8") as f:
        for col1, col2 in zip(data, labels):
            f.write(col1+","+col2+"\n")

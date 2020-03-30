# Take a CSV file with 2 columns (word,number), example: abcba,0
# Lowercase the word and convert it into a comma-separated sequence of integers
# Right pad it with zeros to the longest word and print, followed by number: 1,2,3,2,1,0

import sys

try:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
except IndexError:
    sys.exit(f"Usage: {sys.argv[0]} <input file> <output file>")

uniques = list(chr(0))
max_len = 0
output = ""

# read file, convert to lower case and split into 2 columns
with open(input_file, "rt") as f:
    fcontents = [line.lower().split(",") for line in f.read().splitlines()]

# build characters dict
for (col1, col2) in fcontents:
    for ch in col1:
        if ch not in uniques:
            uniques.append(ch)
    if len(col1) > max_len:
        max_len = len(col1)
uniques.sort()
uniques_dict = {ch: uniques.index(ch) for ch in uniques}

print("max word length:", max_len)
print("unique characters:", len(uniques_dict))
print(uniques_dict)

# pad lines with zeros, convert chars and print the result
for (col1, col2) in fcontents:
    col1 = col1.ljust(max_len, chr(0))
    for ch in col1:
        output += str(uniques_dict[ch]) + ","
    output += col2 + "\n"

with open(output_file, "wt") as f:
    f.write(output)

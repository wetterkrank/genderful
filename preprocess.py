# Routines for converting strings into zero-padded numeric arrays

# zero index reserved for padding, last entry's index used to replace non-relevant characters
ALPHABET_DE = {k:i for i, k in enumerate("\x00abcdefghijklmnopqrstuvwxyzäöüß-\x1A")}
WORD_LENGTH = 40
UNIQUE_CHARS = 33
GENDERS = {0:"female", 1:"male", 2:"neutral"}

def pad_strings(lines, length):
    '''Returns a list of strings right-padded with chr(0) to length'''
    padded = list()
    for line in lines:
        # pads string with chr(0)
        padded.append(line.ljust(length, chr(0)))
    return padded

def unique_chars_dict(lines):
    '''Returns a dictionary of enumerated unique characters in a list of strings.'''
    unique_chars = list(set("".join(lines)))
    unique_chars.sort()
    out_dict = {char: unique_chars.index(char) for char in unique_chars}
    return out_dict

def char_freqs(lines):
    '''Returns the dict with character frequencies in a list of strings'''
    unique_chars = list(set("".join(lines)))
    unique_chars.sort()
    out_dict = {char: 0 for char in unique_chars}
    for line in lines:
        for char in line:
            out_dict[char] += 1
    return out_dict

def chars_to_indexes(smth, chars_dict, max_length):
    '''Replaces string characters by their numbers using chars_dict, result is comma-separated.'''
    if isinstance(smth, list):
        out_list = list()
        for line in smth:
            out_list.append(chars_to_indexes(line, chars_dict, max_length))
    if isinstance(smth, str):
        out_str = ""
        smth = smth[0:max_length]
        smth = smth.ljust(max_length, chr(0))
        for char in smth:
            # the index of last entry in the dict is used for non-matching chars
            out_str += str(chars_dict.get(char, len(chars_dict)-1)) + ","
        out_str = out_str.rstrip(",")
        return out_str
    return out_list


# TODO: Add unit tests
if __name__ == "__main__":
    pass

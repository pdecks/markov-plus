"""markov-chains_plus.py produces random text using text input from stdin or
from combination of text files.

Markov chains using n-grams can be specified with optional argument -n. Default is bigram (n=2)

If optional arguments -n and -f are provided, format as follows:
$ python markov-chains_plus.py -n # -f filename1.txt filename2.txt ... filenameN.txt

Else stdin can be piped to function as follows:
$ cat filename | python markov-chains_plus.py -n # 

"""
from random import choice
import argparse
import sys

# Allow for variation in input arguments
parser = argparse.ArgumentParser()
parser.add_argument("-n", type=int, help="specify length of n-gram")

parser.add_argument("-f", metavar='file.txt', default=None,
                    nargs='+', help="input text file names, separated by a space")
args = parser.parse_args()

n_gram = args.n if args.n else 2

# switch between stdin and input filenames
if args.f is None:
    input_paths = None
else:
    input_paths = args.f


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.
    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    contents = open(file_path).read()

    return contents


def make_chains(text_string, n):
    """Takes input text as string; returns dictionary of n-length markov chains.
    A chain will be a key that consists of a n-tuple of (word1, word2, ..., wordn)
    and the value would be a list of the word(s) that follow those n words in the
    input text.
    For example:
        >>> make_chains("hi there mary hi there juanita", 2)
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    words = text_string.split()

    word_key = words[:n]

    tuple_key = tuple(word_key)


    for i in range(len(words)-n):  # update range, probably n?
        # create empty list to hold n-length chain
        # iterate and append word to key list
        # to create next list: slice first item off list and append next_word
        if tuple_key in chains:
            chains[tuple_key].append(words[i+n])
        else:
            chains[tuple_key] = [words[i+n]]
        # take all of word_key except the first item
        word_key = word_key[1:]
        word_key.append(words[i+n])
        tuple_key = tuple(word_key)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    text = ""

    # select an n-gram key at random until one beginning with 
    # a capital letter is selected
    current_key = choice(chains.keys())

    while not current_key[0][0].isupper():
        current_key = choice(chains.keys())
    
    # convert immutable tuple to list for slicing 
    # list will be sliced and appended while marching through text
    temp_keys = list(current_key)

    # create the first piece of text from the key
    text = " ".join(current_key)

    # keep adding to the text until KeyError is produced
    # this occurs when the last tuple in the original text is selected
    # as current_key
    while True:
        try:
            # retrieve the word following the current key
            # and add it to the text string
            next_word = choice(chains[current_key])
            text += (" " + next_word)

            # update current_key tuple
            # a. update current_key list
            # b. convert current_key list to tuple
            temp_keys = temp_keys[1:]
            temp_keys.append(next_word)
            current_key = tuple(temp_keys)

        except KeyError:
            break
    return text


# Open the file(s) and turn it/them into one long string
input_text = ''
if input_paths is None:
    input_text = sys.stdin.read()
else:
    for input_path in input_paths:
        input_text += open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text, n_gram)

# Produce random text
random_text = make_text(chains)

print random_text

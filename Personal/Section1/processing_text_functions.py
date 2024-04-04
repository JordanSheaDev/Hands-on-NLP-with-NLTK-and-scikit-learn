'''Functions for processing text'''
import re

from collections import Counter


def improved_regex_splitting(line: str):
    '''Splits a string into individual words'''
    # Start with a letter, then a possible combination of letters
    # and apostrophes but that finish with a letter, or single letters
    improved_word_regex = r"(\w[\w']*\w|\w)"

    word_matcher = re.compile(improved_word_regex)

    return word_matcher.findall(line)


def process_and_split(line: str) -> list:
    '''Takes in a line preocesses and splits into words'''
    if len(line) == 1:
        return None
    # New lines used and single speach marks instead of apostrophes
    # Lower case also needed
    line = line.replace('\n', '').replace('’', "'").lower()
    return improved_regex_splitting(line)


def read_and_process(file_path: str,
                     split_lines: bool = False) -> list:
    '''
        Reads a file and returns a list of each word used in the file

        Params:
        file_path: A file path to a text file to process
        split_lines: If true each line will be returned as an individual list
    '''
    processed_corpus = []
    with open(file_path, encoding='UTF-8') as f:
        for line in f:
            line = process_and_split(line)
            if line:
                if split_lines:
                    processed_corpus.append(line)
                else:
                    processed_corpus.extend(line)
    return processed_corpus


def remove_uncommon_and_stop_words(
        corpus: list[str],
        uncommon_amount: float,
        stop_words: list[str],) -> list[str]:
    '''
        Removes uncommon words and stop words from a corpus

        Params:
        corpus: A list of strings to be processed
        uncommon_amount: If 1 or above will be a number of words to
            be removed. If below 1, then will be a proportion to be
            removed.
        stop_words: A list of common words without meaning to remove

        Returns a list of words from the corpus
    '''
    # Find least common elements
    word_counts = Counter(corpus)
    if uncommon_amount > 1:
        uncommon_words = word_counts.most_common()[:-(uncommon_amount+1):-1]
    else:
        removal_amount = int(uncommon_amount*len(corpus))
        uncommon_words = word_counts.most_common()[:-(removal_amount+1):-1]

    reduced_corpus = [w for w in corpus if w not in stop_words]
    return [w for w in reduced_corpus if w not in uncommon_words]

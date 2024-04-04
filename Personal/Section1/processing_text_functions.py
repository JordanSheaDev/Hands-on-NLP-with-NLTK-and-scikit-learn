'''Functions for processing text'''
import re


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

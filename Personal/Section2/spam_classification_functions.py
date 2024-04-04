'''Functions to use to train a spam classification model with nltk'''
import os
from collections import Counter
from random import shuffle
import nltk


class SpamLoader:
    '''
        Class to train a NTLK NaiveBayes Model on Spam filtering
        stop_words: A list of common words without meaning to remove
        uncommon_amount: If 1 or above will be a number of words to be removed.
            If below 1, then will be a proportion to be removed.
    '''
    def __init__(self,
                 stop_words: list[str] = None,
                 uncommon_amount: float = 0.1,) -> None:
        if stop_words:
            self.stop_words = stop_words
        else:
            self.stop_words = self.get_stopwords()
        self.uncommon_amount = uncommon_amount
        self.all_examples = None
        self.features = None

    def update(self):
        '''Check if updates are needed'''
        nltk.download('punkt')
        nltk.download('wordnet')
        nltk.download('stopwords')

    def get_stopwords(self):
        '''Returns english stopwords from nltk'''
        return set(nltk.corpus.stopwords.words('english'))

    def load_files(self, directory: str) -> list[str]:
        '''
            Given a directory path of some text files,
            will read in files and return them as a list
        '''
        result = []
        for fname in os.listdir(directory):
            # Some errors in decoding with utf-8,
            # so these were stripped from the data
            with open(directory + fname, 'r',
                      encoding='utf-8', errors='ignore') as f:
                result.append(f.read())
        return result

    def preprocess_sentence(self, sentence: str) -> list[str]:
        '''
            Processes a sentence to be used in NLP.

            Params:
            sentence: A string to be tokenised

            Returns a list of tokens
        '''
        # Check if stopwords have been given
        lemmatizer = nltk.WordNetLemmatizer()
        # Pre-processing pipeline
        processed_tokens = nltk.word_tokenize(sentence)
        processed_tokens = [w.lower() for w in processed_tokens]
        # Find least common elements and stopwords
        # Find least common elements
        word_counts = Counter(processed_tokens)
        if self.uncommon_amount > 1:
            uncommon_words = word_counts.most_common()[
                :-(self.uncommon_amount+1):-1]
        else:
            removal_amount = int(self.uncommon_amount*len(processed_tokens))
            uncommon_words = word_counts.most_common()[:-(removal_amount+1):-1]
        # Remove uncommon words and stop words
        processed_tokens = [
            t for t in processed_tokens if t not in uncommon_words]
        processed_tokens = [
            t for t in processed_tokens if t not in self.stop_words]
        # Lemmatize the words
        processed_tokens = [lemmatizer.lemmatize(t) for t in processed_tokens]
        return processed_tokens

    def load_and_process_files(self, spam_directory: str, ham_directory: str,
                               all_examples: list[str, int] = None,
                               ) -> tuple[list[str, int], list[str, int]]:
        '''
            Given a directory of spam and ham creates a list of features
            with a value of 1 for spam and 0 for ham
        '''
        if not self.all_examples:
            self.all_examples = []
        if all_examples:
            self.all_examples = self.all_examples.extend(all_examples)

        # Load ham and spam files
        spam_list = self.load_files(spam_directory)
        ham_list = self.load_files(ham_directory)

        # Process the examples
        spam_list = [self.preprocess_sentence(email) for email in spam_list]
        ham_list = [self.preprocess_sentence(email) for email in ham_list]

        # Label the examples
        spam_list = [(email, 1) for email in spam_list]
        ham_list = [(email, 0) for email in ham_list]

        # Join the eamples into a singular list and shuffle
        num_extracted = len(spam_list + ham_list)
        self.all_examples.extend(spam_list)
        self.all_examples.extend(ham_list)
        shuffle(self.all_examples)
        print(f'Successfully extracted {num_extracted} files')
        if len(self.all_examples) != num_extracted:
            print(f'There are now {len(self.all_examples)} files')
        return self.all_examples

    def feature_extraction(self) -> dict[tuple[str:int]:int]:
        '''
            Turn each word into a feature. The feature count is the word count.
        '''
        if not self.features:
            self.features = []
        self.features.extend(
            [(Counter(corpus), label) for corpus, label in self.all_examples])
        return self.features

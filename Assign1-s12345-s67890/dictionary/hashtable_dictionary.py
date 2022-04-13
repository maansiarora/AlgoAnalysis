from typing import List
from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED. Hash-table-based dictionary.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class HashTableDictionary(BaseDictionary):

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        self.dict={}
        for i in words_frequencies:
            self.dict.update({i.word:i.frequency})

        # TO BE IMPLEMENTED

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        # TO BE IMPLEMENTED
        # place holder for return
        for keys in self.dict.keys():
            if keys == word:             #strip if needed
                return self.dict[keys]

        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # TO BE IMPLEMENTED
        # place holder for return
        for i in self.dict.keys():
            if i!=word_frequency.word:
                self.dict[word_frequency.word]=word_frequency.frequency
                return True

        return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # TO BE IMPLEMENTED
        # place holder for return
        for keys in self.dict.keys():
            if keys == word:             #strip if needed
                self.dict.pop(keys)
                return True
        return False

    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        # TO BE IMPLEMENTED
        # place holder for return
        prefix_dict = {}  
        final_li = []  

        for i in self.dict.keys():
            if i.startswith(word):
                prefix_dict[i]=self.dict[i]
        
        prefix_dict = dict(sorted(prefix_dict.items(), key=lambda x: x[1], reverse=True))     
        #prefix_dict = prefix_dict[0:3]
        li = list(prefix_dict)[:3]

        final_li=[]
        for i in li:
            x = WordFrequency(i, prefix_dict[i])
            final_li.append(x)

        return final_li

from typing import List
from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED. List-based dictionary implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

class ListDictionary(BaseDictionary):

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        self.dict_list = []

        for i in words_frequencies:
            li = [i.word, i.frequency]
            self.dict_list.append(li)

        # TO BE IMPLEMENTED

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        # TO BE IMPLEMENTED
        
        for i in self.dict_list:
            if i[0] == word:             #strip if needed
                return i[1]

        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # TO BE IMPLEMENTED
        # place holder for return
        for i in self.dict_list:
            if i[0] == word_frequency.word:
                return False
            else:
                li = [word_frequency.word, word_frequency.frequency]
                self.dict_list.append(li)
                return True


    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # TO BE IMPLEMENTED
        # place holder for return
        for i in self.dict_list:
            if word in i:
                self.dict_list.remove(i)
                return True

        return False


    def autocomplete(self, prefix_word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'prefix_word' as a prefix
        @param prefix_word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'prefix_word'
        """
        # TO BE IMPLEMENTED
        # place holder for return
        
        prefix_li = []  
        final_li = []  

        for i in self.dict_list:
            if i[0].startswith(prefix_word):
                prefix_li.append(i)

        prefix_li = sorted(prefix_li, key=lambda x: x[1], reverse=True)     
        prefix_li = prefix_li[0:3]

        for j in prefix_li:
            x = WordFrequency(j[0], j[1])
            final_li.append(x)

        return final_li
from typing import List
from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency
from dictionary.node import Node


# ------------------------------------------------------------------------
# This class is required to be implemented. Ternary Search Tree implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------


class TernarySearchTreeDictionary(BaseDictionary):

    def build_dictionary(self, words_frequencies: List[WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        # TO BE IMPLEMENTED
        self.tst = Node() 
        for word_freq in words_frequencies:
            self.add_word_frequency(word_freq)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        # TO BE IMPLEMENTED
        # place holder for return
        current_node = self.tst 
        word_length = len(word)
        i = 0
        while i < word_length and current_node != None:
            letter = word[i] 
            if letter < current_node.letter:
                current_node = current_node.left
            elif letter == current_node.letter:
                i += 1
                if i < word_length:
                    current_node = current_node.middle
            else:
                current_node = current_node.right

        if i < word_length or current_node == None or current_node.end_word == False:
            return 0

        return current_node.frequency
        
    
    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # TO BE IMPLEMENTED
        current_node = self.tst
        word_length = len(word_frequency.word)
        char_pos = 0
        while char_pos < word_length:
            letter = word_frequency.word[char_pos] 
            if current_node.letter == None:
                current_node.letter = letter
            if letter < current_node.letter:
                if current_node.left == None:
                    current_node.left = Node()
                current_node = current_node.left
            elif letter == current_node.letter:
                if char_pos == word_length - 1:
                    break
                if current_node.middle == None:
                    current_node.middle = Node()
                current_node = current_node.middle
                char_pos += 1
            elif letter > current_node.letter:
                if current_node.right == None:
                    current_node.right = Node()
                current_node = current_node.right
        if current_node.end_word == False:
            current_node.end_word = True
            current_node.frequency = word_frequency.frequency
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
        if self.search(word) == 0:
            return False

        current_node = self.tst 
        node_li = []
        word_length = len(word) 
        i = 0
        while i < word_length and current_node != None:
            letter = word[i] 
            if letter < current_node.letter:
                current_node = current_node.left
            elif letter == current_node.letter:
                i += 1 
                node_li.append(current_node) 
                if i < word_length:
                    current_node = current_node.middle
            else:
                current_node = current_node.right

        node_li = node_li[::-1]

        for i in range(len(node_li)):
            node = node_li[i] 
            if i == 0:
                node.end_word = False
            if node.middle == None and node.left == None and node.right == None:
                node = None
        return True


    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        # TO BE IMPLEMENTED
        current_node = self.tst 
        word_length = len(word) 
        i = 0
        while i < word_length and current_node != None:
            letter = word[i]
            if letter < current_node.letter:
                current_node = current_node.left
            elif letter == current_node.letter:
                i += 1 
                if i < word_length:
                    current_node = current_node.middle
            else:
                current_node = current_node.right

        if i < word_length or current_node == None:
            return []

        word_li= [] 
        word_li.append([current_node, word, current_node.frequency, current_node.end_word]) 
        i = 0
        while i != len(word_li):
            current_node, current_word = word_li[i][0], word_li[i][1] 
            for j in {current_node.left, current_node.middle, current_node.right}:
                li_element = None
                if j != None:
                    if j == current_node.left or j == current_node.right:
                        li_element = [j, current_word[:-1] + j.letter, j.frequency, j.end_word]
                        if i > 0 and li_element not in word_li:
                            word_li.append(li_element)
                    else:
                        li_element = [j, current_word + j.letter, j.frequency, j.end_word]
                        word_li.append(li_element)
            i += 1

        temp_li = [] 
        for word in word_li:
            frequency, end_word = word[2], word[3] 
            if frequency != None and end_word == True:
                temp_li.append(word)
        word_li = temp_li

        for i in range(len(word_li)):
            word_li[i] = word_li[i][1:]

        if word_li != []:
            word_li.sort(key=lambda x: x[1], reverse=True)
            word_li = word_li[:3] 
            for i in range(len(word_li)):
                word_li[i] = WordFrequency(word_li[i][0], word_li[i][1])

        return word_li
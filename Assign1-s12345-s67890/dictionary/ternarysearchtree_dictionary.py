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

        self.tst = Node() # creating a Node object
        for word_freq in words_frequencies:
            self.add_word_frequency(word_freq) 

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        
        current_node = self.tst  
        word_length = len(word)
        i = 0

        # traversing through the tree to search for the given word
        while i < word_length and current_node != None:
            letter = word[i] 
            if letter < current_node.letter:
                current_node = current_node.left
            elif letter == current_node.letter:
                i = i + 1
                if i < word_length:
                    current_node = current_node.middle
            else:
                current_node = current_node.right

        if i < word_length or current_node == None or current_node.end_word == False:
            return 0 # word not found in the tree

        return current_node.frequency # returning frequency as word is found
        
    
    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        
        current_node = self.tst
        word_length = len(word_frequency.word)
        char_pos = 0 # position  of current letter in the word
        while char_pos < word_length:
            letter = word_frequency.word[char_pos] 
            if current_node.letter == None:
                current_node.letter = letter

            # traversing the left side of the tree
            if letter < current_node.letter:
                if current_node.left == None:
                    current_node.left = Node()
                current_node = current_node.left
            
            # traversing the right side of the tree
            elif letter > current_node.letter:
                if current_node.right == None:
                    current_node.right = Node()
                current_node = current_node.right

            elif letter == current_node.letter:
                if char_pos == word_length - 1:
                    break
                if current_node.middle == None:
                    current_node.middle = Node()
                current_node = current_node.middle
                char_pos += 1
        # assigning the frequency to the current node
        if current_node.end_word == False:
            current_node.end_word = True
            current_node.frequency = word_frequency.frequency
            return True # word and frequency added to the dictionary
        return False # word already in the dictionary

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        
        if self.search(word) == 0:
            return False # given word not present in the dictionary

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

        while i < len(node_li):
            node = node_li[i] 
            if i == 0:
                node.end_word = False
            if node.middle == None and node.left == None and node.right == None:
                node = None
            i = i + 1
        return True # word deleted

    def autocomplete(self, word: str) -> List[WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
       
        current_node = self.tst 
        word_length = len(word) 
        i = 0
        while i < word_length and current_node != None:
            letter = word[i]
            # traversing to the left node
            if letter < current_node.letter:
                current_node = current_node.left
            # traversing to the the middle node
            elif letter == current_node.letter:
                i += 1 
                if i < word_length:
                    current_node = current_node.middle
            # traversing to the right node
            else:
                current_node = current_node.right

        if i < word_length or current_node == None:
            return [] # returning an empty list as word not found

        word_li= [] 
        word_li.append([current_node, word, current_node.frequency, current_node.end_word]) 
        i = 0
        while i != len(word_li):
            current_node, current_word = word_li[i][0], word_li[i][1] # storing current node and the current word
            for j in {current_node.left, current_node.middle, current_node.right}:
                li_element = None
                # if node is present
                if j != None:
                    # traversing the left or right side of the tree
                    if j == current_node.left or j == current_node.right:
                        li_element = [j, current_word[:-1] + j.letter, j.frequency, j.end_word]
                        if i > 0 and li_element not in word_li:
                            word_li.append(li_element)
                    # if the node is in the middle
                    else:
                        li_element = [j, current_word + j.letter, j.frequency, j.end_word]
                        word_li.append(li_element)
            i += 1

        temp_li = [] 
        # going through the word_li
        for word in word_li:
            frequency, end_word = word[2], word[3] 
            if frequency != None and end_word == True:
                temp_li.append(word)
        word_li = temp_li

        # removing current node from the word_li
        i = 0
        while i < len(word_li):
            word_li[i] = word_li[i][1:]
            i = i + 1

        # if word exists
        if word_li != []:
            word_li.sort(key=lambda x: x[1], reverse=True) # sorting in descending order of frequency
            word_li = word_li[:3] 
            i = 0
            while i< len(word_li):
                # creating WordFrequency and storing words with top three freq in the word_li
                word_li[i] = WordFrequency(word_li[i][0], word_li[i][1]) 
                i = i + 1

        return word_li
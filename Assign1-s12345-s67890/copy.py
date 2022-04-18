#import pandas as pd
import sys
import time
import timeit
import random
import string
from tracemalloc import start

from dictionary import word_frequency
from dictionary.node import Node
from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary
from dictionary.list_dictionary import ListDictionary
from dictionary.hashtable_dictionary import HashTableDictionary
from dictionary.ternarysearchtree_dictionary import TernarySearchTreeDictionary


# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# This is the entry point to run the program in file-based mode.
# It uses the data file to initialise the set of words & frequencies.
# It takes a command file as input and output into the output file.
# Refer to usage() for exact format of input expected to the program.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# -------------------------------------------------------------------

def usage():
    """
    Print help/usage message.
    """
    print('python3 dictionary_test_script.py', '<approach> [data fileName]')
    print('<approach> = <list | hashtable | tst>')
    sys.exit(1)


def add_to_dict(dict, list):
    start_time = timeit.default_timer()

    for pair in list:
        word, frequency = pair.split("  ")
        dict.add_word_frequency(word_frequency=WordFrequency(word, int(frequency)))

    end_time = timeit.default_timer()

    return end_time - start_time

def del_from_dict(dict, list):
    start_time = timeit.default_timer()

    for pair in list:
        word = pair.split("  ")[0]
        dict.delete_word(word)

    end_time = timeit.default_timer()

    return end_time - start_time

def ac_in_dict(dict, str):
    start_time = timeit.default_timer()

    dict.autocomplete(str)

    end_time = timeit.default_timer()

    return end_time - start_time

if __name__ == '__main__':
        # Fetch the command line arguments
    args = sys.argv

    if len(args) != 5:
        print('Incorrect number of arguments.')
        usage()

    # initialise search agent
    agent: BaseDictionary = None
    if args[1] == 'list':
        agent = ListDictionary()
    elif args[1] == 'hashtable':
        agent = HashTableDictionary()
    elif args[1] == 'tst':
        agent = TernarySearchTreeDictionary()
    else:
        print('Incorrect argument value.')
        usage()

    # read from data file to populate the initial set of points
    data_filename = args[2]
    words_frequencies_from_file = []
    try:
        data_file = open(data_filename, 'r')
        for line in data_file:
            values = line.split()
            word = values[0]
            frequency = int(values[1])
            word_frequency = WordFrequency(word, frequency)  # each line contains a word and its frequency
            words_frequencies_from_file.append(word_frequency)
        data_file.close()
        agent.build_dictionary(words_frequencies_from_file)
    except FileNotFoundError as e:
        print("Data file doesn't exist.")
        usage()

    command_filename = args[3]
    output_filename = args[4]
    # Parse the commands in command file
    try:
        command_file = open(command_filename, 'r')
        output_file = open(output_filename, 'w')

        for line in command_file:
            command_values = line.split()
            command = command_values[0]
            # search
            if command == 'S':
                word = command_values[1]
                search_result = agent.search(word)
                if search_result > 0:
                    output_file.write(f"Found '{word}' with frequency {search_result}\n")
                else:
                    output_file.write(f"NOT Found '{word}'\n")

            # add
            elif command == 'A':
                word = command_values[1]
                frequency = int(command_values[2])
                word_frequency = WordFrequency(word, frequency)
                if not agent.add_word_frequency(word_frequency):
                    output_file.write(f"Add '{word}' failed\n")
                else:
                    output_file.write(f"Add '{word}' succeeded\n")

            # delete
            elif command == 'D':
                word = command_values[1]
                if not agent.delete_word(word):
                    output_file.write(f"Delete '{word}' failed\n")
                else:
                    output_file.write(f"Delete '{word}' succeeded\n")

            # check
            elif command == 'AC':
                word = command_values[1]
                list_words = agent.autocomplete(word)
                line = "Autocomplete for '" + word + "': [ "
                for item in list_words:
                    line = line + item.word + ": " + str(item.frequency) + "  "
                output_file.write(line + ']\n')
            else:
                print('Unknown command.')
                print(line)

        output_file.close()
        command_file.close()
    except FileNotFoundError as e:
        print("Command file doesn't exist.")
        usage()


    print("hey")
    dict = {}
    words_frequencies_from_file = []
    
    file = open('sampleDataToy.txt', 'r')
    for line in file:
        values = line.split()
        word = values[0]
        frequency = int(values[1])
        word_frequency = WordFrequency(word, frequency)  # each line contains a word and its frequency
        words_frequencies_from_file.append(word_frequency)
        print(word)
    
    agent.build_dictionary(words_frequencies_from_file)
    
    fileLines = file.readlines()
       
    while len(words_frequencies_from_file) < 10:
        word = fileLines[random.randint(1, 20)]
     
    with open('new.txt', 'w') as output_file:
        for i in words_frequencies_from_file:
            output_file.write(i[0])
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
    
def print_description(method_name, operation):
    if operation == "add":
        print("\nAdding words to dictionary:")
    elif operation == "delete":
        print("\nDeleting words from dictionary:")
    elif operation == "autocomplete":
        print("\nAutocompleted words from dictionary")

    if operation == "autocomplete":
        for title in [f'Words {operation}', 'Time taken']:
            print(title.ljust(25), end='')
        print()
    else:
        for title in [f'Words {operation}', 'Unsorted', 'Ascending', 'Descending']:
            print(title.ljust(25), end='')
        print()

    for i in method_name:
        for j in i:
            if isinstance(j, int):
                print(format(j).ljust(25), end='')
            else:
                print(format(j, '5f').ljust(25), end='')
        print()

    return

def dict_addition(dict, list):
    initial_time = timeit.default_timer()

    for w_f in list:
        word, frequency = w_f.split("  ")
        dict.add_word_frequency(word_frequency=WordFrequency(word, int(frequency)))
    finish_time = timeit.default_timer()
    return finish_time - initial_time

def dict_deletion(dict, list):
    initial_time = timeit.default_timer()
    for w_f in list:
        word = w_f.split("  ")[0]
        dict.delete_word(word)
    finish_time = timeit.default_timer()
    return finish_time - initial_time

def dict_autocompletion(dict, str):
    initial_time = timeit.default_timer()
    dict.autocomplete(str)
    final_time = timeit.default_timer()
    return final_time - initial_time

def dict_search(dict, word):
    initial_time = timeit.default_timer()
    dict.search(word)
    final_time = timeit.default_timer()
    return final_time - initial_time


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
    data_filename = args[2]
    words_frequencies_from_file = []
    
    data_file = open(data_filename, 'r')
    for line in data_file:
        values = line.split()
        word = values[0]
        frequency = int(values[1])
        word_frequency = WordFrequency(word, frequency)  # each line contains a word and its frequency
        words_frequencies_from_file.append(word_frequency)
    data_file.close()
    agent.build_dictionary(words_frequencies_from_file)
    
    # Generate words
    word_dict = {}

    '''with open('sampleDataToy.txt', 'r') as input_file:
        fileLines = input_file.readlines()
        while len(word_dict.keys()) < 10:
            word = fileLines[random.randint(0, 19)]
            word = word.replace("\n", "") # Get a random line num
            word = word.replace("-", "")
            word = word.lower()

            if word not in word_dict:
                word_dict[word] = random.randint(1, 10000000) # 1 - 10mil score

    with open('new2.txt', 'w') as output_file:
        for key in word_dict:
            output_file.write(f"{key}  {word_dict[key]}\n")

'''
    with open('sampleDataToy.txt', 'r') as input_file:
            fileLines = input_file.readlines()
            while len(word_dict.keys()) < 10:
                word = fileLines[random.randint(0, 19)]
                word = word.replace("\n", "") # Get a random line num
                word = word.replace("-", "")
                word = word.lower()
                values = line.split()
                word = values[0]
                frequency = int(values[1])


                if word not in word_dict:
                    word_dict[word] = random.randint(1, 10000000) # 1 - 10mil score

    with open('new2.txt', 'w') as output_file:
        for key in word_dict:
            output_file.write(f"{word} {frequency}\n")



    words_to_use = 8

    lines = open('new.txt').readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
    ds = {} # Datasets

    ds_names = ["ds1", "ds2", "ds3"]

    for ds_name in ds_names:
        random.shuffle(lines)
        ds[ds_name + "_unsort"] = lines[:words_to_use]
        ds[ds_name + "_asc"] = sorted(ds[ds_name + "_unsort"])
        ds[ds_name + "_desc"] = sorted(ds[ds_name + "_unsort"], reverse=True)

    sizes = [1,2,4,8]
    ds_add = {}

    for ds_key in ds:
        cur_size = 0
        time_taken = []
        temp_agent = agent

        for size in sizes:
            time_taken.append(dict_addition(temp_agent, ds[ds_key][cur_size:size])) #form a new dict and add word to that dont append into the existing dict for AUTOCOMPLETION FOR SUHAVNI
            cur_size = size
            if len(time_taken) > 1:
                time_taken[-1] += time_taken[-2]

        ds_add[ds_key] = time_taken

    add_table = []
    for size in sizes:
        add_table.append([size, [], [], []])

    for ds_add_key in ds_add:
        for i in range(len(ds_add[ds_add_key])):
            sort_status = ds_add_key.split("_")[1]
            for j in range(len(add_table)):
                if sizes[i] == add_table[j][0]:
                    if sort_status == "unsort":
                        add_table[j][1].append(ds_add[ds_add_key][i])
                    elif sort_status == "asc":
                        add_table[j][2].append(ds_add[ds_add_key][i])
                    elif sort_status == "desc":
                        add_table[j][3].append(ds_add[ds_add_key][i])

    for i in range(len(add_table)):
        for j in range(1, len(ds_names) + 1):
            add_table[i][j] = sum(add_table[i][j]) / 3

    print_description(add_table, 'add')
    


    # Shrinking dictionary (delete word)
    sizes = [1,2,4,8]
    ds_del = {}

    for ds_key in ds:
        cur_size = 0
        time_taken = []
        temp_agent = agent

        for size in sizes:
            time_taken.append(dict_deletion(temp_agent, ds[ds_key][cur_size:size]))
            cur_size = size
            if len(time_taken) > 1:
                time_taken[-1] += time_taken[-2]

        ds_del[ds_key] = time_taken

    del_table = []
    for size in sizes:
        del_table.append([size, [], [], []])

    for ds_del_key in ds_del:
        for i in range(len(ds_del[ds_del_key])):
            sort_status = ds_del_key.split("_")[1]
            for j in range(len(del_table)):
                if sizes[i] == del_table[j][0]:
                    if sort_status == "unsort":
                        del_table[j][1].append(ds_del[ds_del_key][i])
                    elif sort_status == "asc":
                        del_table[j][2].append(ds_del[ds_del_key][i])
                    elif sort_status == "desc":
                        del_table[j][3].append(ds_del[ds_del_key][i])

    for i in range(len(del_table)):
        for j in range(1, len(ds_names) + 1):
            del_table[i][j] = sum(del_table[i][j]) / 3

    print_description(del_table, 'delete')

    # Autocompleting dictionary (ac word)

    sizes = []

    for num in range(1, 8):
        sizes.append(num)

    number_of_acs = 3
    ac_phrases = {}

    # Create 10 of each size (based on random word in newData5000.txt) and store in list (not guaranteed to be inside input file)
    for size in sizes:
        phrase_list = []
        time_taken = 0

        while len(phrase_list) < number_of_acs:
            line_num = random.randint(0, len(lines) - 1)
            cur_word = lines[line_num].split("  ")[0]
            
            phrase = ""
            if len(cur_word) >= size:
                phrase = cur_word[:size]

            if phrase != "" and phrase not in phrase_list:
                phrase_list.append(phrase)

        for phrase in phrase_list:
            time_taken += dict_autocompletion(agent, phrase)
            #print(time_taken)

        # Get average time
        ac_phrases[size] = time_taken / number_of_acs
        #print(ac_phrases[size])
    ac_table = []

    for key in ac_phrases:
        ac_table.append([key, ac_phrases[key]])

    print_description(ac_table, 'autocomplete')


    sizes = []

    for num in range(1, 8):
        sizes.append(num)

    number_of_acs = 3
    ac_phrases = {}

    # Create 10 of each size (based on random word in newData5000.txt) and store in list (not guaranteed to be inside input file)
    for size in sizes:
        phrase_list = []
        time_taken = 0

        while len(phrase_list) < number_of_acs:
            line_num = random.randint(0, len(lines) - 1)
            cur_word = lines[line_num].split("  ")[0]
            phrase_list.append(cur_word)

        
            time_taken += dict_search(agent, cur_word)
        print(time_taken, cur_word)

        # Get average time
        #ac_phrases[size] = time_taken / number_of_acs
        #print(ac_phrases[size])
    
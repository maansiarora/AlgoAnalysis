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
# 
# This is the entry point to run the program in file-based mode.
# It uses the data file to initialise the set of words & frequencies.
# It takes a command file as input and output into the output file.
# Refer to usage() for exact format of input expected to the program.
#
# 
# We have created this file for empirical analysis of our algorithms
# and will use it for calculating time complexities for different datasets.
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
        word, frequency = w_f.split("    ")
        dict.add_word_frequency(word_frequency=WordFrequency(word, int(frequency)))
    finish_time = timeit.default_timer()
    return finish_time - initial_time
 
def dict_deletion(dict, list):
    initial_time = timeit.default_timer()
    for w_f in list:
        word = w_f.split("    ")[0]
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
 
    # read from data file to populate the initial set of points
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
    with open('sampleData.txt', 'r') as input_file:
        fileLines = input_file.readlines()
 
    # randomly selecting 1000 words out of 5000 words from sampleData.txt
    with open('new.txt', 'w') as output_file:
        while len(word_dict.keys()) < 1000:
            x = fileLines[random.randint(0, 4999)]
            word= x[0:x.index(" ")]
            frequency= x[x.index(" "):len(x)]
            if word not in word_dict:
                word_dict[word]=frequency
                output_file.write(f"{word}  {frequency}")
    

    lines_used = 1000
 
    lines = open('new.txt').readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "")
    dataset = {} # Datasets
 
    dataset_names = ["dataset1", "dataset2", "dataset3"]
 
    for dataset_name in dataset_names:
        random.shuffle(lines)
        dataset[dataset_name + "_unsort"] = lines[:lines_used]
        dataset[dataset_name + "_asc"] = sorted(dataset[dataset_name + "_unsort"])
        dataset[dataset_name + "_desc"] = sorted(dataset[dataset_name + "_unsort"], reverse=True)
 


    # Scenario 1 - growing dictionary
    # defining the sizes of words to be added to the base dictionary
    sizes = [10, 100, 500, 1000, 2000]
    dataset_addition = {}
    
    for dataset_key in dataset:
        current_size = 0 # current size of the dictionary
        time_taken = [] # list to define the time taken to perform the function
        temp_agent = agent 
 
        for size in sizes:
            time_taken.append(dict_addition(temp_agent, dataset[dataset_key][current_size:size])) 
            current_size = size
            if len(time_taken) > 1:
                time_taken[-1] += time_taken[-2]
 
        dataset_addition[dataset_key] = time_taken
 
    addition_table = []
    for size in sizes:
        addition_table.append([size, [], [], []])
 
    for dataset_add_key in dataset_addition:
        for i in range(len(dataset_addition[dataset_add_key])):
            sort_status = dataset_add_key.split("_")[1]
            for j in range(len(addition_table)):
                if sizes[i] == addition_table[j][0]:
                    if sort_status == "unsort":
                        addition_table[j][1].append(dataset_addition[dataset_add_key][i])
                    elif sort_status == "asc":
                        addition_table[j][2].append(dataset_addition[dataset_add_key][i])
                    elif sort_status == "desc":
                        addition_table[j][3].append(dataset_addition[dataset_add_key][i])
 
    for i in range(len(addition_table)):
        for j in range(1, len(dataset_names) + 1):
            addition_table[i][j] = sum(addition_table[i][j]) / 3
 
    print_description(addition_table, 'add') # priting the table describing the time compexities in different scenarios 
   
 
    # Scenario 2 - shrinking dictionary
    # defining the sizes of words to be deleted from the base dictionary
    sizes = [10, 100, 200, 400, 800]
    dataset_del = {}
 
    for dataset_key in dataset:
        current_size = 0 # current size of the dictionary
        time_taken = [] # list to define the time taken to perform the function
        temp_agent = agent
 
        for size in sizes:
            time_taken.append(dict_deletion(temp_agent, dataset[dataset_key][current_size:size]))
            current_size = size
            if len(time_taken) > 1:
                time_taken[-1] += time_taken[-2]
 
        dataset_del[dataset_key] = time_taken
   
    deletion_table = []
    for size in sizes:
        deletion_table.append([size, [], [], []])
 
    for dataset_del_key in dataset_del:
        for i in range(len(dataset_del[dataset_del_key])):
            sort_status = dataset_del_key.split("_")[1]
            for j in range(len(deletion_table)):
                if sizes[i] == deletion_table[j][0]:
                    if sort_status == "unsort":
                        deletion_table[j][1].append(dataset_del[dataset_del_key][i])
                    elif sort_status == "asc":
                        deletion_table[j][2].append(dataset_del[dataset_del_key][i])
                    elif sort_status == "desc":
                        deletion_table[j][3].append(dataset_del[dataset_del_key][i])
 
    for i in range(len(deletion_table)):
        for j in range(1, len(dataset_names) + 1):
            deletion_table[i][j] = sum(deletion_table[i][j]) / 3

    #printing the description table for time complexities of different scenarios
    print_description(deletion_table, 'delete') 


    # Scenario 3 - static dictionary
    # Autocompleting dictionary

    sizes = []
    for num in range(1, 8):
        sizes.append(num)
 
    number_of_autocompletes = 3
    autocomplete_phrases = {}
    for size in sizes:
        phrase_list = []
        time_taken = 0
 
        while len(phrase_list) < number_of_autocompletes:
            line_num = random.randint(0, len(lines) - 1) # randomly selecting a line number from our dataset
            current_word = lines[line_num].split("  ")[0] # getting the word of that randomly selected line
           
            phrase = ""
            if len(current_word) >= size:
                phrase = current_word[:size]
            if phrase != "" and phrase not in phrase_list:
                phrase_list.append(phrase)
 
        for phrase in phrase_list:
            time_taken += dict_autocompletion(agent, phrase)
 
        # getting the average time
        autocomplete_phrases[size] = time_taken / number_of_autocompletes
        
    ac_table = []
    for key in autocomplete_phrases:
        ac_table.append([key, autocomplete_phrases[key]])
 
    print_description(ac_table, 'autocomplete') #printing the description table for autocomplete operation
 
 
    # Scenario 3 - static dictinary
    # search operation
    sizes = []
 
    for number in range(1, 8):
        sizes.append(number)
 
    number_of_acs = 3
    autocomplete_phrases = {}
    
    for size in sizes:
        phrase_list = []
        time_taken = 0
 
        while len(phrase_list) < number_of_acs:
            line_number = random.randint(0, len(lines) - 1) # randomly selecting a line number from our dataset
            current_word = lines[line_number].split("  ")[0] # getting the word of that randomly selected line
            phrase_list.append(current_word)
 
            time_taken += dict_search(agent, current_word) # calculating the time to search the current word
        print(time_taken, current_word) #printing the time taken for the operations along with the word being searched

 
    
   


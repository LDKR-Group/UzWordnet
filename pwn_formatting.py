# importing necessary packages
import csv
import re

import pandas as pd
import requests

"""function to safely read the file and clean it"""
def read_file(name):
    # read the file line by line (= synset by synset)
    with open(name) as f:
        lines = f.readlines()
        del lines[0:29] # deleting information about copyright, version, license
        return lines


"""function to parse a single synset(line) from the file data.pos"""
def parse_synset(col_names, line):

    gloss_split = line.split("|") # splitting into gloss (after '|') and everything that is before '|'
    # NOTE: there are no examples without the definitions!
    synset_details = gloss_split[0]
    gloss = gloss_split[1]
    position = gloss.find('"')# find the position of '"' char (if any)
    if (position != -1): # case - gloss contains examples
        definition = gloss[:(position - 2)].lstrip() # extracting gloss and cleaning from trailing or heading spaces
        examples = gloss[position:].rstrip() # extracting examples and cleaning from trailing or heading spaces
    else: # case - gloss contains no examples
        examples = "" # empty examples field
        definition = gloss.rstrip().lstrip() # entire gloss is definition and cleaning from trailing or heading spaces

    # parsing synset details
    synset_details = synset_details.split(" ")# separating the left spring by spaces
    synset_id = synset_details[0] # getting PWN synset id
    pos = synset_details[2] # getting part of speech

    # parsing lemma(s)
    lemmas = [] 
    number_lemmas = int(synset_details[3], 16) # getting the number of lemmas in the given synset
    for i in range(0, number_lemmas):
        lemmas.append(' '.join(synset_details[(4 + i*2)].split('_'))) # parsing and formatting lemmas
    
    # parsing parent(s)
    parents = []
    for index, item in enumerate(synset_details): # search for specific notion of parent synset and taking it
        if item == '@' or item == '@i':
            parents.append(synset_details[(index + 1)])

    # assembling parsed fields in the array
    parsed_info = [synset_id, ', '.join(parents), pos, ', '.join(lemmas), definition, examples]
    
    # filling the unknown fields with empty strings
    for i in range(len(col_names) - len(parsed_info)):
        parsed_info.append('')
    
    # creating a dictionary for future row-append to the dataframe
    dictionary = dict(zip(col_names, parsed_info))
    
    return dictionary


"""function to create dataframe"""
def make_dataframe(col_names, lines):
    df = pd.DataFrame(columns=col_names)# creating a dataframe for reading the data.pos file
    for line in lines:
        df = df.append(parse_synset(col_names, line), ignore_index=True)
    return df


"""defining main function (and parameters to use the functions with)"""
def main():
    filename = "./data.noun" # specifying file to read
    lined_file = read_file(filename) # reading file into arrays of lines (synsets)
    
    # creating columns for the dataframe (table)
    dfColumns = ['Synset_id','Parent(s)', 'PoS', 'Lemma(s)','Definition','Example(s)', 'Target lemma(s)','Target definition','Target examples','Notes']
    df = make_dataframe(dfColumns, lined_file) # making the dataframe
    
    # saving the result for further processing
    df.to_csv('./pwn.csv') # with index
    df.to_csv('./pwn_unindexed.csv', index=False) # without index



# calling main function
if __name__ == "__main__":
    main()

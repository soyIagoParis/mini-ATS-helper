input_string2 = """Python Python Python from the depths of dark web. There is a web made of dark web. Iago París Fernández once and again Iago París Fernández. The Spark."""
input_string1 = """There was a time when people were mouses, then the Cataclysm came and all died very rightfully. Yeah, all died."""


import nltk
from pprint import pprint
from langdetect import detect
import re
import shelve
import pandas
pandas.set_option('display.max_rows', 200)

# --- FUNCTIONS ---
# Returns the duplicates of a list and the number of times said duplicates appear on the list.
# Info returned as a dictionary {duplicate:times}.
def get_duplicates_and_count(list):
    seen = set()
    duplicates = {}

    for item in list:    
        if item in seen:
            if item in duplicates:
                duplicates[item] += 1
            else:
                duplicates[item] = 2
        else:
            seen.add(item)


    # Sort dictionary by descending duplicate count
    sorted_duplicates = sorted(duplicates.items(), key=lambda key_value_pair: key_value_pair[1], reverse=True)
    # Output is a list so reconvert to dict
    return dict(sorted_duplicates)

# Returns a list of uppercased words not beacuse of punctuation that only appear one time on the text
def get_unique_names(list_of_words, list_of_duplicates):
    names = set()
    word_iterator = iter(list_of_words)
    punctuation_and_emoji_regex = r'(\.|\?|\!|\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])+'
    for word in word_iterator:
        if re.search(punctuation_and_emoji_regex, word):
            next(word_iterator, None)
            continue
        if word[0].isupper():
            names.add(word)

    unique_names = []
    for name in names:
        if name not in list_of_duplicates:
            unique_names.append(name)
    return unique_names

# Returns a hash for a text with more than 10 characters dependent on its length
def get_string_hash(source):
    if len(source) > 300:
        return ''.join(input_source[i] for i in range(0,300,10))
    elif len(source) > 10:
        return ''.join(input_string[i] for i in range(10))
    else:
        raise Exception("Your input string is very small. Use at least 10 characters.") 

# Coverts and array of tuples (dict, name) into a dataframe concatenating them vertically and adding some columns, specifically:
# type = name
def convert_dicts_to_dataframe(dicts_and_names):
    dataframes = []
    for dict, name in dicts_and_names:
        if len(dict) > 0:
            dataframe = pandas.DataFrame.from_dict(dict, 'index')
            dataframe.rename(columns={0:'Ocurrences'}, inplace=True)
            dataframe['Type'] = name
            dataframe['Source'] = input_string
            dataframe['Source_hash'] = get_string_hash(input_string)
            print(dataframe)
            dataframes.append(dataframe)
    return pandas.concat(dataframes, axis=0)

# --- END OF FUNCTIONS ---

print("Introduce the text you want to analyze:")
# input_string = input()
input_string = input_string2

# Processing of the input string
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+') # removes punctuation
words = tokenizer.tokenize(input_string)
words_punctuated = nltk.tokenize.word_tokenize(input_string) # TODO: Two-tokenizations, can I tokenize and then remove punctuation?

language_code = detect(input_string)
language_dic = {'es':'spanish', 'en':'english'}
stop_words = set(nltk.corpus.stopwords.words(language_dic[language_code]))
 
# Excludes the stop words
meaningful_words = []

for word in words:
    if word.lower() not in stop_words:
        meaningful_words.append(word)
 
word_pairs = [meaningful_words[i - 1] + " " + meaningful_words[i] for i in range(len(meaningful_words))]
word_triads = [meaningful_words[i - 2] + " " + meaningful_words[i - 1] + " " + meaningful_words[i] for i in range(len(meaningful_words))]


# Formatting to dataframe TODO: ¿can I skip the dict part?
duplicate_words = get_duplicates_and_count(meaningful_words)
unique_names = get_unique_names(words_punctuated, duplicate_words)
unique_names_dict = {x: 1 for x in unique_names}
duplicate_pairs = get_duplicates_and_count(word_pairs)
duplicate_triads = get_duplicates_and_count(word_triads)

dicts_and_names = [
    (duplicate_triads, 'duplicate triad'),
    (duplicate_pairs, 'duplicate pair'),
    (unique_names_dict, 'unique name'),
    (duplicate_words, 'duplicate word')
]

temp_history = convert_dicts_to_dataframe(dicts_and_names)

print("\nRESULTS OF THE TEXT ANALYSIS:\n")
print(temp_history)

# Save into database

print("Do you want to add this results to database (y/n):")
answer = input()
if answer.lower() == "n":
    print("\nResults not saved.")
if answer.lower() == "y":
    s = shelve.open('database.db')
    try:
        if 'history' in s and isinstance(s['history'], pandas.DataFrame):
            history = s['history']
            source_hash = get_string_hash(input_string)
            if source_hash not in history.Source_hash.unique(): # Save only if not already present
                history = pandas.concat([history, temp_history], axis=0)
                history['Ocurrences'] = history['Ocurrences'].astype(int)
                s['history'] = history
                print('\nAdded data from: "' + input_string[0:100] + '".')
            else:
                print('\nThere is already data from: "' + input_string[0:100] + '".')
                
        else: # Create history
            s['history'] = temp_history
    finally:
        print("\nCOMPLETE HISTORY:\n")
        print(s['history'])
        s.close()
    




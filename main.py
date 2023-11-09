input_string = """
Beam Suntory is Crafting the Spirits that Stir the World. Rooted in two centuries of family heritage, Beam Suntory has evolved into the world's third largest leading premium spirits company ... where each employee is treated like family and trusted with legacy. With our greatest assets - our premium spirits and our people - we're driving growth through impactful marketing, innovation and an entrepreneurial spirit. Beam Suntory is a place where you can come Unleash your Spirit by making an impact each and every day.

Junior ML Engineer - Gen AI

What makes this a great opportunity?

The Junior ML Engineer will help to drive Generative AI solutions in the company, working actively in the development of use cases, integrating data from multiple sources, creating data connectors, structuring text for LLM task execution and defining conversational workflows.

This role will work closely with cross-functional teams to develop and implement data-driven solutions that meet business needs. This is a global role to develop and support Gen AI projects across multiple business functions.

Role Responsibilities

Key Responsibilities


     Data Integration from multiple sources, including APIs, databases, streaming data, and external datasets and create data connectors and interfaces to facilitate data exchange between systems.
     Prompt engineering, structuring text in the best way to be understandable for LLM for task execution
     Define and maintain conversational workflows for Gen AI tools
     Collaborate with data scientists and AI Data analysts to design data structures that align with business requirements.
     Maintain comprehensive technical and functional documentation for technical for knowledge sharing and troubleshooting.
     Stay current with emerging data engineering technologies and tools.
     Evaluate and recommend new technologies that can improve data engineering processes
     Identify opportunities where AI technologies can be applied to improve business processes
     Understand business processes across BSI system´s landscape (SAP ECC, CRM, Reporting)


Relationships


    Reporting to: Vice President Digital Delivery
    Direct Reports: Manager Dig.Delivery for Gen AI

    Key Organizational Interfaces:
        Gen AI Team
        IT software and cloud engineers
        IT Solution Architects & Managers
        Key business Stakeholders (BPOs, Key users)




    Role Dimension:
        Part of the digital delivery team for Gen AI products and solutions


Qualifications

Core Competencies (Maximum 4)


     Data Integration
     Programing in Python
     Natural Language Processing (NLP)


Skills


     Advanced in programming languages like Python (desired knowledge of Java, or Scala).
     Knowledge of SQL and database management systems (e.g., PostgreSQL, MySQL, or NoSQL databases).
     Desired experience with data warehousing and ETL tools (e.g., Apache Spark, Apache Airflow, or Talend).
     Familiarity with cloud platforms like AWS, Azure, or Google Cloud.
     Problem-solving view and analytical skills.
     Good communication and collaboration skills.
     Attention to detail and a commitment to data quality and governance.


Education/Experience


     Bachelor’s degree in computer science, Information Technology, or a related field (Master in AI preferred).
     At least 1-3 years of experience in ML engineering or a related field with Generative AI.
     Must be fluent in English language (speak, read, write)
     Mobility


Position based in Madrid (Spain), availability to travel 25% internationally.

At Beam Suntory, people are our number one priority, and we believe our people grow together in diverse and inclusive environments where their unique insights, experiences and backgrounds are valued and respected. Beam Suntory is committed to equal employment opportunity regardless of race, color, ancestry, religion, sex, national origin, sexual orientation, age, citizenship, marital status, disability, gender identity, military veteran status and all other characteristics, attributes or choices protected by law. All recruitment and hiring decisions are based on an applicant’s skills and experience.

"""

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


# --- END OF FUNCTIONS ---

# TODO: prompt asking for string

# Processing of the input string
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+') # removes punctuation
words = tokenizer.tokenize(input_string)
words_punctuated = nltk.tokenize.word_tokenize(input_string) # Two-tokenizations, can I tokenize and then remove punctuation?

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


# - PRINTING -

duplicate_words = get_duplicates_and_count(meaningful_words)
# print("\nDuplicate list:\n")
# pprint(duplicate_words, sort_dicts=False)
# print("\n")

unique_names = get_unique_names(words_punctuated, duplicate_words)
# print("\nUnique names:\n")
# pprint(unique_names)
# print("\n")

duplicate_pairs = get_duplicates_and_count(word_pairs)
# print("\nPair duplicate list:\n")
# pprint(duplicate_pairs, sort_dicts=False)
# print("\n")

duplicate_triads = get_duplicates_and_count(word_triads)
# print("\nTriad duplicate list:\n")
# pprint(duplicate_triads, sort_dicts=False)
# print("\n")

# - Saving in dataframe -
# TODO: shelve the data
unique_names_dict = {x: 1 for x in unique_names}

dicts_and_names = [
    (duplicate_triads, 'duplicate triad'),
    (duplicate_pairs, 'duplicate pair'),
    (unique_names_dict, 'unique name'),
    (duplicate_words, 'duplicate word')
]
dataframes = []
for dict, name in dicts_and_names:
    dataframe = pandas.DataFrame.from_dict(dict, 'index')
    dataframe['Type'] = name
    dataframe['Source'] = input_string
    dataframe['Source_hash'] = ''.join(input_string[i] for i in range(10,300,10))
    dataframes.append(dataframe)

history = pandas.concat(dataframes, axis=0)
history.rename(columns={0:'Ocurrences'}, inplace=True)

print("\n")
print(history)
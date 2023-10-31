example_string = """Desarrollador Python - Inteligencia Artificial

Craftercode busca un desarrollador senior con experiencia en lenguajes de programación orientados a objetos, especialmente Java y Python. Valoramos la experiencia en proyectos relacionados con la inteligencia artificial, incluyendo Machine Learning, Inteligencia Artificial Generativa y Procesamiento de Lenguaje Natural (NLP).

Ubicación: Madrid, España (Posición 100% Remota)"""


import nltk
import pprint
nltk.download("stopwords")

language = "spanish" # TODO: autodetect language
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+') # remove punctuation
words = tokenizer.tokenize(example_string)

print("\nWords list:\n\n" + str(words) + "\n")


from nltk.corpus import stopwords
 
stop_words = set(stopwords.words(language))
 

# excludes the stop words
meaningful_words = []

for word in words:
    if word.lower() not in stop_words:
        meaningful_words.append(word)
 
print("\nMeaningful words list:\n\n" + str(meaningful_words) + "\n")



# Get duplicates list and count
seen = set()
duplicates = {}

for word in meaningful_words:    
    if word in seen:
        if word in duplicates:
            duplicates[word] += 1
        else:
            duplicates[word] = 1
    else:
        seen.add(word)

# TODO: Sort dic by count
print("\nDuplicate list:\n")
pprint.pprint(duplicates)
print("\n")
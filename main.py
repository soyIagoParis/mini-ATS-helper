input_string = """

Descripción
SG Tech 😎


¡Hola! En SG Tech estamos buscando a una persona talentosa y apasionada por el desarrollo de software para unirse a nuestro equipo como Desarrollador/a Python. Si te encanta programar en Python, tienes experiencia en el área de Inteligencia Artificial y estás interesado en trabajar en un ambiente remoto, ¡esta oportunidad es para ti! 😉✨


Acerca de nosotros 🏢


SG Tech es una empresa líder en el campo de la tecnología, especializada en soluciones innovadoras basadas en algoritmos y sistemas inteligentes. Nos enorgullece brindar a nuestros clientes las mejores soluciones de software, enfocándonos en la usabilidad, la eficiencia y la escalabilidad. Trabajamos en estrecha colaboración con nuestros clientes para desarrollar soluciones a medida que impulsen su éxito en el mercado.


Responsabilidades laborales 🤓


    Desarrollar y mantener aplicaciones utilizando Python y otros lenguajes de programación según sea necesario.
    Colaborar con el equipo de desarrollo para diseñar soluciones efectivas y escalables.
    Participar activamente en la implementación de proyectos relacionados con Inteligencia Artificial.
    Realizar pruebas y depurar código para garantizar el rendimiento y la calidad del software.
    Mantenerse actualizado/a con las últimas tendencias y avances en el campo.


¿Qué ofrecemos? 🌟


    Oportunidad de trabajar en proyectos emocionantes y desafiantes relacionados con Inteligencia Artificial.
    Colaboración con un equipo de profesionales altamente calificados y apasionados.
    Posibilidad de aprendizaje y crecimiento continuo en un entorno innovador.
    Horario: L-J: 9-19h V: 9-15h Jornada intensiva verano.
    Proyecto en remoto 100%.
    Salario competitivo acorde a tu experiencia y habilidades.

Requisitos

    Experiencia mínima de 2 años como Desarrollador/a Python.
    Experto/a en lenguajes de programación orientados a objetos, especialmente Java y Python.
    Conocimientos y experiencia en temas relacionados con Inteligencia Artificial, como Machine Learning y IA Generativa.
    Capacidad para trabajar de forma remota sin supervisión constante.


Si te apasiona la programación en Python y estás interesado/a en formar parte de nuestro equipo, ¡no dudes en postularte para este emocionante puesto! 😃🚀 Envíanos tu CV actualizado y una breve descripción de tus proyectos anteriores.


¡Esperamos poder conocerte y dar el próximo paso en tu carrera profesional juntos! 👍🔥
"""

import nltk
from pprint import pprint
from langdetect import detect
import re
import shelve
import pandas

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
    punctuation_and_emoji_regex = "(\.|\?|\!|\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])+"
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
print("\nDuplicate list:\n")
pprint(duplicate_words, sort_dicts=False)
print("\n")

unique_names = get_unique_names(words_punctuated, duplicate_words)
print("\nUnique names:\n")
pprint(unique_names)
print("\n")

duplicate_pairs = get_duplicates_and_count(word_pairs)
print("\nPair duplicate list:\n")
pprint(duplicate_pairs, sort_dicts=False)
print("\n")

duplicate_triads = get_duplicates_and_count(word_triads)
print("\nTriad duplicate list:\n")
pprint(duplicate_triads, sort_dicts=False)
print("\n")

# - Saving in dataframe -
unique_names_dict = {x: 1 for x in unique_names}

dicts = [
    duplicate_words,
    unique_names_dict,
    duplicate_pairs,
    duplicate_triads
]
dataframes = []
for dict in dicts:
    dataframe = pandas.DataFrame.from_dict(dict, 'index')
    print(dataframe)
    dataframes.append(dataframe)
history = pandas.concat(dataframes, axis=0)

print(history)
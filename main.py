example_string = """Desarrollador Python - Inteligencia Artificial

Craftercode busca un desarrollador senior con experiencia en lenguajes de programación orientados a objetos, especialmente Java y Python. Valoramos la experiencia en proyectos relacionados con la inteligencia artificial, incluyendo Machine Learning, Inteligencia Artificial Generativa y Procesamiento de Lenguaje Natural (NLP).

Ubicación: Madrid, España (Posición 100% Remota)"""


import nltk
import pprint
string = "GeeksForGeeks is the best best Computer Science Portal ."
words = nltk.word_tokenize(example_string)
print()
print("Word list:")
print(words)
print()

seen = set()
duplicates = {}

for word in words:    
    if word in seen:
        if word in duplicates:
            duplicates[word] += 1
        else:
            duplicates[word] = 1
    else:
        seen.add(word)

print()
print("Duplicate list:")
pprint.pprint(duplicates)
print()
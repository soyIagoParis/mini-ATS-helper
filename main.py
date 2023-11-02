big_example_string = """
En Futura VIVE, somos una empresa líder en la fabricación de Robótica Social dotada de Inteligencia Artificial, Holografía, y soluciones de Realidad Aumentada y Realidad Virtual. Nuestra misión es ayudar a empresas y a la sociedad en general a mejorar gracias a la tecnología y la innovación. Estamos buscando un Programador Python altamente talentoso y motivado para unirse a nuestro equipo de desarrollo y contribuir a la creación de soluciones tecnológicas de vanguardia.
Tareas

    Desarrollar y mantener aplicaciones y sistemas basados en Python para la mejora de la interacción entre humanos y robots.
    Colaborar estrechamente con los equipos de ingeniería en la implementación de soluciones de IA y robótica social.
    Participar en el diseño, desarrollo y optimización de algoritmos y modelos de aprendizaje automático.
    Realizar pruebas de software y depuración para garantizar el rendimiento y la estabilidad de las aplicaciones.
    Mantenerse actualizado sobre las mejores prácticas de programación y las últimas tendencias en tecnología.

Requisitos

    Experiencia demostrable en programación Python.
    Conocimiento de bibliotecas y frameworks de Python, como TensorFlow y PyTorch.
    Familiaridad con la programación orientada a objetos y diseño de software.
    Habilidad para resolver problemas de manera efectiva y trabajar en equipo.
    Pasión por la tecnología y la innovación.

Beneficios

    Oportunidad de trabajar en un entorno altamente innovador y tecnológico.
    Colaboración con un equipo multidisciplinario de profesionales apasionados por la tecnología.
    Desarrollo profesional y oportunidades de aprendizaje continuo.
    Salario competitivo y paquete de beneficios atractivo.
    Contribución a la misión de Futura VIVE de mejorar la sociedad a través de la tecnología.

Si eres un apasionado de la programación Python y deseas formar parte de un equipo que impulsa la innovación en robótica y tecnología, te invitamos a unirte a nosotros. Futura VIVE es un lugar donde tus habilidades y creatividad pueden prosperar, y donde puedes contribuir a proyectos que hacen una diferencia real. ¡Esperamos recibir tu solicitud y conocer tu talento!
"""

example_string = """Desarrollador Python - Inteligencia Artificial

Craftercode busca un desarrollador senior con experiencia en lenguajes de programación orientados a objetos, especialmente Java y Python. Valoramos la experiencia en proyectos relacionados con la inteligencia artificial, incluyendo Machine Learning, Inteligencia Artificial Generativa y Procesamiento de Lenguaje Natural (NLP).

Ubicación: Madrid, España (Posición 100% Remota)"""


import nltk
import pprint
# nltk.download("stopwords")


tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+') # removes punctuation
words = tokenizer.tokenize(big_example_string)

print("\nWords list:\n\n" + str(words) + "\n")


from nltk.corpus import stopwords
from langdetect import detect

language_code = detect(big_example_string)
language_dic = {'es':'spanish', 'en':'english'}
stop_words = set(stopwords.words(language_dic[language_code]))
 

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
            duplicates[word] = 2
    else:
        seen.add(word)

# Sort dictionary by descending duplicate count
sorted_duplicates = sorted(duplicates.items(), key=lambda key_value_pair: key_value_pair[1], reverse=True)
# Output is a list so reconvert to dict
sorted_duplicates = dict(sorted_duplicates)


print("\nDuplicate list:\n")
pprint.pprint(sorted_duplicates, sort_dicts=False)
print("\n")
from os import chdir
from unidecode import unidecode
import matplotlib.pyplot as plt

chdir(r'C:\Users\aRaulet\PycharmProjects\WordleProject\CSV')
fichier = open('Lexique383.csv', 'r')
WordleLib = open('wordleLibCSV', 'w')

dicostat = {}

for ligne in fichier.readlines():
    extract = ligne.strip().split(sep=',')[0]
    out = ''
    for i in range(len(extract)):
        dico = {'©':'e', '¨':'e', '¢':'a', '´':'o', '®':'i', 'ª':'e', '¯':'i', '»':'u'}
        if extract[i] == 'Ã':
            pass
        elif extract[i] in dico:
            out += dico[extract[i]]

        else:
            out += extract[i]



    if len(out) in dicostat:
        dicostat[len(out)] += 1
    else:
        dicostat[len(out)] = 1

    if len(out) == 5:
        WordleLib.write(out + ',\n')

WordleLib.close()
fichier.close()



print(dicostat)

labels = sorted([ key for key in dicostat])
values = [dicostat[key] for key in labels]
print(labels, values)
# Création du graphique à barres
plt.bar(labels, values)

# Ajout de titre et de labels
plt.xlabel('nombre de lettres')
plt.ylabel('nombre de mots')
plt.show()
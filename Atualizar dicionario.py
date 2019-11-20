import requests
import json

r = requests.get('https://raw.githubusercontent.com/mazucanti/dict-corrector/master/words_dictionary.json')
c = r.content
j = json.load(c)
aux = []

for item in j:
    if item[0] == 'a':
        aux.append(item)
        print("Adicionado")
arq = open('Dicionario/a.json', 'w')

for item in aux:
    arq.write(item + '\n')
arq.close

# adicionar o resto do alfabeto de um jeito mais elegante
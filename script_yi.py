import json
i = {}
y = {}
palavras = {}
with open('words/iy.json', 'rb') as junto:
    palavras = json.load(junto)
    for x in palavras:
        if x[0] == 'i': i[x] = 1
        else: y[x] = 1
with open('words/i.json', 'w', encoding='utf-8') as f:
    json.dump(i,f)

with open('words/y.json', 'w', encoding='utf-8') as f:
    json.dump(y,f)

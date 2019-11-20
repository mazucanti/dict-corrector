import json
import requests

class no_trie():

    def __init__(self, letra: str):
        self.letra = letra
        self.filhos = []
        self.palavra = False
        self.contador = 0


def adiciona_no(raiz, palavra: str):
    no = raiz
    for letra in palavra:
        e_filho = False
        for filho in no.filhos:

            if filho.letra == letra:
                filho.contador += 1
                e_filho = True
                break

        if not e_filho:
            novo_no = no_trie(letra)
            no.filhos.append(novo_no)
            no = novo_no
    no.palavra = True

def importa_base_remota():
    r = requests.get('https://raw.githubusercontent.com/mazucanti/dict-corrector/master/words_dictionary.json')
    conteudo = r.content
    dicionario = json.load(conteudo)
    return dicionario


def cria_trie_dict():
    raiz = no_trie('*')
    dicionario = importa_base_remota()
    for palavra in dicionario:
        adiciona_no(raiz, palavra)
    return raiz

def busca(termo: str):

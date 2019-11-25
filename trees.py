import json
import requests


class trie_node():

    def __init__(self, letter: str):
        self.letter = letter
        self.children = []
        self.word = False
        self.count = 0


def add_node(root, word: str):
    node = root
    for letter in word:
        is_child = False
        for child in node.children:
            if child.letter == letter:
                child.count += 1
                is_child = True
                break
        if not is_child:
            new_node = trie_node(letter)
            node.children.append(new_node)
            node = new_node
    node.word = True


def remote_base_import():
    words = {}
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for letter in alphabet:
        req = requests.get('https://raw.githubusercontent.com/mazucanti/words-base/master/base_words/'+letter+'.json')
        temp = json.loads(req.content.decode('utf-8'))
        words.update(temp)
    return words


def trie_tree():
    root = trie_node('*')
    words = remote_base_import()
    for word in words:
        add_node(root, word)
    return root


def search(root: trie_node, term: str) -> bool:
    found = True
    node = root
    for letter in term:
        if not found:
            break
        found = False
        for child in node.children:
            if letter == child.letter:
                node = child
                found = True
                break
    return

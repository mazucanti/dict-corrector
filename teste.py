import trees
import suggest

avere = trees.trie_tree()
word = 'a'
while "" != word:
    word = input('entre a palavra a ser buscada: ')
    print(trees.search(avere,word))


import trees
import suggest

avere = trees.trie_tree()
word = 'a'
while "" != word:
    word = input('entre a palavra a ser buscada: ')
    print(suggest.gen_sugg(avere,word))


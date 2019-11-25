import trees


def gen_sugg(word: str):
    root = trees.trie_tree()
    node = root
    found = trees.search(node, word)
    valid_letters = ""
    if found:
        print('found')
        return valid_letters
    if not found:
        for letter in word:
            end_of_valid_letters = True
            print('not found')
            for child in node.children:
                if child.letter == letter:
                    valid_letters += letter
                    node = child
                    end_of_valid_letters = False
                    break
            if end_of_valid_letters:
                    break
        final_word = valid_letters + write_sugg(node)
        return final_word


def write_sugg(node):
    max_count = 0
    word = ""
    while not node.word:
        for child in node.children:
            if max_count < child.count:
                max_count = child.count
                max_node = child
        word += max_node.letter
        node = max_node
    return word

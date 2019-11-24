import trees


def gen_sugg(word: str):
    root = trees.trie_tree()
    node = root
    found = trees.search(node, word)
    if found:
        return ""
    if not found:
        valid_letters = ""
        for letter in word:
            reff = node.copy()
            for child in node.children:
                if child.letter == letter:
                    valid_letters += letter
                    node = child
            if node == reff:
                return write_sugg(node, valid_letters)


def write_sugg(node, word):
    max_count = 0
    while not node.word:
        for child in node.children:
            if max_count<child.count:
                max_count = child.count
                max_node = child
        word += max_node.letter
        node = max_node
    return word
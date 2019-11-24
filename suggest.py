import trees


def find_last_letter(word: str):
    root = trees.trie_tree()
    node = root
    found = trees.search(node, word)
    if found:
        return True, None
    if not found:
        for letter in word:
            reff = node.copy()
            for child in node.children:
                if child.letter == letter:
                    node = child
            if node == reff:
                return False, node

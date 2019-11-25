import trees


def gen_sugg(root, word: str):
    if word == "":
        return True, []
    node = root
    found = trees.search(node, word)
    valid_letters = ""
    if found:
        return []
    if not found:
        for letter in word:
            end_of_valid_letters = True
            for child in node.children:
                if child.letter == letter:
                    valid_letters += letter
                    node = child
                    end_of_valid_letters = False
                    break
            if end_of_valid_letters:
                    break
        final_word = valid_letters #+ write_sugg(node)
        return [final_word]



def write_sugg(node):
    count = 0
    max_count = 0
    word = ""
    max_node = trees.trie_node("")
    while (not node.word) and count < 70:
        for child in node.children:
            if max_count <= child.count:
                max_count = child.count
                max_node = child
        word += max_node.letter
        node = max_node
        count += 1
    return word

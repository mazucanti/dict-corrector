import trees


def gen_sugg(root, word: str):
    # if word == '':
    #    return []
    suggestion_list = []
    node = root
    found = trees.search(node, word)
    valid_letters = ''
    if found:
        count = 0
        for letter in word:
            if node.word == True and count == len(word)-1:
                break
            for child in node.children:
                if child.letter == letter:
                    node = child
                    break
            count += 1
        final_word = word + write_sugg(node)
        suggestion_list.append(final_word)
        if final_word != word:
            suggestion_list.append(word)
        return suggestion_list

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
        final_word = valid_letters + write_sugg(node)
        return [final_word]

def is_right(root, word):
    found = trees.search(root, word)

    if found:
        return True, []
    else:
        node = root
        suggestion_list = []
        suggestion = ''
        last_right_word = ''
        for letter in word:
            max_node = trees.trie_node('')
            letter_found = False
            for child in node.children:
                if max_node.count <= child.count:
                    max_node = child
                if child.letter == letter:
                    suggestion += letter
                    node = child
                    letter_found = True
                    break
            if not letter_found:
                suggestion += max_node.letter
                node = max_node
            if node.word == True:
                last_right_word = suggestion
        suggestion_list.append(last_right_word)

        node = root
        valid_letters = ''
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
        final_word = valid_letters + write_sugg(node)

        if final_word != last_right_word:
            suggestion_list.append(final_word)

        return False, suggestion_list


def write_sugg(node):
    count = 0
    max_count = 0
    word = ''
    while 1:
        max_node = trees.trie_node('')
        for child in node.children:
            if max_count <= child.count:
                max_count = child.count
                max_node = child
        word += max_node.letter
        node = max_node
        count += 1
        if node.word or count >= 40:
            break
    if node.word:
        return word
    else:
        return ""

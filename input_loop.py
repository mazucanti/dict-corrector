import curses
import trees, suggest

main_menu_options = {'Start': 0, 'Guide': 1, 'Credits': 2, 'Close': 3}  # Variable that holds the main menu options
exit_options = {'No': 0, 'Yes': 1}  # Variable that hold the exit menu options


def print_loading_screen(stdscr):
    stdscr.clear()

    h, w = stdscr.getmaxyx()
    message = 'Loading trie tree...'

    stdscr.addstr(h//2, w//2 - len(message)//2, message, curses.A_BLINK)

    stdscr.refresh()

def print_menu(stdscr, selected_menu_row):
    stdscr.clear()

    h, w = stdscr.getmaxyx()

    for i, text in enumerate(main_menu_options):
        x = w // 2 - len(text) // 2
        y = h // 2 - len(main_menu_options) // 2 + i
        if i == selected_menu_row:
            stdscr.addstr(y, x, text, curses.color_pair(1))
        else:
            stdscr.addstr(y, x, text)

    stdscr.refresh()


def print_exit_menu(stdscr, exit_cursor, mode):
    stdscr.clear()
    message = 'Are you sure you want to exit the {}?'.format(mode)
    h, w = stdscr.getmaxyx()

    stdscr.addstr(h // 2 - 1, w // 2 - len(message) // 2, message)
    for i, text in enumerate(exit_options):
        x = w // 2 + (-1 + 2 * i) * w // 16 - len(text) // 2
        y = h // 2 + 1
        if i == exit_cursor:
            stdscr.addstr(y, x, text, curses.color_pair(1))
        else:
            stdscr.addstr(y, x, text)

    stdscr.refresh()

''' Shows the exit options and deals with user inputs
    
    Receives a string for a custom message depending on the mode being exited
    Returns False if the user confirms the exit
    Returns True otherwise '''
def exit_routine(stdscr, mode_being_exited):
    exit_cursor_index = 0

    while 1:
        print_exit_menu(stdscr, exit_cursor_index, mode_being_exited)
        key = stdscr.getch()        # Gets user input code

        # Captures left and right arrow inputs and updates the cursor
        if key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
            exit_cursor_index = (exit_cursor_index + 1) % len(exit_options)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if exit_cursor_index == exit_options['No']:
                return True
            else:
                return False


def print_corrector_screen(stdscr, phrase, current_word, current_suggestions, suggestion_cursor, word_cursor):
    stdscr.clear()                                          # Clears the screen

    # Print suggestion window
    h, w = stdscr.getmaxyx()

    if suggestion_cursor != 0:
        stdscr.addstr(h-5, 2, 'Definition of \"'+current_suggestions[suggestion_cursor-1].lower()+'\" at: ', curses.A_BOLD)
        stdscr.addstr(h-4, 2, 'https://www.lexico.com/en/definition/'+current_suggestions[suggestion_cursor-1].lower(), curses.A_UNDERLINE)
    elif word_cursor != 0 and phrase[word_cursor][1] == True:
        stdscr.addstr(h-5, 2, 'Definition of \"'+phrase[word_cursor][0].lower()+'\" at: ', curses.A_BOLD)
        stdscr.addstr(h-4, 2, 'https://www.lexico.com/en/definition/'+phrase[word_cursor][0].lower(), curses.A_UNDERLINE)


    stdscr.move(h-3, 0)
    for i in range(w):
        stdscr.addch('_')

    if current_suggestions != []:
        if suggestion_cursor == 1:
            stdscr.addstr(h - 2, 2, current_suggestions[0], curses.color_pair(1))
        else:
            stdscr.addstr(h - 2, 2, current_suggestions[0])
    if len(current_suggestions) >= 2:
        if suggestion_cursor == 2:
            stdscr.addstr(h - 2, w//2 - len(current_suggestions[1])//2, current_suggestions[1], curses.color_pair(1))
        else:
            stdscr.addstr(h - 2, w // 2 - len(current_suggestions[1]) // 2, current_suggestions[1])
    if len(current_suggestions) >= 3:
        if suggestion_cursor == 3:
            stdscr.addstr(h - 2, w - len(current_suggestions[2]) - 2, current_suggestions[2], curses.color_pair(1))
        else:
            stdscr.addstr(h - 2, w - len(current_suggestions[2]) - 2, current_suggestions[2])

    stdscr.move(0, 0)

    for i, string in enumerate(phrase):
        if i == len(phrase) + word_cursor:
            if string[1] == False:
                stdscr.addstr(string[0], curses.color_pair(3))
            else:
                stdscr.addstr(string[0], curses.color_pair(1))
        elif string[1] == False:
            stdscr.addstr(string[0], curses.color_pair(2))
        else:
            stdscr.addstr(string[0])

    stdscr.addstr(current_word, curses.A_UNDERLINE)         # Prints the word currently being wrote underlined

    stdscr.refresh()                                        # Updates the screen


''' Receives an ASCII code (integer)
    return True if this code translates to a letter
    return False otherwise '''
def is_a_letter(char):
    if char in range(65, 91) or char in range(97, 123):  # (A to Z) and (a to z) ASCII codes
        return True
    else:
        return False

def is_right(root, word):
    return suggest.is_right(root, word)

def autocomplete(root, word_beginning):
    return suggest.gen_sugg(root, word_beginning)

''' '''
def corrector_mode(stdscr, root):
    curses.curs_set(1)      # Turns the cursor visualization on
    unfinished_word = ''    # Variable that holds the word that is currently being wrote
    suggestion_cursor = 0
    word_cursor = 0
    # Phrase is a list of the words already written by the user
    # each of its elements hold another list in the form of
    # ['word', True/False (if False, it means the word was misspelled), [] (a list of possible corrections)
    phrase = []


    while 1:
        if word_cursor == 0:
            current_autocomplete_suggestions = autocomplete(root, unfinished_word.lower())
        else:
            current_autocomplete_suggestions = phrase[word_cursor][2]
        print_corrector_screen(stdscr, phrase, unfinished_word, current_autocomplete_suggestions, suggestion_cursor, word_cursor)

        key = stdscr.getch()    # Gets the code for the key the user pressed (either an ASCII code or a special curses code)

        # This block takes a different action depending on the user input
        # It also implements the usual behavior of special keys

        if key in [263, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 258, 259]:
            None

        elif key == 9: # TAB
            if current_autocomplete_suggestions != []:
                suggestion_cursor = (suggestion_cursor % len(current_autocomplete_suggestions)) + 1

        elif (key == curses.KEY_ENTER or key in [10, 13]) and suggestion_cursor != 0:       # Enter
            if word_cursor == 0:
                unfinished_word = current_autocomplete_suggestions[suggestion_cursor-1]
            else:
                phrase[word_cursor] = [current_autocomplete_suggestions[suggestion_cursor-1], True, []]
            suggestion_cursor = 0
        else:
            suggestion_cursor = 0

            if key == curses.KEY_LEFT:
                if word_cursor == 0 and phrase != [] and is_a_letter((phrase[-1][0][-1])):
                    word_cursor = -1
                elif -(word_cursor - 2) <= len(phrase):
                    word_cursor -= 2
            elif key == curses.KEY_RIGHT:
                if word_cursor < 0:
                    word_cursor += 2

            else:
                word_cursor = 0

                # ESC will be used to exit the mode
                if key == 27:                                           # ESC ASCII code
                    curses.curs_set(0)                                  # Turns off cursor visualization
                    if not exit_routine(stdscr, 'corrector mode'):      # If the user confirms the exit, breaks from the correctors loop
                        break
                    else:
                        curses.curs_set(1)                              # if the user cancels the exit, turns on cursor visualization again

                # Implements backspace/delete functionality
                elif key in [8, 127, 263]:                               # Backspace and Delete ASCII codes
                    if unfinished_word != '':                       # If the user was writing a word
                        unfinished_word = unfinished_word[0:-1]     # Deleted the last character of the unfinished word

                    elif phrase != []:                                                  # Else if there's something to be deleted
                        phrase[-1][0] = phrase[-1][0][:-1]
                        if phrase[-1][0] == '':
                            phrase.pop()
                            if phrase != []:
                                last_word_written = phrase.pop()
                                unfinished_word = last_word_written[0]

                # If the user did not type a letter
                elif not is_a_letter(key):
                    if unfinished_word != '':
                        word_is_correct, suggestions = is_right(root, unfinished_word.lower())
                        phrase.append([unfinished_word, word_is_correct, suggestions])
                        phrase.append([chr(key), True, []])
                        unfinished_word = ''                    # Resets the current word
                    else:
                        if phrase == []:
                            phrase.append(['', True, []])
                        phrase[-1][0] = phrase[-1][0] + chr(key)

                # If the user typed a letter
                else:
                    suggestion_cursor = 0
                    unfinished_word += chr(key)     # Adds if to the word currently being written


def guide(stdscr):
    return True

def credits(stdscr):
    stdscr.clear()
    class_name = 'Algoritmos e Estruturas de Dados II - A1 - 2019.3'
    professor = 'Carlo Kleber da Silva Rodrigues'
    title = 'Dictionary and Text Corrector utilizing Trie Trees'
    students = ['Barbara Dias de Sena', 'Daniel Mazucanti Domingos', 'Pedro Regio Shoji', 'Sergio Pereira Oliveira']
    ra = ['11.2017.21899', '11.2017.21603', '11.2017.21028', '11.2017.21122']
    dictionary = 'Dictionary definitions by \"Lexico\", english online dictionary powered by Oxford'
    dictionary_url = 'https://www.lexico.com/en'

    name_ra = []
    for i in range(len(students)):
        length = 26 - len(students[i])
        length += 13
        name_ra.append(students[i]+length*'_'+ra[i])

    h, w = stdscr.getmaxyx()

    stdscr.addstr(0, w//2 - len(class_name)//2, class_name, curses.A_BOLD)
    stdscr.addstr(h//32 + 1, w//2 - len(title)//2, title)

    stdscr.addstr(h//4, w//2 - len(professor)//2, professor)

    for i in range (len(students)):
        stdscr.addstr(h//2 - len(name_ra)//2 + i, w//2 - len(name_ra[i])//2, name_ra[i])

    stdscr.addstr(h-3, w - len(dictionary) - 2, dictionary)
    stdscr.addstr(h-2, w - len(dictionary_url) - 2, dictionary_url)


    stdscr.refresh()

    stdscr.getch()


''' Enter the right mode depending on the user choice
    
    Receives the user choice
    Returns False if the program should be ended and True otherwise '''
def selected_menu_option(stdscr, user_choice, root):
    if user_choice == main_menu_options['Start']:
        corrector_mode(stdscr, root)
        return True
    elif user_choice == main_menu_options['Guide']:
        guide(stdscr)
        return True
    elif user_choice == main_menu_options['Credits']:
        credits(stdscr)
        return True
    else:
        return exit_routine(stdscr, 'program');

def main(stdscr):
    curses.curs_set(0)  # Makes the cursor invisible
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Initialize a color pair (code, text_color, background_color)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

    print_loading_screen(stdscr)
    root = trees.trie_tree()
    menu_cursor_index = 0

    while (1):
        print_menu(stdscr, menu_cursor_index)

        key = stdscr.getch()  # Gets the user input by ASCII code or special symbols that are translated by the curses library

        if key == curses.KEY_UP:
            menu_cursor_index = (menu_cursor_index - 1) % len(main_menu_options)
        elif key == curses.KEY_DOWN:
            menu_cursor_index = (menu_cursor_index + 1) % len(main_menu_options)
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Some times just curses.KEY_ENTER don't work, I was advised to put these other conditions
            if not selected_menu_option(stdscr, menu_cursor_index, root):
                break


''' This wrapper makes so that some of the terminal properties are changed
    and in case of a program interruption, they are changed back to normal
    
    It also passes as a parameter a "screen" variable
    
    More information at
    https://docs.python.org/3/howto/curses.html#starting-and-ending-a-curses-application'''
curses.wrapper(main)

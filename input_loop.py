import curses

main_menu_options = {'Corrector': 0, 'Dictionary': 1, 'Credits': 2,
                     'Exit': 3}  # Variable that holds the main menu options
exit_options = {'No': 0, 'Yes': 1}  # Variable that hold the exit menu options


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


def print_corrector_screen(stdscr, phrase, current_word):
    stdscr.clear()                                          # Clears the screen

    stdscr.addstr(0, 0, phrase)                             # Prints the old phrase
    stdscr.addstr(current_word, curses.A_UNDERLINE)         # Prints the word currently being wrote underlined
    # stdscr.addstr(current_word, curses.color_pair(1))     # Alternatively prints with a white box around it

    stdscr.refresh()                                        # Updates the screen


''' Receives an ASCII code (integer)
    return True if this code translates to a letter
    return False otherwise '''
def is_a_letter(char):
    if char in range(65, 91) or char in range(97, 123):  # (A to Z) and (a to z) ASCII codes
        return True
    else:
        return False

''' Receives a string ended in letters
    Returns the text until the last word and the last word '''
def split_on_last_word(text):
    i = -1

    # While the current character is a letter and the start of the string was not reached
    while is_a_letter(ord(text[i])) and len(text) + i > 0:
        i -= 1

    # This resolves a problem with the intervals when the split location is in the beginning of the text
    # because text[0:0] = text[0] != ''
    if len(text) + i == 0:
        return '', text
    return text[0:i + 1], text[i + 1:]

''' '''
def corrector_mode(stdscr):
    curses.curs_set(1)      # Turns the cursor visualization on
    unfinished_word = ''    # Variable that holds the word that is currently being wrote
    phrase = ''             # Variable that holds the rest of the text

    while 1:
        print_corrector_screen(stdscr, phrase, unfinished_word)

        key = stdscr.getch()    # Gets the code for the key the user pressed (either an ASCII code or a special curses code)

        # This block takes a different action depending on the user input
        # It also implements the usual behavior of special keys

        # ESC will be used to exit the mode
        if key == 27:                                           # ESC ASCII code
            curses.curs_set(0)                                  # Turns off cursor visualization
            if not exit_routine(stdscr, 'corrector mode'):      # If the user confirms the exit, breaks from the correctors loop
                break
            else:
                curses.curs_set(1)                              # if the user cancels the exit, turns on cursor visualization again

        # Implements backspace/delete functionality
        elif key in [8, 127]:                               # Backspace and Delete ASCII codes
            if unfinished_word != '':                       # If the user was writing a word
                unfinished_word = unfinished_word[0:-1]     # Deleted the last character of the unfinished word

            elif phrase != '':                                                  # Else if there's something to be deleted
                if not (is_a_letter(ord(phrase[-1]))):                          # If the current last character is not a letter
                    phrase = phrase[0:-1]                                       # Just delete it
                    if is_a_letter(ord(phrase[-1])):                            # If the new last character is a letter
                        phrase, unfinished_word = split_on_last_word(phrase)    # Updates the word being wrote and the rest of the text
                else:                                                           # Else if the current last character is a letter
                    unfinished_word = unfinished_word[0:-1]                     # Just delete it

        # If the user did not type a letter
        elif not is_a_letter(key):
            phrase += unfinished_word + chr(key)    # Finishes the word being wrote and updates the text with it
            unfinished_word = ''                    # Resets the current word

        # If the user typed a letter
        else:
            unfinished_word += chr(key)     # Adds if to the word currently being wrote


''' Enter the right mode depending on the user choice
    
    Receives the user choice
    Returns False if the program should be ended and True otherwise '''
def selected_menu_option(stdscr, user_choice):
    if user_choice == main_menu_options['Corrector']:
        corrector_mode(stdscr)
        return True
    elif user_choice == main_menu_options['Dictionary']:
        return True
    elif user_choice == main_menu_options['Credits']:
        return True
    else:
        return exit_routine(stdscr, 'program');

def main(stdscr):
    curses.curs_set(0)  # Makes the cursor invisible
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Initialize a color pair (code, text_color, background_color)

    menu_cursor_index = 0

    while (1):
        print_menu(stdscr, menu_cursor_index)

        key = stdscr.getch()  # Gets the user input by ASCII code or special symbols that are translated by the curses library

        if key == curses.KEY_UP:
            menu_cursor_index = (menu_cursor_index - 1) % len(main_menu_options)
        elif key == curses.KEY_DOWN:
            menu_cursor_index = (menu_cursor_index + 1) % len(main_menu_options)
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Some times just curses.KEY_ENTER don't work, I was advised to put these other conditions
            if not selected_menu_option(stdscr, menu_cursor_index):
                break


''' This wrapper makes so that some of the terminal properties are changed
    and in case of a program interruption, they are changed back to normal
    
    It also passes as a parameter a "screen" variable
    
    More information at
    https://docs.python.org/3/howto/curses.html#starting-and-ending-a-curses-application'''
curses.wrapper(main)

'''
Could be separated in different files

Should change the exiting method (returning false is really scretchy)

There is a strange delay when pressing 'ESC' in corrector mode

Probably the variable phrase (that holds everything the user has already writed and confirmed) should be a dictionary, so that later we can mark it as an spelling error.

Implement a quick guide when entering a mode
'''

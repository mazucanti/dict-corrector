import curses

def main(stdscr):
    while (1):
        key = stdscr.getch()
        stdscr.clear()
        stdscr.addstr(0,0,str(key))
        stdscr.refresh()
curses.wrapper(main)

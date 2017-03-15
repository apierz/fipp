import os
from os import path
import curses
from curses import wrapper

from .context import fipp
from fipp.cv_con import CDLV_con

stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)


def main(stdscr):

    stdscr.clear(); stdscr.refresh()

    content = ["List Item",
                   "List Item",
                   "List Item",
                   "List Item",
                   "List Item",
                   "List Item",
                   "List Item",
                   "List Item",]
    

    dlvcon = CDLV_con(stdscr,
                    content,
                    "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890",
                    "I am a top string")


    dlvcon.refresh_display()

    while True:
        c = stdscr.getch()
        # if c == curses.KEY_RESIZE:
        #     y, x = stdscr.getmaxyx()
        #     stdscr.clear()
        #     cvcon.resize_con(y, x)
            

        if c == curses.KEY_DOWN or c == ord('j'):
            dlvcon.scrolldown_list()
        # elif c == curses.KEY_UP or c == ord('k'):
        #     cvcon.scrollup()
        # elif c == curses.KEY_RIGHT or c == ord('l'):
        #     cvcon.scrollright()
        # elif c == curses.KEY_LEFT or c == ord('h'):
        #     cvcon.scrollleft()

        elif c == ord('q'):
            break  # Exit the while loop


wrapper(main)

#Terminate a curses app
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

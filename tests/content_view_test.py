import os
from os import path
import curses
from curses import wrapper

from .context import fipp
from fipp.cv_con import CCV_con

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

    if path.exists("./tests/index.html"):
        f = open("./tests/index.html", "r")
        if f.mode == 'r':
            content = f.read()
            f.close()



    cvcon = CCV_con(stdscr,
                    content,
                    80,
                    "I am a top string | h scroll position: ",
                    "I am a bottom string")


    cvcon.content_pad.addstr(0,0, "STRING")
    cvcon.content_pad.refresh(0,0, 1,1, 4,4)
    cvcon.refresh_display()

    while True:
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            y, x = stdscr.getmaxyx()
            stdscr.clear()
            cvcon.resize_con(y, x)
            

        if c == curses.KEY_DOWN or c == ord('j'):
            cvcon.scrolldown()
        elif c == curses.KEY_UP or c == ord('k'):
            cvcon.scrollup()
        elif c == ord('q'):
            break  # Exit the while loop


wrapper(main)

#Terminate a curses app
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

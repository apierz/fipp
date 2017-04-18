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

def main(stdscr):

    stdscr.clear(); stdscr.refresh()

    if path.exists("./tests/dfarticle.html"):
        f = open("./tests/dfarticle.html", "r")
        if f.mode == 'r':
            content = f.read()
            f.close()

    cvcon = CCV_con(stdscr,
                    content,
                    200,
                    "I am a top string",
                    "I am a bottom string",
                    scrollbars = True)


    cvcon.refresh_display()

    while True:
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            y, x = stdscr.getmaxyx()
            stdscr.clear()
            cvcon.resize_con()
            

        if c == curses.KEY_DOWN or c == ord('j'):
            cvcon.scrolldown()
        elif c == curses.KEY_UP or c == ord('k'):
            cvcon.scrollup()
        elif c == curses.KEY_RIGHT or c == ord('l'):
            cvcon.scrollright()
        elif c == curses.KEY_LEFT or c == ord('h'):
            cvcon.scrollleft()
        elif c == ord('c'):
            cvcon.change_bar_color('top', 4, 5)
            cvcon.change_bar_color('bottom', 5, 1)
        elif c == ord('e'):
            cvcon.change_content_color(2, 3)

        elif c == ord('q'):
            break  # Exit the while loop


wrapper(main)

#Terminate a curses app
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

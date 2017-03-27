import os
from os import path
import curses
from curses import wrapper

from .context import fipp
from fipp.cv_con import CFLV_con

stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)


def main(stdscr):

    content = ["Singular"]
    content.append('A longer single option')
    stdscr.clear(); stdscr.refresh()

    for x in range (0, 55):
        content.append(["option " + str(x), "choice 1", "choice 2", "choice 3", "choice 4"])


    cflvcon = CFLV_con(stdscr,
                    content,
                    "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890",
                    "I am a top string")

    cflvcon.refresh_display()

    while True:
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            stdscr.clear()
            cflvcon.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            cflvcon.scrolldown_list()
        elif c == curses.KEY_UP or c == ord('k'):
            cflvcon.scrollup_list()
        elif c == curses.KEY_UP or c == ord('c'):
            cflvcon.cycle_options(cflvcon.highlight_pos)
        elif c == curses.KEY_UP or c == ord('e'):
            cflvcon.custom_option(cflvcon.highlight_pos)
        elif c == curses.KEY_UP or c == ord('r'):
            cflvcon.reset_to_default(cflvcon.highlight_pos)
        elif c == ord('1'):
            cflvcon.change_bar_color('top', 4, 5)
            cflvcon.change_bar_color('bottom', 5, 1)
        elif c == ord('2'):
            cflvcon.change_content_color(2, 3)
        elif c == ord('3'):
            cflvcon.change_highlight_color(0, 2)
        elif c == ord('4'):
            cflvcon.change_text_entry_color(1, 5)
        elif c == ord('q'):
            break  # Exit the while loop


wrapper(main)

#Terminate a curses app
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

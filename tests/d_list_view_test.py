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

def main(stdscr):

    stdscr.clear(); stdscr.refresh()

    content = ["List Item 0",
                   "List Item 1",
                   "List Item 2",
                   "List Item 3",
                   "List Item 4",
                   "List Item 5",
                   "List Item 6",
                   "List Item 7",
                   "List Item 8",
                   "List Item 9",
                   "List Item 10",
                   "List Item 1",
                   "List Item 2",
                   "List Item 31234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890",
                   "List Item 4",
                   "List Item 5",
                   "List Item 6",
                   "List Item 7",
                   "List Item 8",
                   "List Item 9",
                   "List Item 10",
                   "List Item 1",
                   "List Item 2",
                   "List Item 3",
                   "List Item 4",
                   "List Item 5",
                   "List Item 6",
                   "List Item 7",
                   "List Item 8",
                   "List Item 9",
                   "List Item 10",
                   "List Item 1",
                   "List Item 2",
                   "List Item 3",
                   "List Item 4",
                   "List Item 5",
                   "List Item 6",
                   "List Item 7",
                   "List Item 8",
                   "List Item 9",
                   "List Item 10",]
    

    dlvcon = CDLV_con(stdscr,
                    content,
                    "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890",
                    "I am a top string")

    dlvcon.add_to_list("added_string")

    for count, item in enumerate(dlvcon.list_items):
        if "0" in item.content_string:
            item.flags[0] = "%"
        if "1" in item.content_string:
            item.flags[1] = "!"
        if "2" in item.content_string:
            item.flags[2] = "-"
        if "3" in item.content_string:
            item.flags[3] = "*"
        if "4" in item.content_string:
            item.flags[4] = "+"
            
    dlvcon.refresh_display()

    while True:
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            stdscr.clear()
            dlvcon.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            dlvcon.scrolldown_list()
        elif c == curses.KEY_UP or c == ord('k'):
            dlvcon.scrollup_list()
        elif c == curses.KEY_UP or c == ord('a'):
            dlvcon.add_to_list("another added list item")
        elif c == curses.KEY_UP or c == ord('i'):
            dlvcon.insert_to_list("inserted list item", dlvcon.highlight_pos)
        elif c == curses.KEY_UP or c == ord('d'):
            dlvcon.delete_from_list(dlvcon.highlight_pos)
        elif c == curses.KEY_UP or c == ord('c'):
            dlvcon.copy_from_list(dlvcon.highlight_pos)
        elif c == curses.KEY_UP or c == ord('p'):
            dlvcon.paste(dlvcon.highlight_pos)
        elif c == curses.KEY_UP or c == ord('e'):
            dlvcon.append_to_list("appended item")
        elif c == ord('1'):
            dlvcon.change_bar_color('top', 4, 5)
            dlvcon.change_bar_color('bottom', 5, 1)
        elif c == ord('2'):
            dlvcon.change_content_color(2, 3)
        elif c == ord('3'):
            dlvcon.change_highlight_color(0, 2)
        elif c == ord('q'):
            break  # Exit the while loop


wrapper(main)

#Terminate a curses app
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

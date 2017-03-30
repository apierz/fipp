import os
from os import path
import curses
from curses import wrapper

from fipp.cv_con import CDLV_con, CFLV_con, CCV_con
from fipp.account import Account

stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)

# def add_account():

def display_item_body(pos,content, content_view):
    content_view.update_content(content)
    content_view.refresh_display()
    
    while True:
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            y, x = stdscr.getmaxyx()
            stdscr.clear()
            content_view.resize_con()
            

        if c == curses.KEY_DOWN or c == ord('j'):
            content_view.scrolldown()
        elif c == curses.KEY_UP or c == ord('k'):
            content_view.scrollup()
        elif c == curses.KEY_RIGHT or c == ord('l'):
            content_view.scrollright()
        elif c == curses.KEY_LEFT or c == ord('h'):
            content_view.scrollleft()
        elif c == ord('n'):
            return 1
        elif c == ord('p'):
            return -1

        elif c == ord('q'):
            break  # Exit the while loop
    return -999


def main(stdscr):

    stdscr.clear(); stdscr.refresh()

    read_pos = None

    uaccount = Account()
    uaccount = uaccount.verify_user_info()
    
    if uaccount is False:
        add_account()

            
    unread_items = uaccount.get_unread_items()

    item_headers = []
    for item in unread_items:
        item_headers.append(item.get_header_string())

    item_list_view = CDLV_con(stdscr, item_headers, "A helpful bottom message", "q:Quit  m:Mark (un)read  s:(un)Star  r:Refresh  l:List feeds")
    content_view = CCV_con(stdscr, "", 80, "A helpful bottom message also", "Commands will go here")

    for pos, item in enumerate(unread_items):
        if item.read is False:
            item_list_view.list_items[pos].flags[1] = "•"
        if item.starred is True:
            item_list_view.list_items[pos].flags[3] = "*"
    
    item_list_view.refresh_display()

    while True:
        for pos, item in enumerate(unread_items):
            if item.read is False:
                item_list_view.list_items[pos].flags[1] = "•"
            if item.read is True:
                item_list_view.list_items[pos].flags[1] = " "

            if item.starred is True:
                item_list_view.list_items[pos].flags[3] = "*"
            if item.starred is False:
                item_list_view.list_items[pos].flags[3] = " "

        item_list_view.refresh_display()
        
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            stdscr.clear()
            item_list_view.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            item_list_view.scrolldown_list()
        elif c == curses.KEY_UP or c == ord('k'):
            item_list_view.scrollup_list()
        elif c == curses.KEY_UP or c == ord('m'):
            read = None
            if unread_items[item_list_view.highlight_pos].read is True:
                read = False
                unread_items[item_list_view.highlight_pos].read = False
            else:
                read = True
                unread_items[item_list_view.highlight_pos].read = True
            uaccount.change_read_status(unread_items[item_list_view.highlight_pos].feed_item_id, read)
        elif c == curses.KEY_UP or c == ord('s'):
            starred = None
            if unread_items[item_list_view.highlight_pos].starred is True:
                starred = False
                unread_items[item_list_view.highlight_pos].starred = False
            else:
                starred = True
                unread_items[item_list_view.highlight_pos].starred = True
            uaccount.change_star_status(unread_items[item_list_view.highlight_pos].feed_item_id, starred)
        elif c == curses.KEY_UP or c == ord('r'):
            unread_items = uaccount.get_unread_items()
            item_headers = []
            for item in unread_items:
                item_headers.append(item.get_header_string())
            item_list_view.update_list_items(item_headers)
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            stdscr.clear(); stdscr.refresh()
            read_pos = item_list_view.highlight_pos
            read_pos += display_item_body(read_pos,
                                          unread_items[item_list_view.highlight_pos].body,
                                          content_view) 

            while read_pos >= 0:
                if read_pos == len(unread_items):
                    read_pos = -1
                else:
                    stdscr.clear(); stdscr.refresh()
                    read_pos += display_item_body(read_pos,
                                                  unread_items[read_pos].body,
                                                  content_view)
            read_pos = 1


        elif c == ord('q'):
            break  # Exit the while loop


wrapper(main)

#Terminate a curses app
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

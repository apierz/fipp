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

def add_account():

    account_view_info = [["Service", "Feed Wrangler", "Feed Bin"], ["Username", " "], ["Password", " "], "Verify Account"]

    account_view = CFLV_con(stdscr, account_view_info,
                                "q:Back  c:Cycle Options  r:Reset to default  e:Edit",
                                "Verify Account Info")
    stdscr.clear()
    stdscr.refresh()
    account_view.refresh_display()

    while True:
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            stdscr.clear()
            account_view.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            account_view.scrolldown_list()
        elif c == curses.KEY_UP or c == ord('k'):
            account_view.scrollup_list()
        elif c == curses.KEY_UP or c == ord('c'):
            account_view.cycle_options(account_view.highlight_pos)
        elif c == curses.KEY_UP or c == ord('e'):
            account_view.custom_option(account_view.highlight_pos)
        elif c == curses.KEY_UP or c == ord('r'):
            account_view.reset_to_default(account_view.highlight_pos)
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            if account_view.highlight_pos == 3:
                new_account = Account(username = account_view.list_items[1].selected_item.rstrip(),
                                    password = account_view.list_items[2].selected_item.rstrip(),
                                    service = account_view.list_items[0].selected_item)
                return new_account

        elif c == ord('q'):
            return False
            break  # Exit the while loop

     

def display_item_body(pos, content, content_view, unread_items):
    content_view.update_content(content)

    content_view.bottom_bar.update_bar(unread_items[pos].feed_title + " - " + \
                                          unread_items[pos].title)
    content_view.refresh_display()
    
    while True:
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            content_view.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            content_view.scrolldown()
        elif c == curses.KEY_UP or c == ord('k'):
            content_view.scrollup()
        elif c == curses.KEY_RIGHT or c == ord('l'):
            content_view.scrollright()
        elif c == curses.KEY_LEFT or c == ord('h'):
            content_view.scrollleft()
        elif c == ord('m'):
            read = None
            if unread_items[pos].read is True:
                read = False
                unread_items[pos].read = False
            else:
                read = True
                unread_items[pos].read = True
            uaccount.change_read_status(unread_items[pos].feed_item_id, read)
        elif c == ord('s'):
            starred = None
            if unread_items[pos].starred is True:
                starred = False
                unread_items[pos].starred = False
            else:
                starred = True
                unread_items[pos].starred = True
            uaccount.change_star_status(unread_items[pos].feed_item_id, starred)
        elif c == ord('n'):
            return 1
        elif c == ord('p'):
            return -1

        elif c == ord('q'):
            break  # Exit the while loop
    return -999

def display_feed_list(account):
    user_feeds = account.feeds
    feed_names = []
    for feed in user_feeds:
        feed_names.append(feed.title)

    feed_list_view = CDLV_con(stdscr, feed_names,
                                 "q:Back  a:Add Feed  d:Remove Feed",
                                 "Subscribed Feeds [" + account.service + "]")

    stdscr.clear()
    stdscr.refresh()

    while True:
        feed_list_view.refresh_display()
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            feed_list_view.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            feed_list_view.scrolldown_list()
        elif c == curses.KEY_UP or c == ord('k'):
            feed_list_view.scrollup_list()
        elif c == ord('a'):
            pass
        elif c == ord('r'):
            pass
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            recent_items = account.get_most_recent(user_feeds[feed_list_view.highlight_pos])
            display_feed_items(recent_items, account)
        elif c == ord('q'):
            break  # Exit the while loop

def display_feed_items(items, account):
    stdscr.clear()
    stdscr.refresh()

    uaccount = account
    read_pos = 0
    read_mod = False
    star_mod = False
    item_headers = []
    for item in items:
        item_headers.append(item.get_header_string())

    item_list_view = CDLV_con(stdscr, item_headers, "q:Back  m:Mark (un)read  s:(un)Star",
                                "A helpful bottom message")

    content_view = CCV_con(stdscr, "", 80, "q:Back  m:Mark (un)read  s:(un)Star  n:Next  p:Prev", "Title, Info, Etc")

    while True:
        unread_count = 0

        for pos, item in enumerate(items):
            if item.read is False:
                item_list_view.list_items[pos].flags[1] = "•"
                unread_count += 1
            if item.read is True:
                item_list_view.list_items[pos].flags[1] = " "

            if item.starred is True:
                item_list_view.list_items[pos].flags[3] = "*"
            if item.starred is False:
                item_list_view.list_items[pos].flags[3] = " "

        if read_mod is True:
            item_list_view.bottom_bar.left_flags[1] = "•"
        if read_mod is False:
            item_list_view.bottom_bar.left_flags[1] = "-"

        if star_mod is True:
            item_list_view.bottom_bar.left_flags[2] = "*"
        if star_mod is False:
            item_list_view.bottom_bar.left_flags[2] = "-"


        titles = []
        for item in items:
            titles.append(item.feed_title)
            
        if len(titles) > 1 and len(set(titles)) > 1:
            bottom_string = str(len(items)) + " starred items from [" + uaccount.service + "]"
        else:
            bottom_string = str(unread_count) + " unread items from [" + items[0].feed_title + "]"
            itemprev = item.feed_title

        item_list_view.bottom_bar.bar_content = bottom_string

        item_list_view.refresh_display()
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            stdscr.clear()
            item_list_view.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            item_list_view.scrolldown_list()
        elif c == curses.KEY_UP or c == ord('k'):
            item_list_view.scrollup_list()
        elif c == ord('m'):
            read = None
            if items[item_list_view.highlight_pos].read is True:
                read = False
                unread_count += 1
                items[item_list_view.highlight_pos].read = False
            else:
                read = True
                unread_count -= 1
                items[item_list_view.highlight_pos].read = True
            read_mod = True
            uaccount.change_read_status(items[item_list_view.highlight_pos].feed_item_id, read)
        elif c == ord('s'):
            starred = None
            if items[item_list_view.highlight_pos].starred is True:
                starred = False
                items[item_list_view.highlight_pos].starred = False
            else:
                starred = True
                items[item_list_view.highlight_pos].starred = True
            star_mod = True
            uaccount.change_star_status(items[item_list_view.highlight_pos].feed_item_id, starred)
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            stdscr.clear(); stdscr.refresh()
            read_pos = item_list_view.highlight_pos
            read_pos += display_item_body(read_pos,
                                          items[item_list_view.highlight_pos].body,
                                          content_view, items)

            while read_pos >= 0:
                if read_pos == len(items):
                    read_pos = -1
                else:
                    stdscr.clear(); stdscr.refresh()
                    read_pos += display_item_body(read_pos,
                                                  items[read_pos].body,
                                                  content_view, items)
            read_pos = 1


        elif c == ord('q'):
            break  # Exit the while loop

def main(stdscr):

    stdscr.clear(); stdscr.refresh()

    read_pos = None
    read_mod = False
    star_mod = False

    uaccount = Account()
    uaccount = uaccount.verify_user_info()


    while uaccount is False:
        uaccount = add_account()

    unread_items = uaccount.get_unread_items()

    item_headers = []
    for item in unread_items:
        item_headers.append(item.get_header_string())

    item_list_view = CDLV_con(stdscr, item_headers, "q:Quit  m:Mark (un)read  s:(un)Star  r:Refresh  l:List feeds  *:Starred items",
                                  "A helpful bottom message")
    content_view = CCV_con(stdscr, "", 80, "q:Back  m:Mark (un)read  s:(un)Star  n:Next  p:Prev", "Title, Info, Etc")

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

        if read_mod is True:
            item_list_view.bottom_bar.left_flags[1] = "•"
        if read_mod is False:
            item_list_view.bottom_bar.left_flags[1] = "-"

        if star_mod is True:
            item_list_view.bottom_bar.left_flags[2] = "*"
        if star_mod is False:
            item_list_view.bottom_bar.left_flags[2] = "-"


        item_list_view.bottom_bar.bar_content = str(len(unread_items)) + \
                                                     " unread items in " + \
                                                     uaccount.service + " account"

        item_list_view.refresh_display()

        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            stdscr.clear()
            item_list_view.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            item_list_view.scrolldown_list()
        elif c == curses.KEY_UP or c == ord('k'):
            item_list_view.scrollup_list()
        elif c == ord('m'):
            read = None
            if unread_items[item_list_view.highlight_pos].read is True:
                read = False
                unread_items[item_list_view.highlight_pos].read = False
            else:
                read = True
                unread_items[item_list_view.highlight_pos].read = True
            read_mod = True
            uaccount.change_read_status(unread_items[item_list_view.highlight_pos].feed_item_id, read)
        elif c == ord('s'):
            starred = None
            if unread_items[item_list_view.highlight_pos].starred is True:
                starred = False
                unread_items[item_list_view.highlight_pos].starred = False
            else:
                starred = True
                unread_items[item_list_view.highlight_pos].starred = True
            star_mod = True
            uaccount.change_star_status(unread_items[item_list_view.highlight_pos].feed_item_id, starred)
        elif c == ord('r'):
            unread_items = uaccount.get_unread_items()
            item_headers = []
            for item in unread_items:
                item_headers.append(item.get_header_string())
            item_list_view.update_list_items(item_headers)
        elif c == ord('l'):
            display_feed_list(uaccount)
        elif c == ord('*'):
            display_feed_items(uaccount.get_starred_items(), uaccount)
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            stdscr.clear(); stdscr.refresh()
            read_pos = item_list_view.highlight_pos
            read_pos += display_item_body(read_pos,
                                          unread_items[item_list_view.highlight_pos].body,
                                          content_view, unread_items)

            while read_pos >= 0:
                if read_pos == len(unread_items):
                    read_pos = -1
                else:
                    stdscr.clear(); stdscr.refresh()
                    read_pos += display_item_body(read_pos,
                                                  unread_items[read_pos].body,
                                                  content_view, unread_items)
            read_pos = 1


        elif c == ord('q'):
            break  # Exit the while loop


wrapper(main)

#Terminate a curses app
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

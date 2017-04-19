import os
from os import path
import time
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

def add_account(account):

    account_view_info = [["Service", "Feed Wrangler", "Feedbin"], ["Username", " "], ["Password", " "], "Verify Account"]

    if account is not False:
        account_view = CFLV_con(stdscr, account_view_info,
                                "q:Back  c:Cycle Options  r:Reset to default  e:Edit",
                                "Verify Account Info", [account.bf_col, account.bb_col], [account.bf_col, account.bb_col],
                                  [account.mf_col, account.mb_col], [account.hf_col, account.hb_col],
                                  [account.tf_col, account.tb_col])
    else:
        account_view = CFLV_con(stdscr, account_view_info,
                                "q:Back  c:Cycle Options  r:Reset to default  e:Edit",
                                "Verify Account Info")
    stdscr.clear()
    stdscr.refresh()
    account_view.refresh_display()
    

    while True:
        update_color(account_view, account)
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

def color_to_num(color):
    if color is "White":
        num = 7
    if color is "Black":
        num = 0
    if color is "Red":
        num = 1
    if color is "Green":
        num = 2
    if color is "Yellow":
        num = 3
    if color is "Blue":
        num = 4
    if color is "Magenta":
        num = 5
    if color is "Cyan":
        num = 6
    return num

def num_to_color(num):
    if num is 7:
        color = "White"
    if num is 0:
        color = "Black"
    if num is 1:
        color = "Red"
    if num is 2:
        color = "Green"
    if num is 3:
        color = "Yellow"
    if num is 4:
        color = "Blue"
    if num is 5:
        color = "Magenta"
    if num is 6:
        color = "Cyan"
    return color

def display_settings(account):
    settings_menu = [["Bar Foreground", "White", "Black", "Red", "Green",
                          "Yellow", "Blue", "Magenta", "Cyan"],
                     ["Bar Background", "Black", "White", "Red", "Green",
                          "Yellow", "Blue", "Magenta", "Cyan"],
                     ["Main Foreground", "Black", "White", "Red", "Green",
                          "Yellow", "Blue", "Magenta", "Cyan"],
                     ["Main Background", "White", "Black", "Red", "Green",
                          "Yellow", "Blue", "Magenta", "Cyan"],
                     ["Highlight Foreground", "White", "Black", "Red", "Green",
                          "Yellow", "Blue", "Magenta", "Cyan"],
                     ["HighLight Background", "Yellow", "White", "Red", "Green",
                          "Yellow", "Blue", "Magenta", "Cyan"],
                     ["Textbox Foreground", "White", "Black", "Red", "Green",
                          "Yellow", "Blue", "Magenta", "Cyan"],
                     ["Textbox Background", "Blue", "Black", "White", "Red",
                          "Green", "Yellow", "Magenta", "Cyan"],
                     ["Scrollbar Foreground", "White", "Black", "Red", "Green",
                          "Yellow", "Blue", "Magenta", "Cyan"],
                     ["Scrollbar Background", "Blue", "Black", "White", "Red",
                          "Green", "Yellow", "Magenta", "Cyan"]]

    settings_view = CFLV_con(stdscr, settings_menu,
                                 "q:Back  c:Cycle Options  r:Reset to default",
                                 "Options",
                                 [account.bf_col, account.bb_col],
                                 [account.bf_col, account.bb_col],
                                 [account.mf_col, account.mb_col],
                                 [account.hf_col, account.hb_col])

    settings_view.list_items[0].selected_item = num_to_color(account.bf_col)
    settings_view.list_items[0].selected_index = settings_view.list_items[0].options.index(num_to_color(account.bf_col))
    settings_view.list_items[1].selected_item = num_to_color(account.bb_col)
    settings_view.list_items[1].selected_index = settings_view.list_items[1].options.index(num_to_color(account.bb_col))
    settings_view.list_items[2].selected_item = num_to_color(account.mf_col)
    settings_view.list_items[2].selected_index = settings_view.list_items[2].options.index(num_to_color(account.mf_col))
    settings_view.list_items[3].selected_item = num_to_color(account.mb_col)
    settings_view.list_items[3].selected_index = settings_view.list_items[3].options.index(num_to_color(account.mb_col))
    settings_view.list_items[4].selected_item = num_to_color(account.hf_col)
    settings_view.list_items[4].selected_index = settings_view.list_items[4].options.index(num_to_color(account.hf_col))
    settings_view.list_items[5].selected_item = num_to_color(account.hb_col)
    settings_view.list_items[5].selected_index = settings_view.list_items[5].options.index(num_to_color(account.hb_col))
    settings_view.list_items[6].selected_item = num_to_color(account.tf_col)
    settings_view.list_items[6].selected_index = settings_view.list_items[6].options.index(num_to_color(account.tf_col))
    settings_view.list_items[7].selected_item = num_to_color(account.tb_col)
    settings_view.list_items[7].selected_index = settings_view.list_items[7].options.index(num_to_color(account.tb_col))
    settings_view.list_items[8].selected_item = num_to_color(account.sf_col)
    settings_view.list_items[8].selected_index = settings_view.list_items[8].options.index(num_to_color(account.sf_col))
    settings_view.list_items[9].selected_item = num_to_color(account.sb_col)
    settings_view.list_items[9].selected_index = settings_view.list_items[9].options.index(num_to_color(account.sb_col))

    stdscr.clear()
    stdscr.refresh()
    settings_view.refresh_display()

    while True:

        if account.color_changed is True:
            update_color(settings_view, account)
        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            stdscr.clear()
            account_view.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            settings_view.scrolldown_list()
        elif c == curses.KEY_UP or c == ord('k'):
            settings_view.scrollup_list()
        elif c == curses.KEY_UP or c == ord('c'):
            settings_view.cycle_options(settings_view.highlight_pos)
            account.color_changed = True
            if settings_view.highlight_pos is 0:
                account.bf_col = color_to_num(settings_view.list_items[0].selected_item)
            if settings_view.highlight_pos is 1:
                account.bb_col = color_to_num(settings_view.list_items[1].selected_item)
            if settings_view.highlight_pos is 2:
                account.mf_col = color_to_num(settings_view.list_items[2].selected_item)
            if settings_view.highlight_pos is 3:
                account.mb_col = color_to_num(settings_view.list_items[3].selected_item)
            if settings_view.highlight_pos is 4:
                account.hf_col = color_to_num(settings_view.list_items[4].selected_item)
            if settings_view.highlight_pos is 5:
                account.hb_col = color_to_num(settings_view.list_items[5].selected_item)
            if settings_view.highlight_pos is 6:
                account.tf_col = color_to_num(settings_view.list_items[6].selected_item)
            if settings_view.highlight_pos is 7:
                account.tb_col = color_to_num(settings_view.list_items[7].selected_item)
            if settings_view.highlight_pos is 8:
                account.sf_col = color_to_num(settings_view.list_items[8].selected_item)
            if settings_view.highlight_pos is 9:
                account.sb_col = color_to_num(settings_view.list_items[9].selected_item)

        elif c == curses.KEY_UP or c == ord('r'):
            settings_view.reset_to_default(settings_view.highlight_pos)
            account.color_changed = True
            if settings_view.highlight_pos is 0:
                account.bf_col = color_to_num(settings_view.list_items[0].selected_item)
            if settings_view.highlight_pos is 1:
                account.bb_col = color_to_num(settings_view.list_items[1].selected_item)
            if settings_view.highlight_pos is 2:
                account.mf_col = color_to_num(settings_view.list_items[2].selected_item)
            if settings_view.highlight_pos is 3:
                account.mb_col = color_to_num(settings_view.list_items[3].selected_item)
            if settings_view.highlight_pos is 4:
                account.hf_col = color_to_num(settings_view.list_items[4].selected_item)
            if settings_view.highlight_pos is 5:
                account.hb_col = color_to_num(settings_view.list_items[5].selected_item)
            if settings_view.highlight_pos is 6:
                account.tf_col = color_to_num(settings_view.list_items[6].selected_item)
            if settings_view.highlight_pos is 7:
                account.tb_col = color_to_num(settings_view.list_items[7].selected_item)
            if settings_view.highlight_pos is 8:
                account.sf_col = color_to_num(settings_view.list_items[7].selected_item)
            if settings_view.highlight_pos is 9:
                account.sb_col = color_to_num(settings_view.list_items[7].selected_item)

        elif c == ord('q'):
            account.save_user_info()
            return False
            break  # Exit the while loop

def display_item_body(pos, content, unread_items, account):
    content_view = CCV_con(stdscr, content, 80, "q:Back  m:Mark (un)read  s:(un)Star  n:Next  p:Prev", "Title, Info, Etc",
                                  [account.bf_col, account.bb_col], [account.bf_col, account.bb_col],
                                  [account.mf_col, account.mb_col], True,
                                  [account.sf_col, account.sb_col])
    content_view.refresh_display()

    content_view.bottom_bar.update_bar(unread_items[pos].get_date_time() + \
                                          unread_items[pos].feed_title + " - " +\
                                          unread_items[pos].title + " by: " +\
                                          unread_items[pos].author)

    #attempt to update read status
    result = account.change_read_status(unread_items[pos].feed_item_id, True)
    error = False

    if type(result) is str:
        old_bottom = content_view.bottom_bar.bar_content
        content_view.bottom_bar.bar_content = result
        content_view.bottom_bar.update_bar()
        error = True
    else:
        unread_items[pos].read = True

    content_view.refresh_display()

    while True:
        if unread_items[pos].read is False:
            content_view.bottom_bar.left_flags[2] = "•"
        if unread_items[pos].read is True:
            content_view.bottom_bar.left_flags[2] = "-"

        if unread_items[pos].starred is True:
            content_view.bottom_bar.left_flags[3] = "*"
        if unread_items[pos].starred is False:
            content_view.bottom_bar.left_flags[3] = "-"

        content_view.bottom_bar.update_bar()

        c = stdscr.getch()

        if error is True:
            content_view.bottom_bar.bar_content = old_bottom
            content_view.bottom_bar.update_bar()
            error = False

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
            account.change_read_status(unread_items[pos].feed_item_id, read)
        elif c == ord('s'):
            starred = None
            if unread_items[pos].starred is True:
                starred = False
                unread_items[pos].starred = False
            else:
                starred = True
                unread_items[pos].starred = True
            account.change_star_status(unread_items[pos].feed_item_id, starred)
        elif c == ord('n'):
            return 1
        elif c == ord('p'):
            return -1

        elif c == ord('q'):
            break  # Exit the while loop
    return -999

def display_feed_list(account):
    error = False
    user_feeds = account.feeds
    feed_names = []
    for feed in user_feeds:
        feed_names.append(feed.title)

    feed_list_view = CDLV_con(stdscr, feed_names,
                                 "q:Back  a:Add Feed  d:Remove Feed",
                                 "Subscribed Feeds [" + account.service + "]",
                                  [account.bf_col, account.bb_col],
                                  [account.bf_col, account.bb_col],
                                  [account.mf_col, account.mb_col],
                                  [account.hf_col, account.hb_col],
                                  [account.tf_col, account.tb_col])

    stdscr.clear()
    stdscr.refresh()

    while True:
        if account.color_changed is True:
            update_color(feed_list_view, account)

        user_feeds = account.feeds
        feed_list_view.refresh_display()
        c = stdscr.getch()

        if error is True:
            feed_list_view.bottom_bar.bar_content = "Subscribed Feeds [" + \
              account.service + "]"
            error = False

        if c == curses.KEY_RESIZE:
            feed_list_view.resize_con()

        if c == curses.KEY_DOWN or c == ord('j'):
            feed_list_view.scrolldown_list()
        elif c == curses.KEY_UP or c == ord('k'):
            feed_list_view.scrollup_list()
        elif c == ord('a'):
            url = feed_list_view.load_text_popup()
            if url != "":
                result = account.add_feed(url)
                if type(result) is str:
                    feed_list_view.bottom_bar.bar_content = result
                    feed_list_view.bottom_bar.update_bar()
                    error = True
                time.sleep(4.0)
                account.load_feeds()
                account = account.verify_user_info()
                user_feeds = account.feeds
                feed_names = []
                for feed in user_feeds:
                    feed_names.append(feed.title)
                feed_list_view.update_list_items(feed_names)
                stdscr.clear()
                stdscr.refresh()
                feed_list_view._adjust_to_changes()
        elif c == ord('d'):
                result = account.remove_feed(str(user_feeds[feed_list_view.highlight_pos].feed_id))
                if type(result) is str:
                    feed_list_view.bottom_bar.bar_content = result
                    feed_list_view.bottom_bar.update_bar()
                    error = True
                time.sleep(2.0)
                account.load_feeds()
                account = account.verify_user_info()
                user_feeds = account.feeds
                feed_names = []
                for feed in user_feeds:
                    feed_names.append(feed.title)
                feed_list_view.update_list_items(feed_names)
                stdscr.clear()
                stdscr.refresh()
                feed_list_view._adjust_to_changes()
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            recent_items = account.get_most_recent(user_feeds[feed_list_view.highlight_pos])
            display_feed_items(recent_items, account)
        elif c == ord('q'):
            break  # Exit the while loop

def display_feed_items(items, account):
    stdscr.clear()
    stdscr.refresh()

    account = account
    read_pos = 0
    read_mod = False
    star_mod = False
    item_headers = []
    for item in items:
        item_headers.append(item.get_header_string())

    item_list_view = CDLV_con(stdscr, item_headers,
                                "q:Back  m:Mark (un)read  s:(un)Star",
                                "A helpful bottom message",
                                  [account.bf_col, account.bb_col],
                                  [account.bf_col, account.bb_col],
                                  [account.mf_col, account.mb_col],
                                  [account.hf_col, account.hb_col],
                                  [account.tf_col, account.tb_col])

    while True:
        unread_count = 0

        if account.color_changed is True:
            update_color(item_list_view, account)

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
            item_list_view.bottom_bar.left_flags[2] = "•"
        if read_mod is False:
            item_list_view.bottom_bar.left_flags[2] = "-"

        if star_mod is True:
            item_list_view.bottom_bar.left_flags[3] = "*"
        if star_mod is False:
            item_list_view.bottom_bar.left_flags[3] = "-"


        titles = []
        for item in items:
            titles.append(item.feed_title)

        if len(titles) > 1 and len(set(titles)) > 1:
            bottom_string = str(len(items)) + " starred items from [" + account.service + "]"
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
            else:
                read = True
                unread_count -= 1
            result = account.change_read_status(items[item_list_view.highlight_pos].feed_item_id, read)
            if type(result) is str:
                    feed_list_view.bottom_bar.bar_content = result
                    feed_list_view.bottom_bar.update_bar()
            else:
                items[item_list_view.highlight_pos].read = read
                read_mod = True
                item_list_view.scrolldown_list()


        elif c == ord('s'):
            starred = None
            if items[item_list_view.highlight_pos].starred is True:
                starred = False
            else:
                starred = True
            result = account.change_star_status(items[item_list_view.highlight_pos].feed_item_id, starred)
            if type(result) is str:
                    feed_list_view.bottom_bar.bar_content = result
                    feed_list_view.bottom_bar.update_bar()
            else:
                items[item_list_view.highlight_pos].starred = starred
                star_mod = True
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            stdscr.clear(); stdscr.refresh()
            read_pos = item_list_view.highlight_pos
            read_pos += display_item_body(read_pos,
                                          items[item_list_view.highlight_pos].body, items, account)

            while read_pos >= 0:
                if read_pos == len(items):
                    read_pos = -1
                else:
                    stdscr.clear(); stdscr.refresh()
                    read_pos += display_item_body(read_pos,
                                                  items[read_pos].body, items, account)
            read_pos = 1


        elif c == ord('q'):
            break  # Exit the while loop

def update_color(view_con, account):
    if account is not False:
        view_con.change_bar_color("top", account.bf_col, account.bb_col)
        view_con.change_bar_color("bottom", account.bf_col, account.bb_col)
        view_con.change_content_color(account.mf_col, account.mb_col)

        if type(view_con) is not CCV_con:
            view_con.change_highlight_color(account.hf_col, account.hb_col)
            view_con.change_text_entry_color(account.tf_col, account.tb_col)

        view_con.color_changed = False

def main(stdscr):

    stdscr.clear(); stdscr.refresh()

    read_pos = None
    read_mod = False
    star_mod = False
    error_flag = False

    account = Account()
    account = account.verify_user_info()

    while account is False:
        account = add_account(account)

    result = unread_items = account.get_unread_items()
    item_headers = []
    if type(result) is str:
        bottom_string = result
        error_flag = True
        item_headers.append("")
    else:
        for item in unread_items:
            item_headers.append(item.get_header_string())

    item_list_view = CDLV_con(stdscr, item_headers,
                                  "q:Quit  m:Mark (un)read  s:(un)Star  r:Refresh  l:List feeds  *:Starred items  o:Options",
                                  "A helpful bottom message",
                                  [account.bf_col, account.bb_col],
                                  [account.bf_col, account.bb_col],
                                  [account.mf_col, account.mb_col],
                                  [account.hf_col, account.hb_col])

    while True:

        if account.color_changed is True:
            update_color(item_list_view, account)

        if error_flag is False:
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
                item_list_view.bottom_bar.left_flags[2] = "•"
            if read_mod is False:
                item_list_view.bottom_bar.left_flags[2] = "-"

            if star_mod is True:
                item_list_view.bottom_bar.left_flags[3] = "*"
            if star_mod is False:
                item_list_view.bottom_bar.left_flags[3] = "-"


        if error_flag is True:
            item_list_view.bottom_bar.bar_content = bottom_string
        else:
            item_list_view.bottom_bar.bar_content = str(len(unread_items)) + \
                                                    " unread items in " + \
                                                    account.service + " account"

        item_list_view.refresh_display()

        c = stdscr.getch()
        item_list_view.bottom_bar.bar_content = str(len(unread_items)) + \
                                                    " unread items in " + \
                                                    account.service + " account"
        if c == curses.KEY_RESIZE:
            stdscr.clear()
            item_list_view.resize_con()
        elif c == ord('r'):
            item_headers = []
            result = unread_items = account.get_unread_items()
            if type(result) is str:
                bottom_string = result
                error_flag = True
                item_headers = [""]
            else:
                for item in unread_items:
                    item_headers.append(item.get_header_string())
                item_list_view.update_list_items(item_headers)
                error_flag = False

            
        elif c == ord('o'):
            display_settings(account)

        elif c == ord('q'):
            account.save_user_info()
            break  # Exit the while loop


        if error_flag is False:
            if c == curses.KEY_DOWN or c == ord('j'):
                item_list_view.scrolldown_list()
            elif c == curses.KEY_UP or c == ord('k'):
                item_list_view.scrollup_list()
            elif c == ord('m'):
                read = None
                if unread_items[item_list_view.highlight_pos].read is True:
                    read = False
                else:
                    read = True
                result = account.change_read_status(unread_items[item_list_view.highlight_pos].feed_item_id, read)
                if type(result) is str:
                    bottom_string = result
                    error_flag = True
                else:
                    unread_items[item_list_view.highlight_pos].read = read
                    read_mod = True
            elif c == ord('s'):
                starred = None
                if unread_items[item_list_view.highlight_pos].starred is True:
                    starred = False
                else:
                    starred = True
                result = account.change_star_status(unread_items[item_list_view.highlight_pos].feed_item_id, starred)
                if type(result) is str:
                    bottom_string = result
                    error_flag = True
                else:
                    unread_items[item_list_view.highlight_pos].starred = starred
                    star_mod = True
            elif c == ord('l'):
                display_feed_list(account)
            elif c == ord('*'):
                display_feed_items(account.get_starred_items(), account)
            elif c == curses.KEY_ENTER or c == 10 or c == 13:
                stdscr.clear(); stdscr.refresh()
                read_pos = item_list_view.highlight_pos
                if len(item_headers) >=1:
                    read_pos += display_item_body(read_pos,
                                            unread_items[item_list_view.highlight_pos].body,
                                                unread_items, account)

                while read_pos >= 0:
                    if read_pos == len(unread_items):
                        read_pos = -1
                    else:
                        stdscr.clear(); stdscr.refresh()
                        read_pos += display_item_body(read_pos,
                                                    unread_items[read_pos].body,
                                                        unread_items, account)
                read_pos = 1



wrapper(main)

#Terminate a curses app
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

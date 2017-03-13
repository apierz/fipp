import datetime
from datetime import date, time, timedelta
import json
from account import Account
import time
import datetime
import urllib
import os
from html.parser import HTMLParser
import curses
from curses import wrapper
import math
import requests


global api_url
api_url = "https://feedwrangler.net/api/v2/"

class MyHTMLParser(HTMLParser):

    # Tag Codes:
    # 1: End of p
    # 2: Start of italic
    # 3: End of italic
    # 4: Start of a
    # 5: end of a
    # 6: start of list item
    # 7: end of list item
    # 8: start of bq
    # 9: end of bq
    #10: start of bold
    #11: end of bold
    #12: start h1
    #13: end h1
    #14: start h2
    #15: end h2
    #16: start h3
    #17: end h3
    #18: start h4
    #19: end h4
    #20: start of OL
    #21: end of OL
    #22: start of UL
    #23: end of UL


    def __init__(self, *, convert_charrefs=True):

        self.content = []
        self.convert_charrefs = convert_charrefs
        self.reset()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.content.append(4)
        if tag == "em" or tag == "i":
            self.content.append(2)
        if tag == "strong" or tag == "b":
            self.content.append(10)
        for name, value in attrs:
            if name == "href":
                if len(value) >= 40:
                    value = goo_shorten_url(value)
                self.content.append("(" + value + ")")
        if tag == "li":
            self.content.append(6)
        if tag == "blockquote":
            self.content.append(8)
        if tag == "h1":
            self.content.append(12)
        if tag == "h2":
            self.content.append(14)
        if tag == "h3":
            self.content.append(16)
        if tag == "h4":
            self.content.append(18)
        if tag == "ol":
            self.content.append(20)
        if tag == "ul":
            self.content.append(22)

    def handle_endtag(self, tag):
        if tag == "p":
            self.content.append(1)
        if tag == "em" or tag == "i":
            self.content.append(3)
        if tag == "a":
            self.content.append(5)
        if tag == "li":
            self.content.append(7)
        if tag == "blockquote":
            self.content.append(9)
        if tag == "strong" or tag == "b":
            self.content.append(11)
        if tag == "h1":
            self.content.append(13)
        if tag == "h2":
            self.content.append(15)
        if tag == "h3":
            self.content.append(17)
        if tag == "h4":
            self.content.append(19)
        if tag == "ol":
            self.content.append(21)
        if tag == "ul":
            self.content.append(23)


    def handle_data(self, data):
        words = data.split()
        for word in words:
            word = word.strip().replace("\t", " ").replace("\n"," ")
            self.content.append(word)


def goo_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyCoMyPAgrC7LEzSMZV0Mr6JxRhp1JZ4yt4'
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    response_data = r.json()
    return response_data['id']


def display_feed_body(feed_item):

    f = open("raw.txt","w")
    f.write(feed_item.body)
    f.close()

    parser = MyHTMLParser()
    parser.feed(feed_item.body)
    content = parser.content

    stdscr.clear()
    stdscr.refresh()

    pad_range = 0
    if len(content) >= curses.LINES:
        pad_range = len(content)
    else:
        pad_range = curses.LINES

    pad = curses.newpad(pad_range, curses.COLS)
    top_pad = curses.newpad(1, curses.COLS + 4)
    bottom_pad = curses.newpad(1, curses.COLS + 4)

    line = 0
    top_string = "q:Back  m:Mark (un)read  s:(un)Star  n:Next  p:Prev"
    top_string+=get_filler_string(top_string)
    top_pad.addstr(0, 0, top_string)

    title_string1 = feed_item.feed_name
    title_string2 = feed_item.title

    bottom_string = "-"
    if feed_item.starred == True:
        bottom_string += "*"
    else:
        bottom_string+= "-"

    bottom_string+= " " + title_string1 + " - " + title_string2

    while len(bottom_string) >= curses.COLS - 6:
        bottom_string = bottom_string[:-2]
        bottom_string += "…"

    for x in range(0,pad_range-1):
        pad.addstr(x,0, get_filler_string(), curses.A_REVERSE)

    gap = " "
    margin = ""
    if curses.COLS <= 80:
        width = curses.COLS
    else:
        width = 80
    text_line = ""
    ordered_list = False
    list_counter = 1
    for piece in content:
        if content:
            if piece == 2:
                text_line += " *"
                gap = ""
            if piece == 8:
                margin = "    "
                text_line = margin
            if piece == 9:
                margin = ""
                text_line = margin
            if piece == 10:
                text_line += " **"
                gap = ""
            if piece == 12:
                text_line = "# "
            if piece == 14:
                text_line = "## "
            if piece == 16:
                text_line = "### "
            if piece == 18:
                text_line = "#### "
            if piece == 20:
                ordered_list = True
            if piece == 22:
                ordered_list = False
            if isinstance(piece, str):
                if len(piece) + len(gap) + len(text_line) + len(margin) > width:
                    pad.addstr(line,0, text_line, curses.A_REVERSE)
                    text_line = margin
                    line+=1
                if gap == " " and piece in (",",".","!","?","\"","\'"):
                    gap = ""
                if len(text_line) + len(gap) + len(piece) + len(margin) <= width:
                    text_line = text_line + gap + piece
                    if gap == "":
                        gap = " "
            if piece == 1:
                pad.addstr(line,0, text_line, curses.A_REVERSE)
                text_line = margin
                line+=2
            if piece == 3:
                text_line += "*"
            if piece == 6:
                if ordered_list == True:
                    text_line+= str(list_counter)+". "
                    list_counter+=1
                if ordered_list == False:
                    text_line += "* "
            if piece == 7:
                pad.addstr(line,0, text_line, curses.A_REVERSE)
                text_line = margin
                line+=1
            if piece == 11:
                text_line += "**"
            if piece in (13,15,17,19):
                pad.addstr(line,0, text_line, curses.A_REVERSE)
                text_line = margin
                line+=2
            if piece == 21:
                list_counter == 1

    bottom_string+=get_filler_string(bottom_string)
    if line >= curses.LINES -2:
        bottom_string = bottom_string[:-2]
        bottom_string+= "↓ "
    bottom_pad.addstr(0, 0, bottom_string)

    top_pad.refresh(0,0, 0,0, 0, curses.COLS-1)
    pad.refresh(0,0, 1,0, curses.LINES - 1, curses.COLS)
    bottom_pad.refresh(0, 0, curses.LINES-1, 0, curses.LINES-1, curses.COLS -1)

    feed_item.read=True
    feed_item.update_read_status(True)

    pad_pos = 1
    scroll_counter = 0
    while True:
        c = stdscr.getch()
        if c == curses.KEY_DOWN or c == ord('j'):
            if  line >= curses.LINES-3 and pad_pos < line - curses.LINES + 2:
                pad_pos+=1
                pad.refresh(pad_pos,0, 1,0, curses.LINES -2, curses.COLS-2)
                if pad_pos > 0:
                    top_string = top_string[:-2]
                    top_string+= "↑ "
                    top_pad.addstr(0,0, top_string)
                    top_pad.refresh(0,0, 0,0, 0, curses.COLS-1)
            if pad_pos == line - curses.LINES+2:
                bottom_string = bottom_string[:-2]
                bottom_string+= "  "
                bottom_pad.addstr(0,0, bottom_string)
                bottom_pad.refresh(0, 0, curses.LINES-1, 0, curses.LINES-1, curses.COLS -1)
        elif c == curses.KEY_UP or c == ord('k'):
            if pad_pos>0:
                pad_pos-=1
                pad.refresh(pad_pos,0, 1,0, curses.LINES -2, curses.COLS-2)
            if pad_pos == 0:
                    top_string = top_string[:-2]
                    top_string+= "  "
                    top_pad.addstr(0,0, top_string)
                    top_pad.refresh(0,0, 0,0, 0, curses.COLS-1)
            if pad_pos == line - curses.LINES+1:
                bottom_string = bottom_string[:-2]
                bottom_string+= "↓ "
                bottom_pad.addstr(0,0, bottom_string)
                bottom_pad.refresh(0, 0, curses.LINES-1, 0, curses.LINES-1, curses.COLS -1)
        elif c == ord('n') :
            return 1
        elif c==ord('p'):
            if feed_item.item_count != 1:
                return -1
        elif c == ord('m'):
            status = False
            bottom_string=bottom_string[1:]
            if feed_item.read == False:
                status = True
                bottom_string = "-" + bottom_string
            else:
                bottom_string = "•" + bottom_string
            feed_item.read = status
            feed_item.update_read_status(status)
            bottom_pad.addstr(0,0, bottom_string)
            bottom_pad.refresh(0, 0, curses.LINES-1, 0, curses.LINES-1, curses.COLS -1)
        elif c == ord('s'):
            first_char = bottom_string[:1]
            bottom_string=bottom_string[2:]
            status = False
            if feed_item.starred == False:
                status = True
                second_char = "*"
            else:
                second_char = "-"
            feed_item.starred = status
            feed_item.update_starred_status(status)
            bottom_string = first_char + second_char + bottom_string
            bottom_pad.addstr(0,0, bottom_string)
            bottom_pad.refresh(0, 0, curses.LINES-1, 0, curses.LINES-1, curses.COLS -1)

        elif c == ord('q'):
            break  # Exit the while loop
    return -999


class FeedItem():
    def __init__(self, title, body, pub_date, read, starred,
                     feed_item_id, url, author, feed_id, feed_name,
                     updated_at, item_count, account):
        self.title = title.strip().replace("\t", "").replace("\n","")
        self.body = body
        self.pub_date = pub_date
        self.read = read
        self.starred = starred
        self.feed_item_id = feed_item_id
        self.url = url
        self.author = author
        self.feed_id = feed_id
        self.feed_name = feed_name.strip().replace("\t", "").replace("\n","")
        self.updated_at = updated_at
        self.item_count = item_count
        self.account = account

    def get_header_string(self):
        header_string = ""
        if self.read == False:
            header_string += " •"
        else:
            header_string += "  "

        if self.starred == True:
            header_string += " * "
        else:
            header_string += "   "

        header_string += format_date(self.pub_date)

        short_name = (self.feed_name[:21] + '…') if len(self.feed_name) > 21 else self.feed_name

        while len(short_name) <= 22:
            short_name += " "

        header_string += short_name

        short_title = self.title

        while len(short_title + short_name) +5 + 5 >= curses.COLS - 2:
            short_title = short_title[:-2]
            short_title += "…"

        header_string += short_title

        return header_string

    def get_parsed_body(self):
        parser = MyHTMLParser()
        parser.feed(self.body)

    def update_read_status(self, status):
        response = urllib.request.urlopen("https://feedwrangler.net/api/v2/feed_items/update?access_token=" +
            self.account.access_token + "&feed_item_id=" +
            str(self.feed_item_id) + "&read=" +
            str(status).lower()).read()
        data = json.loads(response.decode())

    def update_starred_status(self, status):
        response = urllib.request.urlopen("https://feedwrangler.net/api/v2/feed_items/update?access_token=" +
            self.account.access_token + "&feed_item_id=" +
            str(self.feed_item_id) + "&starred=" +
            str(status).lower()).read()
        data = json.loads(response.decode())

def get_filler_string(str=""):
    filler_string = ""
    while len(str) + len(filler_string) < curses.COLS:
        filler_string+= " "
    return filler_string

def update_feed_display(feed_items, pad, pad_pos,
                            scroll_counter, feed_filter=None):
    unread_count=0

    for x in range(1, len(feed_items)):

        header_string=feed_items[str(x)].get_header_string()
        header_string+=get_filler_string(header_string)

        if len(feed_items) > curses.LINES -2 and \
          pad_pos + 2 != len(feed_items) and \
          curses.LINES - 2 + scroll_counter ==x:
            header_string = header_string[:-1]
            header_string+="↓"

        if scroll_counter > 0 and x-1==scroll_counter:
            header_string = header_string[:-1]
            header_string+="↑"

        if feed_items[str(x)].read == False:
            unread_count+=1

        if pad_pos == x -1:
            pad.addstr(x, 0, header_string, curses.color_pair(1))
        else:
            pad.addstr(x, 0, header_string, curses.A_REVERSE)

        get_filler_string()

    for z in range(len(feed_items) - 1, curses.LINES - 1):
        pad.addstr(z, 0, get_filler_string(), curses.A_REVERSE)

    helper_string = "q:Quit  m:Mark (un)read  s:(un)Star  r:Refresh  l:List feeds"
    helper_string+=get_filler_string(helper_string)
    pad.addstr(scroll_counter,0, helper_string)

    bottom_string ="-"
    if unread_count < len(feed_items) - 1:
        bottom_string+= "*"
    else:
        bottom_string+= "-"

    bottom_string+="Unread Items: " + str(unread_count) + " "
    if feed_filter == None:
        if feed_items["1"]:
            bottom_string+= "| " + feed_items["1"].account.client
        else:
            bottom_string+= "No Unread Items"

    pad.addstr(curses.LINES + scroll_counter - 1,0, bottom_string)
    for y in range(0, curses.COLS - len(bottom_string)):
        pad.addstr(" ")

    pad.refresh(scroll_counter,0, 0,0, curses.LINES - 1, curses.COLS)

def format_date(date_int):
    t1=time.localtime(date_int)
    t2=time.localtime()

    if t1.tm_mday == t2.tm_mday and t1.tm_mon == t2.tm_mon and t1.tm_year == t2.tm_year:
        hour_string = str(t1.tm_hour)
        if t1.tm_hour < 10:
            hour_string = ' ' + hour_string

        min_string = str(t1.tm_min)
        if t1.tm_min < 10:
            min_string = "0" + min_string
        return str(hour_string)+":"+min_string + " "
    else:
        date_string=""
        if t1.tm_mon < 10:
            date_string+=" "

        date_string+=str(t1.tm_mon) + "/" + str(t1.tm_mday)

        while len(date_string) < 6:
            date_string += " "
        return date_string

def load_unread_feeds(user_account):
    response = urllib.request.urlopen("https://feedwrangler.net/api/v2/feed_items/list?access_token=" + user_account.access_token + "&read=false").read()
    data = json.loads(response.decode())

    unread_feed_items = {}
    item_count = 1
    for item in data['feed_items']:
        unread_feed_items[str(item_count)] = FeedItem(item['title'],
                                                      item['body'],
                                                      item['published_at'],
                                                      item['read'],
                                                      item['starred'],
                                                      item['feed_item_id'],
                                                      item['url'],
                                                      item['author'],
                                                      item['feed_id'],
                                                      item['feed_name'],
                                                      item['updated_at'],
                                                      item_count,
                                                      user_account)
        item_count+=1

    return unread_feed_items

user_account = Account()
stdscr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
# resize = curses.is_term_resized(y,x)

def main(stdscr):

    stdscr.clear(); stdscr.refresh()
    feed_items = load_unread_feeds(user_account)

    pad_pos = 0
    if len(feed_items) < 1000:
        height = 1000
    else:
        height = len(feed_items)

    pad = curses.newpad(height, curses.COLS)
    scroll_counter = 0
    scroll_buffer = 2

    while True:
        update_feed_display(feed_items, pad, pad_pos, scroll_counter)
        stdscr.refresh()

        c = stdscr.getch()
        if c == curses.KEY_RESIZE:
            y,x = stdscr.getmaxyx()
            stdscr.clear()
            curses.resizeterm(y, x)
            stdscr.refresh()
            update_feed_display(feed_items, pad, pad_pos)
        if c == curses.KEY_DOWN or c == ord('j'):
            if pad_pos >= curses.LINES - 3 and pad_pos  < len(feed_items) - 3:
                scroll_counter+=1
            if pad_pos + 1 < len(feed_items) - scroll_buffer:
                pad_pos += 1
                update_feed_display(feed_items, pad, pad_pos, scroll_counter)
            else:
                o=p=0
        elif c == curses.KEY_UP or c == ord('k'):
            if scroll_counter >=1 and pad_pos >= scroll_counter :
                scroll_counter-=1
            if pad_pos > 0:
                pad_pos -= 1
                update_feed_display(feed_items, pad, pad_pos, scroll_counter)
            else:
                o=p=0
        elif c == ord('r'):
            feed_items = load_unread_feeds(user_account)
            pad_pos = 0
            scroll_counter = 0
            update_feed_display(feed_items, pad, pad_pos, scroll_counter)
        elif c == ord('m'):
            status = False
            feed_item = feed_items[str(pad_pos + 1)]
            if feed_item.read == False:
                status = True
            feed_item.read = status
            feed_item.update_read_status(status)
            update_feed_display(feed_items, pad, pad_pos, scroll_counter)
        elif c == ord('s'):
            status = False
            feed_item = feed_items[str(pad_pos + 1)]
            if feed_item.starred == False:
                status = True
            feed_item.starred = status
            feed_item.update_starred_status(status)
            update_feed_display(feed_items, pad, pad_pos, scroll_counter)
        elif c == ord('q'):
            break  # Exit the while loop
        elif c == curses.KEY_HOME:
            x = y = 0
        elif c == curses.KEY_ENTER or c == 10 or c == 13:
            stdscr.clear(); stdscr.refresh()
            pad_pos += display_feed_body(feed_items[str(pad_pos + 1)])

            while pad_pos >= 0:
                if feed_items[str(pad_pos +1)].item_count == len(feed_items):
                    pad_pos = -1
                else:
                    stdscr.clear(); stdscr.refresh()
                    pad_pos += display_feed_body(feed_items[str(pad_pos + 1)])
            pad_pos = 1

wrapper(main)

#Terminate a curses app
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

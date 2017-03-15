import curses
from html.parser import HTMLParser
import requests
import json

class CV_bar():
    def __init__(self, content_string, location):
        self.bar_content = content_string
        self.pad = curses.newpad(1, curses.COLS)
        self.left_flags = [" ", " "]
        self.right_flags = [" ", " "]
        self.width = curses.COLS + 1
        self.location = location
        self.trun_content()

    def _get_filler_string_tb(self, str=""):
        filler_string = ""
        while len(str) + len(filler_string) < curses.COLS - 2:
            filler_string+= " "
        return filler_string


    def update_bar(self):
        self.pad.move(0,0)
        self.pad.clrtoeol()
        self.pad.move(0,0)
        self.trun_content()

        bar_string = self.left_flags[0] + self.left_flags[1] + " " + self.bar_content + self._get_filler_string_tb(self.bar_content + "      ") + " " + self.right_flags[0] + self.right_flags[1]

        
        self.pad.addstr(0,0, bar_string)

        if self.location == "top":
            self.pad.refresh(0,0, 0,0, 0,self.width)
        if self.location == "bottom":
            self.pad.refresh(0,0, curses.LINES-1,0,
                                    curses.LINES-1,self.width)

    def trun_content(self):
        if len(self.bar_content) + 6 > curses.COLS -2:
            while len(self.bar_content) + 6 > curses.COLS -2:
                self.bar_content = self.bar_content[:-1]
            self.bar_content+="…"
            

class CCV_con():
    # Curses Content View Controller
    def __init__(self, stdscr, content, content_width, top_string, bottom_string):
        
        self.bottom_bar = CV_bar(bottom_string, "bottom")
        self.top_bar = CV_bar(top_string, "top")
        self.content = content
        self.v_scroll_position = 0
        self.h_scroll_position = 0
        self.stdscr = stdscr
        self.width = curses.COLS
        self.content_width = content_width
        self.padding_width = content_width + curses.COLS
        self.content_lines = 0
        self.table_holder = []

        lines = curses.LINES if int(len(content))+1 <= curses.LINES else int(len(content))+1
        self.content_pad = curses.newpad(lines, self.padding_width )

        filler_string = self._get_filler_string_content()
        for x in range (0,lines):
            self.content_pad.addstr(x, 0, filler_string, curses.A_REVERSE)

        
    def resize_con(self, y, x):
        self.width = x
        curses.resizeterm(y, x)
        self.refresh_display
        self.stdscr.refresh()

    def refresh_display(self):
        self.stdscr.clear()
        self.stdscr.refresh()

        self.scroll_ind_check()
        self.top_bar.update_bar()
        self.bottom_bar.update_bar()
        
        self._string_content_handler()

        self.content_pad.refresh(0,0, 1,0, curses.LINES-2, curses.COLS - 1)

    def _string_content_handler(self):
        if "</html>" in self.content or "<html>" in self.content:
                parser = MyHTMLParser()
                parser.feed(self.content)
                parsed_string = parser.content

        else:
            parsed_string = []
            string_split_lines = self.content.splitlines()

            for line in string_split_lines:
                strings = line.split()
                for string in strings:
                    parsed_string.append(string)
                    parsed_string.append(" ")
                parsed_string.append(66)

        self._parsed_list_content_handler(parsed_string)
        

    def _parsed_list_content_handler(self, plist):
        line = 0
        width = self.content_width
        gap = ""
        margin = ""
        text_line = ""
        first_half = ""
        ordered_list = False
        list_counter = 1

        for count, piece in enumerate(plist):
            first_half = ""

            if piece:
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
                    text_line = "     # "
                if piece == 14:
                    text_line = "    ## "
                if piece == 16:
                    text_line = "   ### "
                if piece == 18:
                    text_line = "  #### "
                if piece == 24:
                    text_line = " ##### "
                if piece == 26:
                    text_line = "###### "
                if piece == 20:
                    ordered_list = True
                if piece == 22:
                    ordered_list = False
                if piece == 29:
                    text_line += " __"
                    gap = ""
                if piece == 31:
                    text_line += " `"
                    gap = ""
                if piece == 33:
                    text_line += " ~~"
                    gap = ""
                if piece == 38:
                    self.table_holder = plist
                    table_size = self._handle_table(count,line)
                    line+=table_size
                    for z, data in enumerate(plist[count:]):
                        if data == 40:
                            break
                        else:
                            del plist[z]
                if isinstance(piece, str):
                    if len(piece) > width:
                        while len(first_half) + len(text_line) +len(gap) + len(margin) < width:
                            first_half+=piece[:1]
                            piece = piece[1:]
                        plist.insert(count+1, piece)
                        piece = first_half
                            
                    if len(piece) + len(gap) + len(text_line) + len(margin) > width:
                        self.content_pad.addstr(line,0, text_line, curses.A_REVERSE)
                        text_line = margin
                        gap = ""
                        line+=1
                    if gap == " " and piece in (",",".","!","?","\"","\'", "*"):
                        gap = ""
                    if len(text_line) + len(gap) + len(piece) + len(margin) <= width:
                        text_line = text_line + gap + piece
                        if gap == "":
                            gap = " "
                if piece == 1:
                    self.content_pad.addstr(line,0, text_line, curses.A_REVERSE)
                    text_line = margin
                    line+=2
                    gap = ""
                if piece == 3:
                    text_line += "*"
                if piece == 6:
                    if ordered_list == True:
                        text_line+= str(list_counter)+". "
                        list_counter+=1
                    if ordered_list == False:
                        text_line += "* "
                if piece == 7:
                    self.content_pad.addstr(line,0, text_line, curses.A_REVERSE)
                    text_line = margin
                    gap = ""
                    line+=1
                if piece == 11:
                    text_line += "**"
                if piece in (13,15,17,19,25,27):
                    self.content_pad.addstr(line,0, text_line, curses.A_REVERSE)
                    gap = ""
                    text_line = margin
                    line+=2
                if piece == 21:
                    list_counter == 1
                    line+=1
                if piece == 23:
                    line+=1
                if piece == 30:
                    text_line += "__"
                if piece == 34:
                    text_line += "~~"
                if piece == 36:
                    line+=1
                    gap=""
                if piece == 66:
                    self.content_pad.addstr(line,0, text_line, curses.A_REVERSE)
                    gap = ""
                    text_line = margin
                    line+=1

        self.content_lines = line
        self.scroll_ind_check()
        self.bottom_bar.update_bar()

    def scroll_ind_check(self):
            con1 = self.v_scroll_position < self.content_lines + curses.LINES -2
            con2 = self.content_lines > curses.LINES-2

            if con1 and con2:
                self.bottom_bar.right_flags[0] = "↓"

            if self.v_scroll_position == self.content_lines - curses.LINES + 2:
                self.bottom_bar.right_flags[0] = " "

            if self.v_scroll_position > 0:
                self.top_bar.right_flags[0] = "↑"

            if self.v_scroll_position <= 0:
                self.top_bar.right_flags[0] = " "

            if self.h_scroll_position > 0:
                self.bottom_bar.left_flags[1] = "←"

            if self.h_scroll_position == 0:
                self.bottom_bar.left_flags[1] = " "

            con3 = self.h_scroll_position != self.content_width - curses.COLS
            con4 = self.content_width > curses.COLS

            if con3 and con4:
                self.bottom_bar.right_flags[1] = "→"

            if self.h_scroll_position == self.content_width - curses.COLS:
                self.bottom_bar.right_flags[1] = " "

    def scrollup(self):
        if self.v_scroll_position >0:
            self.v_scroll_position-=1
            self.content_pad.refresh(self.v_scroll_position, self.h_scroll_position,
                                         1, 0,
                                         curses.LINES -2, curses.COLS - 1)

            self.scroll_ind_check()
            self.top_bar.update_bar()
            self.bottom_bar.update_bar()

    def scrolldown(self):
        if self.v_scroll_position < self.content_lines - curses.LINES+2:
            self.v_scroll_position+=1
            self.content_pad.refresh(self.v_scroll_position, self.h_scroll_position,
                                         1, 0,
                                         curses.LINES -2, curses.COLS - 1)

            self.scroll_ind_check()
            self.top_bar.update_bar()
            self.bottom_bar.update_bar()

    def scrollright(self):
        if self.h_scroll_position < self.content_width - curses.COLS:
            self.h_scroll_position+=1
            self.content_pad.refresh(self.v_scroll_position, self.h_scroll_position,
                                         1, 0,
                                         curses.LINES -2, curses.COLS - 1)

            self.scroll_ind_check()
            self.top_bar.update_bar()
            self.bottom_bar.update_bar()


    def scrollleft(self):
        if self.h_scroll_position != 0:
            self.h_scroll_position-=1
            self.content_pad.refresh(self.v_scroll_position, self.h_scroll_position,
                                         1, 0,
                                         curses.LINES -2, curses.COLS - 1)

            self.scroll_ind_check()
            self.top_bar.update_bar()
            self.bottom_bar.update_bar()

    def _get_filler_string_content(self, str=""):
        filler_string = ""
        y, x = self.content_pad.getmaxyx()
        for i in range(1, x):
            filler_string+=" "
        
        return filler_string


    def _handle_table(self, count, line):
        x = 0
        y = 0
        table_row_count = 0
        row = []
        rows = []
        row_string = ""
        base_string = ""
        while self.table_holder[x] != 40:
            x+=1

        table_slice = self.table_holder[count:x]
        data_list = []
        
        for data in table_slice:
            if type(data) is str:
                data_list.append(data)
        max_length = len(max(data_list,key=len)) + 3

                             
        for cell in table_slice:
            if cell == 41:
                rows.append(row)
                row = []
            if type(cell) is str:
                row.append(cell)


        for row_data in rows:
            row_data_string = "|"
            for data in row_data:
                while len(data) < max_length:
                    data = " " + data + " "
                if len(data)%2 != 0:
                    data=data[1:]
                data += "|"
                row_data_string += data
            self.content_pad.addstr(line,0, row_data_string, curses.A_REVERSE)
            line+=1
            while len(base_string)< len(row_data_string):
                base_string+="-"
            self.content_pad.addstr(line,0,base_string, curses.A_REVERSE)
            line+=1
            table_row_count+=1

        return (table_row_count * 2) + 1
                
        

    def goo_shorten_url(self, url):
        post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyCoMyPAgrC7LEzSMZV0Mr6JxRhp1JZ4yt4'
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post(post_url, data=json.dumps(payload), headers=headers)
        response_data = r.json()
        return response_data['id']

# class cdlv_list_item():
#     def __init__(self, content_string):
#         self.content_string = content_string
#         self.flags = [" ", " ", " ", " ", " "]

#     def trun_string(self, string):
#         if len(self.string) + 6 > curses.COLS -2:
#             while len(self.string) + 6 > curses.COLS -2:
#                 self.string = self.string[:-1]
#         self.string+="…"
#         return string

#     def fill_list_string(self, list_string = ""):
#         y, x = self.content_pad.getmaxyx()
#         for i in range(1, x):
#             list_string+=" "
#         return list_string

#     def get_list_string(self):
#         flag_string = ""
#         for flag in flags:
#             flag_string+=flag[0]
#         list_string = self.trun_string(flag_string + self.content_string)
#         return self.fill_list_string(list_string)
        

# class cdlv_con():
#     #Curses Dynamic List View Controller
#     def __init__(self, stdscr, list_items, bottom_string, top_string, width):
#         self.stdscr = stdscr
#         self.bottom_bar = CV_bar(bottom_string, "bottom")
#         self.top_bar = CV_bar(top_string, "top")
#         self.list_items = []
#         for item in list_items:
#             self.list_items.append(cdlv_list_item(item))
        
#         self.v_scroll_pos = 0
#         self.highlight_pos = 0
#         self.width = curses.COLS
#         self.padding_width = curses.COLS + 4

#         lines = curses.LINES if int(len(self.feed_items))+1 <= curses.LINES else int(len(self.feed_items))+1
        
#         self.content_pad = curses.newpad(lines, self.padding_width)

#     def refresh_display(self):
#         for count, item in enumerate(self.list_items):

#             text = item.get_list_string()
            
#             if self.highlight_pos == count:
#                 pad.addstr(x, 0, text, curses.color_pair(1))
#             if self.highlight_pos != count:
#                 pad.addstr(x, 0, text, curses.A_REVERSE)

#         for z in range(len(self.list_items) - 1, curses.LINES - 2):
#             pad.addstr(z, 0, self.fill_list_string(), curses.A_REVERSE)

#         self.content

#     # def scrollup_list(self):

#     # def scrolldown_list(self):
    
# class cflv_con(cv_con):
    #Curses Fixed List View Controller

    
class MyHTMLParser(HTMLParser):
    #HTMLParser, turns and html string into Markdown formatted plain-text

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
    #66: /n in plain text content
    #25: start h5
    #26: end h5
    #27: start h6
    #28: end h6
    #29: start of unarticulated
    #30: end of unarticulated
    #31: start of code
    #32: end of code
    #33: start of strikethrough
    #34: end of strikethrough
    #35: start of img
    #36: end of img
    #37: start of table
    #38: start of table row
    #39: start of table data
    #40: end of table 
    #41: end of table row
    #42: end of table data
    #43: start of caption
    #44: end of caption
    #45: start of inline quote
    #46: end of inline quote

    def __init__(self, *, convert_charrefs=True):

        self.content = []
        self.link_data = ""
        self.convert_charrefs = convert_charrefs
        self.reset()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.content.append(4)
        if tag == "em" or tag == "i":
            self.content.append(2)
        if tag == "strong" or tag == "b":
            self.content.append(10)
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
        if tag == "h5":
            self.content.append(24)
        if tag == "h6":
            self.content.append(26)
        if tag == "u":
            self.content.append(29)
        if tag == "code":
            self.content.append(31)
        if tag == "s":
            self.content.append(33)
        if tag == "del":
            self.content.append(33)
        if tag == "ins":
            self.content.append(29)
        if tag == "table":
            self.content.append(37)
        if tag == "tr":
            self.content.append(38)
        if tag == "td" or tag == "th":
            self.content.append(39)
        if tag == "caption":
            self.content.append(43)
        if tag == "q":
            self.content.append(45)
        for name, value in attrs:
            if name == "href":
                self.content.append("(" + value + ")")
            if name == "src":
                self.content.append("![" + value + "]")
                self.content.append(36)
            if name == "alt":
                self.content.append("(Imagine a picture of a(n) " + value + ")")
                self.content.append(36)
            if name == "cite":
                self.content.append("[" + value + "]")

    def handle_endtag(self, tag):
        if tag == "p":
            self.content.append(1)
        if tag == "em" or tag == "i":
            self.content.append(3)
        if tag == "a":
            self.content[-1], self.content[-2] = self.content[-2], self.content[-1]
            if type(self.content[-2]) is str and type(self.content[-1]) is str:
                self.content[-2] = self.content[-2] + self.content[-1]
                hold = self.content[-1]
                del self.content[-1]
                if " " in hold:
                    for word in hold.split():
                        self.content.append(word)

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
        if tag == "h5":
            self.content.append(25)
        if tag == "h6":
            self.content.append(27)
        if tag == "u":
            self.content.append(30)
        if tag == "code":
            self.content.append(32)
        if tag == "s":
            self.content.append(34)
        if tag == "del":
            self.content.append(34)
        if tag == "ins":
            self.content.append(30)
        if tag == "img":
            self.content.append(36)
        if tag == "table":
            self.content.append(40)
        if tag == "tr":
            self.content.append(41)
        if tag == "td" or tag == "th":
            self.content.append(42)
        if tag == "caption":
            self.content.append(44)
        if tag == "q":
            self.content.append(46)


    def handle_data(self, data):
        if len(self.content) >=2:
            if self.content[-2] == 4:
                data = "[" + data + "]"
                self.content.append(data)
                return
            if self.content[-1] == 39:
                self.content.append(data)
                return
            if self.content[-2] == 45:
                data = "\"" + data + "\""
        
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

def is_html(text):
    elements = set(HTMLSanitizerMixin.acceptable_elements)

    parser = TestHTMLParser()
    parser.feed(text)

    return True if parser.elements.intersection(elements) else False
       

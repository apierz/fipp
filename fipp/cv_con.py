import curses
from html.parser import HTMLParser
import requests
import json


class CCV_con():
    # Curses Content View Controller
    def __init__(self, stdscr, content, content_width, top_string, bottom_string):
        
        self.bottom_pad = curses.newpad(1, curses.COLS)
        self.top_pad = curses.newpad(1, curses.COLS)
        self.top_string = top_string
        self.bottom_string = bottom_string
        self.content = content
        self.v_scroll_position = 0
        self.h_scroll_position = 0
        self.stdscr = stdscr
        self.width = curses.COLS
        self.content_width = content_width
        self.content_lines = 0

        lines = curses.LINES if int(len(content)/50)+1 <= curses.LINES else int(len(content)/50)+1
        self.content_pad = curses.newpad(lines, self.content_width + 1 )

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

        self.update_top_string(self.top_string)
        self.update_bottom_string(self.bottom_string)

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
                if piece == 66:
                    self.content_pad.addstr(line,0, text_line, curses.A_REVERSE)
                    gap = ""
                    text_line = margin
                    line+=1

        self.content_lines = line
        f = open("raw_data.txt", "w")
        for item in plist:
            if type(item) is str:
                f.write(item)
            else:
                f.write(str(item))
        f.close()

                
    def update_top_string(self, top_string):
        self.top_pad.move(0,0)
        self.top_pad.clrtoeol()
        self.top_pad.move(0,0)
        top_string = top_string + self._get_filler_string_tb(top_string)

        if self.v_scroll_position > 0:
            top_string = top_string[:-2]
            top_string+= "↑ "

        if self.v_scroll_position <= 0:
            top_string = top_string[:-2]
            top_string+= "  "

        self.top_pad.addstr(0,0, top_string)
        self.top_pad.refresh(0,0, 0,0, 0,self.width)

    def update_bottom_string(self, bottom_string):
        self.bottom_pad.move(0,0)
        self.bottom_pad.clrtoeol()
        self.bottom_pad.move(0,0)
        bottom_string = "  " + self.bottom_string
        bottom_string = bottom_string + self._get_filler_string_tb(bottom_string)
        
        if self.v_scroll_position < self.content_lines + curses.LINES -2:
            holder = bottom_string[-1]
            bottom_string = bottom_string[:-2]
            bottom_string+= "↓" + holder

        if self.v_scroll_position == self.content_lines - curses.LINES + 2:
            holder = bottom_string[-1]
            bottom_string = bottom_string[:-2]
            bottom_string+= " " + holder

        if self.h_scroll_position != self.content_width - curses.COLS:
            bottom_string = bottom_string[:-1]
            bottom_string+= "→"

        if self.h_scroll_position == self.content_width - curses.COLS:
            bottom_string = bottom_string[:-1]
            bottom_string+= " "

        if self.h_scroll_position > 0:
            bottom_string = bottom_string[1:]
            bottom_string= "←" + bottom_string

        if self.h_scroll_position == 0:
            bottom_string = bottom_string[1:]
            bottom_string= " " + bottom_string

        self.bottom_pad.addstr(0,0, bottom_string)
        self.bottom_pad.refresh(0,0, curses.LINES-1,0,
                                    curses.LINES-1,self.width)

    def scrollup(self):
        if self.v_scroll_position >0:
            self.v_scroll_position-=1
            self.content_pad.refresh(self.v_scroll_position, self.h_scroll_position,
                                         1, 0,
                                         curses.LINES -2, curses.COLS - 1)
            self.update_top_string(self.top_string)
            self.update_bottom_string(self.bottom_string)

    def scrolldown(self):
        if self.v_scroll_position < self.content_lines - curses.LINES+2:
            self.v_scroll_position+=1
            self.content_pad.refresh(self.v_scroll_position, self.h_scroll_position,
                                         1, 0,
                                         curses.LINES -2, curses.COLS - 1)
            self.update_top_string(self.top_string)
            self.update_bottom_string(self.bottom_string)

    def scrollright(self):
        if self.h_scroll_position < self.content_width - curses.COLS:
            self.h_scroll_position+=1
            self.content_pad.refresh(self.v_scroll_position, self.h_scroll_position,
                                         1, 0,
                                         curses.LINES -2, curses.COLS - 1)
            self.update_top_string(self.top_string)
            self.update_bottom_string(self.bottom_string)


    def scrollleft(self):
        if self.h_scroll_position != 0:
            self.h_scroll_position-=1
            self.content_pad.refresh(self.v_scroll_position, self.h_scroll_position,
                                         1, 0,
                                         curses.LINES -2, curses.COLS - 1)
            self.update_top_string(self.top_string)
            self.update_bottom_string(self.bottom_string)

    def _get_filler_string_content(self, str=""):
        # filler_string = ""
        # while len(str) + len(filler_string) < self.content_width - 1:
        #     filler_string+= " "
        # filler_string+=" "

        filler_string = ""
        y, x = self.content_pad.getmaxyx()
        for i in range(1, x):
            filler_string+=" "
        
        return filler_string

    def _get_filler_string_tb(self, str=""):
        filler_string = ""
        while len(str) + len(filler_string) < curses.COLS - 2:
            filler_string+= " "
        return filler_string


    def goo_shorten_url(self, url):
        post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyCoMyPAgrC7LEzSMZV0Mr6JxRhp1JZ4yt4'
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post(post_url, data=json.dumps(payload), headers=headers)
        response_data = r.json()
        return response_data['id']

# class cdlv_con(cv_con):
    #Curses Dynamic List View Controller
    
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
        for name, value in attrs:
            if name == "href":
                self.content.append("(" + value + ")")
            

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


    def handle_data(self, data):
        if len(self.content) >=2:
            if self.content[-2] == 4:
                data = "[" + data + "]"
                self.content.append(data)
                return
        
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
       

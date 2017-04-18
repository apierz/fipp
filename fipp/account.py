import curses
from curses import wrapper
import locale
import os
from os import path
import datetime
from datetime import date, time, timedelta
import time
import urllib.request
import json
from pathlib import Path
import pickle

class Feed():
    def __init__(self, title, feed_id, feed_url, site_url, account):
        self.title = title
        self.feed_id = feed_id
        self.feed_url = feed_url
        self.site_url = site_url
        self.account = account

class FeedItem():
    def __init__(self, feed_item_id, published_at, created_at,
                     url, title, starred, read, body, author,
                     feed_id, feed_title, service):
        self.feed_item_id = feed_item_id
        self.published_at = published_at
        self.created_at = created_at
        self.url = url
        self.title = title.rstrip()
        self.starred = starred
        self.read = read
        self.body = "<url>" + self.url + "</url></p>" + body
        self.author = author
        self.feed_id = feed_id
        self.feed_title = feed_title
        self.service = service

    def get_header_string(self):
        header_string = ""
        header_string += self.format_date(self.published_at)

        short_name = (self.feed_title[:21] + '…') if len(self.feed_title) > 21 else self.feed_title

        while len(short_name) <= 22:
            short_name += " "

        header_string += short_name + " " + self.title

        return header_string

    def get_date_time(self):
        t1=time.localtime(self.published_at)
        min_string = ""
        if t1.tm_min < 10:
            min_string = "0" + str(t1.tm_min)
        else:
            min_string = str(t1.tm_min)

        time_string = "| " + str(t1.tm_hour) + ":" + min_string + " " + str(t1.tm_mon) + "/" + str(t1.tm_mday) + " |"

        return time_string
        

    def format_date(self, date_int):
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


class Account():

    global FW_API_URL
    FW_API_URL = "https://feedwrangler.net/api/v2/"
    global FW_CLIENT_KEY
    FW_CLIENT_KEY = "77037deda1050eff59d9619d4d2f4fd4"

    global FB_API_URl
    FB_API_URl = "https://api.feedbin.com/v2/"
    head = { "Content-Type": "application/json; charset=utf-8"}

    def __init__(self, username = "", password = "", service = "", key = "",
                     bf_col = 7, bb_col = 0, mf_col = 0, mb_col = 7,
                     hf_col = 7, hb_col = 3, tf_col = 7, tb_col = 4,
                     sf_col = 4, sb_col = 0):
        
        self.bf_col = bf_col
        self.bb_col = bb_col
        self.mf_col = mf_col
        self.mb_col = mb_col
        self.hf_col = hf_col
        self.hb_col = hb_col
        self.tf_col = tf_col
        self.tb_col = tb_col
        self.sf_col = sf_col
        self.sb_col = sb_col
        self.color_changed = False
        
        self.service = service
        self.username = username
        self.password = password
        self.key = key
        self.feeds = []

        if service == "Feed Wrangler":
            response = urllib.request.urlopen(FW_API_URL + "users/authorize?email=" + self.username +
                                                  "&password=" + password +
                                                  "&client_key=" + FW_CLIENT_KEY).read()
            data = json.loads(response.decode())
            if data['error']:
                pass
            else:
                self.key = data['access_token']
                self.save_user_info()
            self.load_feeds()

            self.save_user_info()

        if service == "Feedbin":
            s = requests.Session()
            ret = s.get("https://api.feedbin.com/v2/authentication.json", auth=(self.username, password))
            if ret.status_code is 403:
                pass
            else:
                self.key = s
                self.save_user_info()
            self.load_feeds()


    def add_feed(self, url):
        if self.service == "Feed Wrangler":
            try:
                response = urllib.request.urlopen(FW_API_URL + \
                            "/subscriptions/add_feed_and_wait?access_token=" + \
                            self.key + "&choose_first=true" +\
                            "&feed_url="+url).read()
                data = json.loads(response.decode())
                if data['error']:
                    return data['error']
                else:
                    return True
            except:
                return data['error']

        if self.service == "Feedbin":
            try:
                payload = {"feed_url": url}
                ret = self.key.post(FB_API_URl + "subscriptions.json",
                                  data = json.dumps(payload),
                                  headers = head,
                                  auth=(self.username, self.password))
                if ret.status_code is 403:
                    return "Error Reaching Feedbin Server"
                else:
                    return True
            except:
                return "Error Reaching Feedbin Server"
                

    def remove_feed(self, feed_id):
        if self.service == "Feed Wrangler":
            try:
                response = urllib.request.urlopen(FW_API_URL + \
                            "subscriptions/remove_feed?access_token=" + \
                            self.key + \
                            "&feed_id=" + feed_id).read()
                data = json.loads(response.decode())
                if data['error']:
                    return data['error']
                else:
                    return True
            except:
                return "Error reaching server"

    def process_data(self, data):
        if self.service == "Feed Wrangler":
            if data['error']:
                pass
            else:
                feed_items = []
                for item in data['feed_items']:
                    if '\n' in item['title']:
                        title = ""
                        titles = item['title'].splitlines()
                        for piece in titles:
                            title += piece + " "
                        item['title'] = title
                    feed_items.append(FeedItem(item['feed_item_id'],
                                                item['published_at'],
                                                item['created_at'],
                                                item['url'],
                                                item['title'],
                                                item['starred'],
                                                item['read'],
                                                item['body'],
                                                item['author'],
                                                item['feed_id'],
                                                item['feed_name'],
                                                self.service))
                if len(data['feed_items']) is 0:
                    feed_items.append(FeedItem(0,
                                               0,
                                                0,
                                                "none",
                                                "no items",
                                                False,
                                                False,
                                                "None",
                                                "None",
                                                0,
                                                " ",
                                                self.service))
                return feed_items

    def get_starred_items(self):
        try:
            if self.service == "Feed Wrangler":
                response = urllib.request.urlopen(FW_API_URL + "feed_items/list?starred=true" + \
                                                    "&access_token=" + self.key).read()
                data = json.loads(response.decode())
                if data['error']:
                    return data['error']
                else:
                    return self.process_data(data)
        except:
            return "Error reaching server"

    def get_most_recent(self, feed):
        try:
            if self.service == "Feed Wrangler":
                response = urllib.request.urlopen(FW_API_URL + "feed_items/list?feed_id=" + \
                                                    str(feed.feed_id) + \
                                                    "&limit=25" + \
                                                    "&access_token=" + self.key).read()
                data = json.loads(response.decode())
                if data['error']:
                    return data['error']
                else:
                    return self.process_data(data)
        except:
            return "Error reaching server"

    def get_unread_items(self):
        try:
            if self.service == "Feed Wrangler":
                response = urllib.request.urlopen(FW_API_URL + "/feed_items/list?access_token=" +
                                                        self.key + "&read=false").read()
                data = json.loads(response.decode())
                if data['error']:
                    return data['error']
                else:
                    return self.process_data(data)
        except:
            return "Error reaching server"

    def save_user_info(self):
        outFile = open("user_info", "wb")
        pickle.dump(self, outFile)
        outFile.close()

    def verify_user_info(self):
        my_file = Path("user_info")
        if my_file.is_file():
            f = open("user_info", "rb")
            data = f.read()
            uaccount = pickle.loads(data)
            uaccount.load_feeds()
            f.close()
            service = uaccount.service

            if service == "Feed Wrangler":
                return uaccount
            else:
                f.close()
                return False
        else:
            return False

    def load_feeds(self):
        if self.service == "Feed Wrangler":
            try:
                if self.key != "":
                    response = urllib.request.urlopen(FW_API_URL + "subscriptions/list?access_token=" + self.key).read()
                    data = json.loads(response.decode())
                    if data['error']:
                        return data['error']
                    else:
                        self.feeds = []
                        for feed in data['feeds']:
                            feed_sub = Feed(feed['title'],
                                                feed['feed_id'],
                                                feed['feed_url'],
                                                feed['site_url'],
                                                self)
                            self.feeds.append(feed_sub)

                        self.save_user_info()
            except:
                return "Error reaching server"

    def change_star_status(self, item_id, status):
       if self.service == "Feed Wrangler":
           response = urllib.request.urlopen(FW_API_URL + "feed_items/update?access_token=" +
                                                self.key + "&feed_item_id=" +
                                                str(item_id) + "&starred=" +
                                                str(status).lower()).read()
           data = json.loads(response.decode())
           if data['error']:
               return data['error']
           else:
               return True

    def change_read_status(self, item_id, status):
        if self.service == "Feed Wrangler":
            try:
                response = urllib.request.urlopen(FW_API_URL + "feed_items/update?access_token=" +
                                                    self.key + "&feed_item_id=" +
                                                    str(item_id) + "&read=" +
                                                    str(status).lower()).read()

                data = json.loads(response.decode())
                if data['error']:
                    return data['error']
                else:
                    return True
            except:
                return "Error reaching server"

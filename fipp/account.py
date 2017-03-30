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
# import readline
from pathlib import Path

class Feed():
    def __init__(self, title, feed_id, feed_url, site_url):
        self.title = title
        self.feed_id = feed_id
        self.feed_url = feed_url
        self.site_url = site_url

class FeedItem():
    def __init__(self, feed_item_id, published_at, created_at,
                     url, title, starred, read, body, author,
                     feed_id, feed_title, service):
        self.feed_item_id = feed_item_id
        self.published_at = published_at
        self.created_at = created_at
        self.url = url
        self.title = title
        self.starred = starred
        self.read = read
        self.body = body
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

    def __init__(self, username = "", password = "", service = "", key = ""):
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
                key = data['error']
            else:
                self.key = data['access_token']
                self.write_user_info(self.service, self.username, self.key)
            self.load_feeds()


    def get_unread_items(self):
            if self.service == "Feed Wrangler":
                response = urllib.request.urlopen(FW_API_URL + "/feed_items/list?access_token=" +
                                                    self.key + "&read=false").read()
            data = json.loads(response.decode())
            unread_feed_items = []

            for item in data['feed_items']:
                unread_feed_items.append(FeedItem(item['feed_item_id'],
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
            return unread_feed_items


    def write_user_info(self, service, username, auther):
        f = open("user_info", "w+")
        f.write(service + "\n" +
                username + "\n" +
                auther)
        f.close()

    def verify_user_info(self):
        my_file = Path("user_info")
        if my_file.is_file():
            f = open("user_info", "r")
            # service = f.readline().rstrip()
            service = "Feed Wrangler"

            if service == "Feed Wrangler":
                # username = f.readline().rstrip()
                # key = f.readline().rstrip()
                username = "andy@andypierz.com"
                key = "eb5324a134d198bd7910db38c517b04f"
                user_account = Account(username = username, key = key, service = service)
                f.close()
                return user_account
            else:
                f.close()
                return False
        else:
            return False

    def load_feeds(self):
        if self.service == "Feed Wrangler":
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
                                            feed['site_url'])
                        self.feeds.append(feed_sub)

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
               return data['result']

    def change_read_status(self, item_id, status):
        if self.service == "Feed Wrangler":
            response = urllib.request.urlopen(FW_API_URL + "feed_items/update?access_token=" +
                                                self.key + "&feed_item_id=" +
                                                str(item_id) + "&read=" +
                                                str(status).lower()).read()

            data = json.loads(response.decode())
            if data['error']:
                return data['error']
            else:
                return data['result']

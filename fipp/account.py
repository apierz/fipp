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
import readline

class Account():

    global api_url
    api_url = "https://feedwrangler.net/api/v2/"
    global client_key
    client_key = "77037deda1050eff59d9619d4d2f4fd4"

    def read_email(self):
        if path.exists("account_info.txt"):
            f = open("account_info.txt", "r")
            if f.mode == 'r':
                email = f.readline()
                f.close()
                return email
        else:
            return None

    def read_access_token(self):
        if path.exists("account_info.txt"):
            f = open("account_info.txt", "r")
            if f.mode == 'r':
                access_token = f.readline()
                access_token = f.readline().rstrip()
                f.close()
                return access_token
        else:
            return None

    def authenticate_user(self):
        while self.access_token == None or self.email == None:
            print("No account found: \n")
            email = input("Enter email: ")
            password = input("Enter password: ")
            response = urllib.request.urlopen(api_url + "users/authorize?email=" + email + "&password=" + password + "&client_key=" + client_key).read()
            data = json.loads(response.decode())

            if data['error']:
                print(data['error'])
            else:
                self.email        = data['user']['email']
                self.access_token = data['access_token']
                self.feeds        = data['feeds']
                self.write_data(self.email, self.access_token)

    def write_data(self, email, access_token):
        f = open("account_info.txt", "w+")
        if f.mode == "w+":
            f.write(email + "\n" + access_token + "\n")
            f.close()

    def load_feeds(self, access_token):
        if access_token != None:
            response = urllib.request.urlopen(api_url + "subscriptions/list?access_token=" + access_token).read()
            data = json.loads(response.decode())

            if data['error']:
                return None
            else:
                return data['feeds']

    def __init__(self):
        self.email = self.read_email()
        self.access_token = self.read_access_token()
        self.feeds = self.load_feeds(self.access_token)
        self.client = "Feed Wrangler"
        self.authenticate_user()

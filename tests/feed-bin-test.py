import requests
from requests import session
import json
from .context import fipp

url = "https://api.feedbin.com/v2"
uname = "andy@andypierz.com"
pword = "9breaker"
head = { "Content-Type": "application/json; charset=utf-8"}

s = requests.Session()
ret = s.get("https://api.feedbin.com/v2/authentication.json", auth=(uname, pword))
print(ret.status_code)
print(ret.headers['content-type'])
print(s.cookies)
print(ret.text)

ret = s.get("https://api.feedbin.com/v2/subscriptions.json", auth=(uname, pword))
print(ret.status_code)
print(ret.headers['content-type'])
print(ret.text)

# ret = s.get("https://api.feedbin.com/v2/unread_entries.json", auth=(uname, pword))
# print(ret.status_code)
# print(ret.headers['content-type'])
# print(ret.text)

# ids = ret.text[1:-1]

# ret = s.get("https://api.feedbin.com/v2/entries.json", headers = {"ids":ids}, auth=(uname, pword),)
# print(ret.status_code)
# print(ret.headers['content-type'])
# print(ret.text)



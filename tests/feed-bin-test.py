import requests
from requests import session
import json
from .context import fipp

url = "https://api.feedbin.com/v2/"
uname = "andy@andypierz.com"
pword = "9breaker"
head = { "Content-Type": "application/json; charset=utf-8"}

s = requests.Session()
ret = s.get("https://api.feedbin.com/v2/authentication.json", auth=(uname, pword))
print(ret.status_code)
print(ret.headers['content-type'])
print(s.cookies)
print(ret.text)
print("------------")

# ret = s.get("https://api.feedbin.com/v2/subscriptions.json", auth=(uname, pword))
# print(ret.status_code)
# print(ret.headers['content-type'])
# print(ret.text)


# ret = s.get("https://api.feedbin.com/v2/starred_entries.json", auth=(uname, pword))
# starred = json.loads(ret.text)

ret = s.get("https://api.feedbin.com/v2/unread_entries.json", auth=(uname, pword))
unread = json.loads(ret.text)
idstring = ""
for idnum in unread:
    idstring += str(idnum) + ","
idstring = idstring[:-1]
print(idstring)


ret = s.get("https://api.feedbin.com/v2/entries.json?=" + idstring, auth=(uname, pword),)
print(ret.status_code)
print(ret.headers['content-type'])
data = json.loads(ret.text)
feed_id = data[0]['feed_id']
# ret = s.get(url + "entries.json?ids="+ idstring,
#                     headers = head,
#                     auth=(uname, pword))
# print(ret.text)
# print(ret.status_code)
# data = json.loads(ret.text)
# print(data)
print(feed_id)
ret = s.get("https://api.feedbin.com/v2/feeds/" + str(feed_id) + "/entries.json?page=1",
                                  headers = head,
                                  auth=(uname, pword))
data = json.loads(ret.text)
print(data)


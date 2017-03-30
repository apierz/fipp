import requests
from requests import session
import json
from .context import fipp


url = "http://www.newsblur.com"
uname = "andy@andypierz.com"
pword = "9breaker"

s = requests.Session()
head = {'username' : uname, "password" : pword}
ret = s.post("https://www.newsblur.com/api/login", headers=head, auth=(uname, pword))
print(ret.status_code)
print(ret.headers['content-type'])
print(json.dumps(ret.json(), indent=2))

# head = {"include_favicons" : "false", "flat" : "true"}
# ret = requests.get(url + "/reader/feeds", json=head)
# print(ret.status_code)

# data = ret.json()
# print(data)


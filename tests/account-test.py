import os
from os import path
import curses
from curses import wrapper

from .context import fipp
from fipp.account import Account


def main():
    my_account = Account()
    my_account = my_account.verify_user_info()

    if my_account is False:
        service = input('Enter feed service: ')
        username = input('Enter email: ')
        password = input('Enter password: ')

        my_account = Account(username=username, password=password, service = service)

    feeds = my_account.feeds

    for feed in feeds:
        print(feed.title + '\n')

    unread_items = my_account.get_unread_items()

    print(unread_items[-1].body)
    
                  
    

if __name__ == "__main__":
    main()

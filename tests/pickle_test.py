import pickle
from fipp.account import Account

def main():
    uaccount = Account()
    uaccount = uaccount.verify_user_info()

    print(uaccount.username)
    print(uaccount.password)
    print(uaccount.service)

if __name__ == "__main__":
    main()

import requests
from colorama import Fore as COL
import time
import threading

def Check(auth):
    global tokencount
    try:
        token = auth.split(":")[2]
        halfauth = auth[:len(token)//2]
        x = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token})
        if x.status_code == 200:
            y = requests.get('https://discord.com/api/v9/users/@me/affinities/users', headers={'Authorization': token})
            json = x.json()
            if y.status_code == 200:
                print(COL.GREEN + f'VALID: {halfauth}***** {json["username"]}#{json["discriminator"]}')
                tokencount += 1
                open("valid.txt", "a").write(auth+"\n")
                open("unformat.txt", "a").write(token+"\n")
            elif y.status_code == 403:
                print(COL.YELLOW + f'LOCKED: {halfauth}***** {json["username"]}#{json["discriminator"]}')
            elif y.status_code == 429:
                print(COL.YELLOW + f"You're being rate limited")
                time.sleep(y.headers['retry-after'])
            elif x.status_code == 429:
                print(COL.YELLOW + f"You're being rate limited")
                time.sleep(y.headers['retry-after'])
            else:
                print(COL.RED + f'INVALID: {halfauth}')
    except:
        pass

open("valid.txt", "w")
tokencount = 0
tokenpath = input("Tokens file:")
for auth in open(tokenpath, "r").read().splitlines():
    t =threading.Thread(target=Check, args=(auth, )).start()

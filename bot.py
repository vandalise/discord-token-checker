import requests
from colorama import Fore as COL
import time
import threading

def Check(auth):
    global tokencount
    try:
        halfauth = auth[:len(auth)//2]
        x = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': auth})
        if x.status_code == 200:
            y = requests.get('https://discord.com/api/v9/users/@me/affinities/users', headers={'Authorization': auth})
            json = x.json()
            if y.status_code == 200:
                print(COL.GREEN + f'VALID: {halfauth}***** {json["username"]}#{json["discriminator"]}')
                tokencount += 1
                open("valid.txt", "a").write(auth+"\n")
            elif y.status_code == 403:
                print(COL.YELLOW + f'LOCKED: {halfauth}***** {json["username"]}#{json["discriminator"]}')
            elif y.status_code == 429:
                print(COL.YELLOW + f"You're being rate limited")
                time.sleep(y.headers['retry-after'])
            elif x.status_code == 429:
                print(COL.YELLOW + f"You're being rate limited")
                time.sleep(y.headers['retry-after'])
            else:
                print(COL.RED + f'INVALID: {auth}')
    except:
        pass

open("valid.txt", "w")
tokencount = 0
tokenpath = input("Tokens file:")
for token in open(tokenpath, "r").read().splitlines():
    t =threading.Thread(target=Check, args=(token, )).start()

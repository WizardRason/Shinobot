#import io
import json
import os

with open('settings.json') as f:
	settings = json.load(f)

username = settings["mal_username"]
password = settings["mal_password"]

#                 WizardRason#6819
owner_user  = settings["owner_user"]
token       = settings["token"]

secret_channel = settings["secret_channel"]
public_channel = settings["public_channel"]

def init():
    if os.path.exists("settings.json"):
        # checks if file exists
        print ("File exists and is readable")
    else:
        print ("Either file is missing or is not readable, creating file...")

        settings = {k: input(f'Please enter {m}: ') for k, m in {
            "mal_username": "your mal username",
            "mal_password": "your mal password",
            "owner_user": "discord id",
            "token": "your bot token",
            "secret_channel": "the id of your private channel (where you talk as your bot)",
            "public_channel": "the id of your default public channel"
        }.items()}


        with open('settings.json','w') as f:
            json.dump(settings, f)

    if os.path.exists("rip_map.json"):
        # checks if file exists
        print ("File exists and is readable")
    else:
        print ("Either file is missing or is not readable, creating file...")
        f = open('rip_map.json','wb')  #create file locally
        f.close()

        d = {}

        with open('rip_map.json','w') as f:
            json.dump(d, f)
            
if __name__ == '__main__':
    init()
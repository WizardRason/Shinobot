#import io
import json
import os

def startupCheck():
    if os.path.exists("settings.json"):
        # checks if file exists
        print ("File exists and is readable")
    else:
        print ("Either file is missing or is not readable, creating file...")
        f = open('settings.json','wb')  #create file locally
        f.close()

        mal_username   = input("Please enter your mal username: ")
        mal_password   = input("Please enter your mal password: ")
        owner_user     = input("Please enter your discord id: ")
        token          = input("Please enter your bot token: ")
        secret_channel = input("Please enter the id of your private channel(where you talk as your bot): ")
        public_channel = input("Please enter the id of your default public channel: ")

        settings = {
        "mal_username"    : mal_username,
        "mal_password"    : mal_password,
        "owner_user"      : owner_user,
        "token"           : token,
        "secret_channel"  : secret_channel,
        "public_channel"  : public_channel
        }


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

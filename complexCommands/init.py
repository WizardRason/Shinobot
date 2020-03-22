import json
import os

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
os.chdir('..')

username = None
password = None

#                 WizardRason#6819
owner_user  = None
token       = None

admin_server = None

def init():
	if os.path.exists("jsonFiles/settings.json"):
		# checks if file exists
		print ("File exists and is readable")
	else:
		print ("Either file is missing or is not readable, creating file...")

		settings = {k: input(f'Please enter {m}: ') for k, m in {
			"mal_username": "your mal username",
			"mal_password": "your mal password",
			"owner_user": "discord id",
			"token": "your bot token",
			"admin_server": "the id of your server (where you talk as your bot)"
		}.items()}

		settings["owner_user"] = int(settings["owner_user"])
		settings["admin_server"] = int(settings["admin_server"])

		with open('jsonFiles/settings.json','w') as f:
			json.dump(settings, f)

	if os.path.exists("jsonFiles/rip_map.json"):
		# checks if file exists
		print ("File exists and is readable")
	else:
		print ("Either file is missing or is not readable, creating file...")
		f = open('jsonFiles/rip_map.json','wb')  #create file locally
		f.close()

		d = {}

		with open('jsonFiles/rip_map.json','w') as f:
			json.dump(d, f)

	if os.path.exists("jsonFiles/channels.json"):
		# checks if file exists
		print ("File exists and is readable")
	else:
		print ("Either file is missing or is not readable, creating file...")
		f = open('jsonFiles/channels.json','wb')  #create file locally
		f.close()

		d = {}

		with open('jsonFiles/channels.json','w') as f:
			json.dump(d, f)

	if os.path.exists("jsonFiles/retiredRips.json"):
		# checks if file exists
		print ("File exists and is readable")
	else:
		print ("Either file is missing or is not readable, creating file...")
		f = open('jsonFiles/retiredRips.json','wb')  #create file locally
		f.close()

		d = {}

		with open('jsonFiles/retiredRips.json','w') as f:
			json.dump(d, f)
	openSettings()
			
def openSettings():
	global username
	global password
	global owner_user
	global token
	global admin_server
	with open('jsonFiles/settings.json') as f:
		settings = json.load(f)

	username = settings["mal_username"]
	password = settings["mal_password"]

	#             WizardRason#6819
	owner_user  = settings["owner_user"]
	token       = settings["token"]

	admin_server = settings["admin_server"]
	
if __name__ == '__main__':
	init()

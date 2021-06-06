import json
import os
import pickle

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

	filePaths = [
		"settings.json",
		"rip_map.json",
		"channels.p",
		"retiredRips.json"
	]
	allRead = True

	if not os.path.isdir(os.path.join(path,'..','scripts')):
		os.mkdir(os.path.join(path,'..','scripts'))
	if not os.path.isdir(os.path.join(path,'..','ripPics')):
		os.mkdir(os.path.join(path,'..','ripPics'))

	for filePath in filePaths:
		if os.path.exists("jsonFiles/" + filePath):
			# checks if file exists
			pass #print (settingsFile + " exists and is readable")
		else:
			print ("Either " + filePath + " is missing or is not readable, creating new file...")

			if "settings.json" in filePath:
				settings = {k: input(f'Please enter {m}: ') for k, m in {
					"mal_username": "your mal username (depreciated)",
					"mal_password": "your mal password (depreciated)",
					"owner_user": "discord id",
					"token": "your bot token",
					"admin_server": "the id of your server (where you talk as your bot)"
				}.items()}

				settings["owner_user"] 		= int(settings["owner_user"])
				settings["admin_server"] 	= int(settings["admin_server"])
			else:
				f = open('jsonFiles/'+ filePath,'wb')  #create file locally
				f.close()
				settings = {}

			if ".json" in filePath:
				with open('jsonFiles/settings.json','w') as f:
					json.dump(settings, f)
			else:
				pickle.dump( settings, open( "jsonFiles/channels.p", "wb" ) )
			allRead = False

	if allRead: print ("All files exist and are readable")

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

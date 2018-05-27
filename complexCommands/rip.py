import asyncio
import json
import random
import os
import requests

from complexCommands import init

owner_user = init.owner_user

rip_cooldown = []
cooldownTime = 15

async def commandRip(message, client):
	global rip_cooldown
	#adds to the rip_map
	if (message.content.startswith('!ripadd')): #allow for multiple quotes per picture
		with open('rip_map.json') as f:
			rip_map = json.load(f)
		if len(message.content.strip()) > 7:
			mess = message.content[7:].strip()
			filename = mess.partition(' ')[0]
			quote    = mess.partition(' ')[2]

			if message.attachments or quote:
				if filename in list(rip_map.keys()):
					rip_map[filename].append(quote)
				else:
					rip_map.update({filename: [quote]})

				for k in message.attachments:
					if os.path.exists('ripPics/' + filename + '.jpg'):
						client.send_file(client.get_member(owner_user),'ripPics/' + filename + '.jpg',content="This got replaced")

					f = open('ripPics/' + filename + '.jpg','wb')  #create file locally
					f.write(requests.get(k['url']).content)  #write image content to this file
					f.close()

				await client.send_file(message.channel, 'ripPics/' + filename + '.jpg' if os.path.exists('ripPics/' + filename + '.jpg') else None,content=quote)
			else:
				await client.send_message(message.channel, 'Wait... what am I supposed to post?')
		else:
			await client.send_message(message.channel, '```!ripadd <distinguishing filename without extension> <message to be included>\nInclude picture in post```')

		with open('rip_map.json','w') as f:
			json.dump(rip_map, f)

	#pm the message author with a list of all "rip"s
	elif (message.content.startswith('!riplist')):
		with open('rip_map.json') as f:
			rip_map = json.load(f)
		list_rip ='```'
		for k in list(rip_map.keys()):
			list_rip = list_rip + k + ':\n'
			for l in rip_map[k]:
				list_rip = list_rip +'\t"' + l + '"\n'
		await client.send_message(message.author, list_rip + '```')

	#posts a meme based on the given search term, or posts a default meme (meme.jpg)
	elif ((message.author.id == owner_user or message.author.id not in rip_cooldown) and message.content.startswith('!rip')): #not done yet
		rip_cooldown.append(message.author.id)
		with open('rip_map.json') as f:
			rip_map = json.load(f)
		chosen_rip = message.content[4:].strip() if len(message.content.strip()) > 4 else None
		rip_meme = chosen_rip if chosen_rip in list(rip_map.keys()) else random.choice(list(rip_map.keys()))
		#await client.send_message(message.channel, rip_map[rip_meme])
		if os.path.exists('ripPics/' + rip_meme + '.jpg'):
			await client.send_file(message.channel, 'ripPics/' + rip_meme + '.jpg',content=random.choice(rip_map[rip_meme]))
		else:
			await client.send_message(message.channel, random.choice(rip_map[rip_meme]))
		await asyncio.sleep(cooldownTime)
		rip_cooldown.remove(message.author.id)

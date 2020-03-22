import discord
import asyncio
import json
import random
import os
import requests

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
os.chdir('..')

rip_cooldown = True
cooldownTime = 15

with open('jsonFiles/rip_map.json') as f:
	rip_map = json.load(f)

async def commandRip(message, client, owner_user):
	global rip_cooldown
	global rip_map
	#adds to the rip_map
	if (message.content.startswith('!ripadd')): #allow for multiple quotes per picture
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
						await client.get_member(owner_user).send("This got replaced",file = discord.File('ripPics/' + filename + '.jpg'))
						# await client.send_file(client.get_member(owner_user),'ripPics/' + filename + '.jpg',content="This got replaced")

					f = open('ripPics/' + filename + '.jpg','wb')  #create file locally
					f.write(requests.get(k['url']).content)  #write image content to this file
					f.close()

				await message.channel.send(quote, file = (discord.File('ripPics/' + filename + '.jpg') if os.path.exists('ripPics/' + filename + '.jpg') else None))
				# await client.send_file(message.channel, 'ripPics/' + filename + '.jpg' if os.path.exists('ripPics/' + filename + '.jpg') else None,content=quote)
			else:
				await message.channel.send('Wait... what am I supposed to post?')
				# await client.send_message(message.channel, 'Wait... what am I supposed to post?')
		else:
			await message.channel.send('```!ripadd <distinguishing filename without extension> <message to be included>\nInclude picture in post```', delete_after = 30.0)
			# await client.send_message(message.channel, '```!ripadd <distinguishing filename without extension> <message to be included>\nInclude picture in post```')

		with open('jsonFiles/rip_map.json','w') as f:
			json.dump(rip_map, f)

	#pm the message author with a list of all "rip"s
	elif (message.content.startswith('!riplist')):
		list_rip ='```All Items that can be called with !rip command:\n\n'
		for k in list(rip_map.keys()):
			list_rip = list_rip + k + ':\n'
			for l in rip_map[k]:
				list_rip = list_rip +'\t"' + l + '"\n'
		await message.author.send(list_rip + '```')
		# await client.send_message(message.author, list_rip + '```')

	elif (message.content.startswith('!ripremove') and message.author.id == owner_user):
		with open('jsonFiles/retiredRips.json') as f:
			retiredList = json.load(f)
		mess = message.content[10:].strip()
		
		if mess in rip_map.keys():
			retiredList.update({mess: rip_map.pop(mess, None)})
			with open('jsonFiles/retiredRips.json','w') as f:
				json.dump(retiredList, f)
			with open('jsonFiles/rip_map.json','w') as f:
				json.dump(rip_map, f)
			await message.add_reaction('👍')

	#posts a meme based on the given search term, or posts a default meme (meme.jpg)
	elif ((message.author.id == owner_user or rip_cooldown) and message.content.startswith('!rip')): #not done yet
		rip_cooldown = False
		chosen_rip = message.content[4:].strip() if len(message.content.strip()) > 4 else None
		rip_meme = chosen_rip if chosen_rip in list(rip_map.keys()) else random.choice(list(rip_map.keys()))

		await message.channel.send(random.choice(rip_map[rip_meme]), file = discord.File('ripPics/' + rip_meme + '.jpg') if os.path.exists('ripPics/' + rip_meme + '.jpg') else None)
		
		# if os.path.exists('ripPics/' + rip_meme + '.jpg'):
		#	await client.send_file(message.channel, 'ripPics/' + rip_meme + '.jpg',content=random.choice(rip_map[rip_meme]))
		# else:
		#	await client.send_message(message.channel, random.choice(rip_map[rip_meme]))
		await asyncio.sleep(cooldownTime)
		rip_cooldown = True

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
	if (message.content.startswith('!ripadd')): #allow for multiple quotes per picture
		if len(message.content.strip()) > 7:
			mess = message.content[7:].strip()
			filename = mess.partition(' ')[0]
			quote    = mess.partition(' ')[2]
			commandAddRip(filename, quote, message.attachments, client, message.channel, owner_user)
		else:
			await message.channel.send('```!ripadd <distinguishing filename without extension> <message to be included>\nInclude picture in post```', delete_after = 30.0)
		pass

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
		pass

	elif ((message.author.id == owner_user or rip_cooldown) and message.content.startswith('!rip')): #not done yet
		pass

async def commandAddRip(name, phrase, image, client, ctx, owner_user):
	global rip_map
	#adds to the rip_map
	#allow for multiple quotes per picture

	def check(m):
		return m.channel == ctx.channel and m.author.id == ctx.author_id and m.attachments

	if image:
		await ctx.defer()
		try:
			message = await client.wait_for('message',check=check, timeout=300.0)

			for k in message.attachments:
				if os.path.exists('ripPics/' + name + '.jpg'):
					with open('ripPics/' + name + '.jpg', 'rb') as f:
						await client.get_user(owner_user).send("This got replaced",file = discord.File(f))

				f = open('ripPics/' + name + '.jpg','wb')  #create file locally
				f.write(requests.get(k.url).content)  #write image content to this file
				f.close()
		except asyncio.TimeoutError:
			await ctx.channel.send(content = "You broke your promise {}, you never sent me any lewds! But it's ok, I forgive you... ||for now||".format(ctx.author.mention)) 
			image = False

	if image or phrase:
		if name in list(rip_map.keys()):
			rip_map[name].append(phrase)
		elif phrase:
			rip_map.update({name: [phrase]})
		
		with open('jsonFiles/rip_map.json','w') as f:
			json.dump(rip_map, f)

		await ctx.send(phrase, file = (discord.File('ripPics/' + name + '.jpg') if os.path.exists('ripPics/' + name + '.jpg') else None))
	else: 
		await ctx.send('Wait... what am I supposed to post?')

async def commandRemoveRip(name, ctx):
	with open('jsonFiles/retiredRips.json') as f:
		retiredList = json.load(f)
	
	if name in rip_map.keys():
		retiredList.update({name: rip_map.pop(name, None)})
		with open('jsonFiles/retiredRips.json','w') as f:
			json.dump(retiredList, f)
		with open('jsonFiles/rip_map.json','w') as f:
			json.dump(rip_map, f)
		await ctx.send("'rip' {} removed".format(name), hidden = True)

#posts a meme based on the given search term, or posts a default meme (meme.jpg)
async def commandRandomRip(name, ctx, owner_user):
	global rip_cooldown
	if ctx.author_id == owner_user or rip_cooldown: #not done yet
		rip_cooldown = False
		rip_meme = name if name in list(rip_map.keys()) else random.choice(list(rip_map.keys()))

		await ctx.send(random.choice(rip_map[rip_meme]), file = discord.File('ripPics/' + rip_meme + '.jpg') if os.path.exists('ripPics/' + rip_meme + '.jpg') else None)
		await asyncio.sleep(cooldownTime)
		rip_cooldown = True
	else:
		await ctx.send(content="Wait your turn, don't spam",hidden=True)

def ripChoicesList():
	listOfRips = []
	for k in list(rip_map.keys()):
		listOfRips.append({'name' : k, 'value' : k})
	return listOfRips
import discord
import asyncio
import os
import requests
#from io import BytesIO
from discord.ext.commands import Bot
from discord.ext import commands
import json
import random
import socket
import time
import pickle

from complexCommands import init
init.init()
from complexCommands import rip
#from complexCommands import anime

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

#init.init()

client  = discord.Client()

cooldownTime = 15

#                 WizardRason#6819
owner_user  = init.owner_user 	#settings["owner_user"]
token       = init.token 		#settings["token"]

admin_server = init.admin_server	#settings["admin_server"]

#with open('jsonFiles/channels.json') as f:
try:
	channels = pickle.load( open( "jsonFiles/channels.p", "rb" ) )
except EOFError:
	channels = {}

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print(owner_user)
	print('-------')
	print(path)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	print(s.getsockname()[0])
	channel = await client.fetch_user(owner_user)
	await channel.send(s.getsockname()[0])
	s.close()

#async def deleteAfterTime(message, coolDown):
#	await asyncio.sleep(coolDown)
#	await client.delete_message(message)

@client.event
async def on_message(message):
	global channels

	if (client.user.id != message.author.id and any(x in message.content.lower() for x in ["doughnut", "donut"])):
		doughLinks = [
		"https://thumbs.gfycat.com/MiserlyNippyCockroach-size_restricted.gif",
		"https://i.imgur.com/16GrVjp.gif",
		"https://i.imgur.com/1kzxKmJ.gif",
		"http://i0.kym-cdn.com/photos/images/original/000/758/438/be5.gif",
		"https://thumbs.gfycat.com/ImaginativeRadiantAldabratortoise-size_restricted.gif",
		"http://i0.kym-cdn.com/photos/images/original/001/089/184/f86.gif",
		"https://78.media.tumblr.com/9642f23f4b95da57a9ea4c835e395e7a/tumblr_oompyrlBxh1r922azo1_540.gif"
		]
		doughPhrases = [
		"Did someone say DONUTS!?!?!?!",
		"Just looking at it reveals how delicious it must be.\nI can tell! I don't even have to eat it.\nI will, though!",
		"Please present those donuts to me immediately!",
		"I haven't tasted it yet, but just imagining the flavor, I can almost feel it expanding in my mouth, and I'm certain that I'll shout, without being afraid of what others might think...\nJAPANAINO!",
		"Flocky chou?",
		"Panaino!",
		"Are they donuts? They're donuts, right? They have to be donuts!",
		"So they are donuts! That's magnificent!"
		]
		#msg_donut = 
		await message.channel.send(random.choice(doughPhrases) + "\n" + random.choice(doughLinks), delete_after = cooldownTime)
		#asyncio.ensure_future(deleteAfterTime(msg_donut, cooldownTime))

	#posts a meme based on the given search term, or posts a default meme (meme.jpg)
	elif (message.content.startswith('!meme') and False): #not done yet
		if len(message.content.strip()) > 5:
			meme = message.content[5:]
			await message.channel.send('This is a meme. Searching the web for:' + meme)
		else:
			await message.channel.send('meme.jpg')

	#posts a gif of shinobu being carried
	elif (message.content.startswith('!adult')):
		await message.channel.send('I need an adult\n' + "https://thumbs.gfycat.com/BigheartedSplendidFlyingfish-size_restricted.gif")

	#!rip commands
	elif (message.content.startswith('!rip')):
		await rip.commandRip(message, client, owner_user)
		
	#gives the link to the mal page of the given anime
	elif (message.content.startswith('!anime') or message.content.startswith('!manga')):
		#await (anime.commandAnime(message, client) if message.content[1] == 'a' else anime.commandManga(message, client))
		pass

	elif (message.content.startswith('!command')):
		cmd = message.content[8:].strip() if len(message.content.strip()) > 7 else None
		if cmd:
			scriptdir = path+"/scripts/"
			if os.path.exists('scripts/' + cmd) and (message.author.id == owner_user or "@" not in cmd):
				os.system(scriptdir + cmd)
			else: await message.channel.send("Bad Path")

	elif (message.content.startswith('!cmdlist')):
		if os.path.exists('scripts/'):
			l = os.listdir(path + '/scripts/')
			await message.channel.send([x for x in l if not '!' in x])
			if message.author.id == owner_user: await message.channel.send(l)
		else: await message.channel.send("None Saved")

	#posts everything said in public_channel into secret_channel, including who said it
	if (message.channel.type == discord.ChannelType.text and message.guild != client.get_guild(admin_server) or (client.user.id != message.author.id and message.channel.id in list(channels.keys()))):
		if message.channel.id not in list(channels.keys()) and message.guild != client.get_guild(admin_server):
			newChan = await client.get_guild(admin_server).create_text_channel(name = message.channel.name)
			channels.update({message.channel.id: newChan.id})
			channels.update({newChan.id: message.channel.id})
			#with open('jsonFiles/channels.json','w') as f:
			#	json.dump(channels, f)
			print(channels)
			pickle.dump( channels, open( "jsonFiles/channels.p", "wb" ) )
		
		content = (message.content if message.guild.id == admin_server else '**' + message.author.name +'**: ' + message.content)
		
		if content:
			if message.attachments:
				for k in message.attachments:
					await client.get_channel(channels[message.channel.id]).send(content = content, file = await k.to_file())
			else: 
				await client.get_channel(channels[message.channel.id]).send(content = content)
		#	await client.get_channel(channels[message.channel.id]).send_message(content)
		#if message.attachments:
		#	for k in message.attachments:
		#		_, file_ext = os.path.splitext(k['url'])
		#		await client.get_channel(channels[message.channel.id]).send(BytesIO(requests.get(k['url']).content), filename = 'file' + file_ext)

if __name__ == '__main__':
    #client.run(token)
	while True:
		try:
			client.loop.run_until_complete(client.start(token))
	
		except KeyboardInterrupt:
			client.loop.run_until_complete(client.logout())
			# cancel all tasks lingering
			raise
			#exit
		except BaseException:
			print('Retrying in 30 seconds...')
			time.sleep(30)

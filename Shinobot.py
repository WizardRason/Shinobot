import discord
import asyncio
import os
import requests
#import spice_api
#import html
from io import BytesIO
from discord.ext.commands import Bot
from discord.ext import commands
#import json
import random
import socket

from complexCommands import init
from complexCommands import rip
#from complexCommands import anime

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

init.init()

#with open('settings.json') as f:
#	settings = json.load(f)

client  = discord.Client()
echoing = True

cooldownTime = 15

# creds = spice_api.init_auth(settings["mal_username"], settings["mal_password"])

#                 WizardRason#6819
owner_user  = init.owner_user 	#settings["owner_user"]
token       = init.token 		#settings["token"]

secret_channel = init.secret_channel	#settings["secret_channel"]
public_channel = init.public_channel	#settings["public_channel"]

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
	await client.send_message(await client.get_user_info(owner_user), s.getsockname()[0])
	s.close()

async def deleteAfterTime(message, coolDown):
	await asyncio.sleep(coolDown)
	await client.delete_message(message)

@client.event
async def on_message(message):
	global public_channel
	global echoing
	
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
		msg_donut = await client.send_message(message.channel, random.choice(doughPhrases) + "\n" + random.choice(doughLinks))
		asyncio.ensure_future(deleteAfterTime(msg_donut, cooldownTime))

	#changes the public channel in which the bot comments
	if (echoing and message.channel.id == secret_channel and message.content.startswith('!swap')):
		echoing = False
		list_channels ='To which channel should I go?```'
		for k in client.get_channel(public_channel).server.channels:
			if (not type(k.bitrate) is int) and secret_channel != k.id:
				list_channels = list_channels + k.name + ':\t' + k.id + '\n'
		await client.send_message(message.channel, list_channels + '```')
		msg = await client.wait_for_message(author=message.author)
		for k in client.get_channel(public_channel).server.channels:
			invalid_channel = True
			if (k.name == msg.content or k.id == msg.content) and secret_channel != k.id:
				invalid_channel = False
				public_channel = k.id
				break
		if invalid_channel:
			await client.send_message(message.channel, 'Invalid Channel.')
		else:
			await client.send_message(message.channel, '__**Swapping to ' + client.get_channel(public_channel).name + '**__')
		echoing = True

	#posts a meme based on the given search term, or posts a default meme (meme.jpg)
	elif (message.content.startswith('!meme') and False): #not done yet
		if len(message.content.strip()) > 5:
			meme = message.content[5:]
			await client.send_message(message.channel, 'This is a meme. Searching the web for:' + meme)
		else:
			await client.send_file(message.channel, 'meme.jpg')

	#posts a gif of shinobu being carried
	elif (message.content.startswith('!adult')):
		await client.send_message(message.channel, 'I need an adult\n' + "https://thumbs.gfycat.com/BigheartedSplendidFlyingfish-size_restricted.gif")

	#!rip commands
	elif (message.content.startswith('!rip')):
		await rip.commandRip(message, client)
		
	#gives the link to the mal page of the given anime
	elif (message.content.startswith('!anime') or message.content.startswith('!manga')):
		#await (anime.commandAnime(message, client) if message.content[1] == 'a' else anime.commandManga(message, client))
		pass
		
	#posts everything (besides commands) said in public_channel into secret_channel, including who said it
	elif (echoing and (message.channel.id == secret_channel or message.channel.id == public_channel) and client.user.id != message.author.id):
		echoing = False
		goto_channel = (public_channel if message.channel.id == secret_channel else secret_channel)
		content =     (message.content if message.channel.id == secret_channel else '**' + message.author.name +'**: ' + message.content)
		if content:
			await client.send_message(client.get_channel(goto_channel), content)
		if message.attachments:
			for k in message.attachments:
				_, file_ext = os.path.splitext(k['url'])
				await client.send_file(client.get_channel(goto_channel), BytesIO(requests.get(k['url']).content), filename = 'file' + file_ext)
		echoing = True

if __name__ == '__main__':
    client.run(token)

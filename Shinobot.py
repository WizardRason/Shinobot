#pipreqs --encoding=utf8 .\Shinobot\ --force

import discord
import os
import random
import socket
import pickle
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, utils

from complexCommands import init
init.init()
from complexCommands import rip
#from complexCommands import anime

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

#client  = discord.Client()
client 	= commands.Bot(command_prefix="!", intents = discord.Intents.all())
slash 	= SlashCommand(client, sync_commands=True)
cooldownTime = 15

TestingGuildList = None 	#For Testing purposes, make into an array with single test guild id
TestingGuild = None 		#For Testing purposes, set to test guild id

#                 WizardRason#6819
owner_user  = init.owner_user 	#settings["owner_user"]
token       = init.token 		#settings["token"]

admin_server = init.admin_server	#settings["admin_server"]

#with open('jsonFiles/channels.json') as f:
try: channels = pickle.load( open( "jsonFiles/channels.p", "rb" ) )
except EOFError: channels = {}

@client.event
async def on_ready():
	print('Logged in as: '+ client.user.name + " (" + str(client.user.id) + ")")
	print("Owner User ID: " + str(owner_user))
	for server in client.guilds:
		print ("Connected to server: {}".format(server))
	print('-------')
	print("Bot Path: " + path)
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	print("Current IP of Bot: " + ip)
	channel = await client.fetch_user(owner_user)
	msg = await channel.history(limit=1).flatten()
	msg = msg[0].content
	if ip != msg:
		await channel.send(s.getsockname()[0])
	s.close()

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
			await message.channel.send([x for x in l if not '@' in x])
			if message.author.id == owner_user: await message.channel.send(l)
		else: await message.channel.send("None Saved")

	#posts everything said in public_channel into secret_channel, including who said it
	if (message.channel.type == discord.ChannelType.text and message.guild != client.get_guild(admin_server) or (client.user.id != message.author.id and message.channel.id in list(channels.keys()))):
		if message.channel.id not in list(channels.keys()) and message.guild != client.get_guild(admin_server):
			newChan = await client.get_guild(admin_server).create_text_channel(name = message.channel.name)
			channels.update({message.channel.id: newChan.id})
			channels.update({newChan.id: message.channel.id})
			print(channels)
			pickle.dump( channels, open( "jsonFiles/channels.p", "wb" ) )
		
		content = (message.content if message.guild.id == admin_server else '**' + message.author.name +'**: ' + message.content)
		
		if content:
			if message.attachments:
				for k in message.attachments:
					try: await client.get_channel(channels[message.channel.id]).send(content = content, file = await k.to_file())
					except AttributeError: pass
			else: 
				try: await client.get_channel(channels[message.channel.id]).send(content = content)
				except AttributeError: pass
'''
options = [
	{
		'name' 			: "optone",
		'description' 	: "This is the first option we have.",
		'required' 		: True,
		'type' 			: 3,
		'choices' 		: [
			{
				'name' 	: "ChoiceOne",
				'value' : "DOGE!"
			},
			{
				'name' 	: "ChoiceTwo",
				'value' : "NO DOGE"
			}
		]
	}
]

@slash.slash(name="test", description = "This is just a test command, nothing more.", guild_ids = TestingGuildList, options = options)
async def test(ctx: SlashContext, optone: str):
	global options
	embed = discord.Embed(title="embed test")
	await ctx.send(content=optone, embeds=[embed])
	await ctx.send(content="Here is a hidden message, just for you",hidden=True)
	#makes changes to the options variable(adding more choices) and updates the command
	options[0]['choices'].append({'name' : optone,'value' : "NO DOGE"})
	await utils.manage_commands.add_slash_command(bot_id=client.user.id,bot_token=token,guild_id=TestingGuild,cmd_name="test", description = "This is just a test command, nothing more.",options=options)
#'''
ripOptions = [
	{
		"name"			: "name",
		"description"	: "The 'rip' that you want",
		"required"		: False,
		"type"			: 3,
		'choices' 		: rip.ripChoicesList()
	}
]

ripAddOptions = [
	{
		"name"			: "name",
		"description"	: "The descriptive name of the new 'rip'",
		"required"		: True,
		"type"			: 3
	},
	{
		"name"			: "image",
		"description"	: "Is there an image you want to be posted with that 'rip'? (I'll ask what it is after)",
		"required"		: True,
		"type"			: 5
	},
	{
		"name"			: "phrase",
		"description"	: "The phrase that will be posted for that 'rip', but you don't need one",
		"required"		: False,
		"type"			: 3
	}
]

ripRemoveOptions = [
	{
		"name"			: "name",
		"description"	: "The 'rip' that you want to remove",
		"required"		: True,
		"type"			: 3,
		'choices' 		: rip.ripChoicesList()
	}
]

@slash.slash(name="rip", description = "A random rip phrase.", guild_ids = TestingGuildList, options = ripOptions)
async def Randomrip(ctx: SlashContext, name = None):
	await rip.commandRandomRip(name, ctx, owner_user)
	ripOptions[0]['choices'] = rip.ripChoicesList()
	await utils.manage_commands.add_slash_command(bot_id=client.user.id,bot_token=token,guild_id=TestingGuild,cmd_name="rip", description = "A random rip phrase.",options=ripOptions)

@slash.slash(name="ripadd", description = "Allows you to add to the rip phrases.", guild_ids = TestingGuildList, options = ripAddOptions)
async def Addrip(ctx: SlashContext, name: str, image: bool, phrase = None):
	await rip.commandAddRip(name, phrase, image, client, ctx, owner_user) 

@slash.slash(name="ripremove", description = "Removes a particular rip phrase (This is an owner command).", guild_ids = TestingGuildList, options = ripRemoveOptions)
async def Removerip(ctx: SlashContext, name : str):
	if(ctx.author_id == owner_user):
		await rip.commandRemoveRip(name, ctx)
	else: await ctx.send("Sorry, you don't have permission for that. Have some sparkles instead (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
	ripRemoveOptions[0]['choices'] = rip.ripChoicesList()
	await utils.manage_commands.add_slash_command(bot_id=client.user.id,bot_token=token,guild_id=TestingGuild,cmd_name="ripremove", description = "Removes a particular rip phrase.",options=ripRemoveOptions)

commandOptions = [
	{
		"name"			: "command",
		"description"	: "The command to perform",
		"required"		: True,
		"type"			: 3,
		'choices' 		: [{'name': k.split('.')[0], 'value' : k} for k in os.listdir(path + '/scripts/')]
	}
]

@slash.slash(name="command", description = "Executes the given command, (ownder commands start with @).", guild_ids = TestingGuildList, options = commandOptions)
async def command(ctx: SlashContext, command : str):

	scriptdir = path+"/scripts/"
	if os.path.exists('scripts/' + command) and (ctx.author_id == owner_user or "@" not in command):
		os.system(scriptdir + command)
		await ctx.send("Command Sent", hidden=True)
	else: await ctx.send("Sorry, you don't have permission for that. Have some sparkles instead (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
	commandOptions[0]['choices'] = [{'name': k.split('.')[0], 'value' : k} for k in os.listdir(path + '/scripts/')]
	await utils.manage_commands.add_slash_command(bot_id=client.user.id,bot_token=token,guild_id=TestingGuild,cmd_name="command", description = "Executes the given command, (ownder commands start with @).",options=commandOptions)


@slash.slash(name="adult", description = "I need an adult!", guild_ids = TestingGuildList)
async def Randomrip(ctx: SlashContext):
	await ctx.send('I need an adult!\n' + "https://thumbs.gfycat.com/BigheartedSplendidFlyingfish-size_restricted.gif")

if __name__ == '__main__':
	client.run(token)

import discord
import asyncio
import json
import bs4 as bs
import urllib.request
import spice_api
import html

from discord.ext.commands import Bot
from discord.ext import commands

from complexCommands import init

creds = spice_api.init_auth(init.username, init.password)

async def commandAnime(message, client):
	jojo = False
	if len(message.content.strip()) > 6:
		anime = message.content[6:].strip()
		if anime.isdigit():
			a = [spice_api.search_id(int(anime), spice_api.get_medium('anime'), creds)]
		else:
			a = spice_api.search(anime, spice_api.get_medium('anime'), creds)
	else:#default if none are given
		jojo = True
		a = [spice_api.search_id(14719, spice_api.get_medium('anime'), creds)]

	if a:
		temp = html.unescape(a[0].synopsis).replace('<br />','').replace('[b]','**').replace('[/b]','**').replace('[i]','*')
		temp2 = temp.replace('[/i]','*').replace('[u]','__').replace('[/u]','__').replace('[s]','~~').replace('[/s]','~~')
		if temp2.endswith(']'):
			desc = temp2.rsplit('[', 1)[0].rstrip('\n')
		elif temp2.endswith(')'):
			desc = temp2.rsplit('(', 1)[0].rstrip('\n')
		elif temp2.endswith('}'):
			desc = temp2.rsplit('{', 1)[0].rstrip('\n')
		else:
			desc = temp2.rstrip('\n')

		embed = discord.Embed(title=a[0].title, description=("**" + a[0].english + "**\n" + desc if a[0].english else desc), url='https://myanimelist.net/anime/' + a[0].id, color=0x2E51A2)
		#embed.set_image(url=a[0].image_url)
		embed.set_thumbnail(url=a[0].image_url)
		embed.set_author(name = a[0].anime_type)
		embed.add_field(name="Score", value=a[0].score)
		embed.add_field(name="Episodes", value=a[0].episodes)
		
		if jojo:
			await client.send_message(message.channel, 'You should watch Jojo:')
		await client.send_message(message.channel, embed=embed)
		#await client.send_message(message.channel, 'https://myanimelist.net/anime/' + a[0].id)
	else:
		await client.send_message(message.channel, 'Sorry, I didn\'t find anything')

async def commandManga(message, client):
	jojo = False
	if len(message.content.strip()) > 6:
		anime = message.content[6:].strip()
		if anime.isdigit():
			a = [spice_api.search_id(int(anime), spice_api.get_medium('manga'), creds)]
		else:
			a = spice_api.search(anime, spice_api.get_medium('manga'), creds)
	else:#default if none are given
		jojo = True
		#await client.send_message(message.channel, 'You should read Jojo:')# https://myanimelist.net/anime/14719/JoJo_no_Kimyou_na_Bouken_TV?q=jojo')
		a = [spice_api.search_id(3008, spice_api.get_medium('manga'), creds)]

	if a:
		temp = html.unescape(a[0].synopsis).replace('<br />','').replace('[b]','**').replace('[/b]','**').replace('[i]','*')
		temp2 = temp.replace('[/i]','*').replace('[u]','__').replace('[/u]','__').replace('[s]','~~').replace('[/s]','~~')
		if temp2.endswith(']'):
			desc = temp2.rsplit('[', 1)[0].rstrip('\n')
		elif temp2.endswith(')'):
			desc = temp2.rsplit('(', 1)[0].rstrip('\n')
		elif temp2.endswith('}'):
			desc = temp2.rsplit('{', 1)[0].rstrip('\n')
		else:
			desc = temp2.rstrip('\n')

		embed = discord.Embed(title=a[0].title, description=("**" + a[0].english + "**\n" + desc if a[0].english else desc), url='https://myanimelist.net/anime/' + a[0].id, color=0x2E51A2)
		#embed.set_image(url=a[0].image_url)
		embed.set_thumbnail(url=a[0].image_url)
		embed.set_author(name = a[0].manga_type)
		embed.add_field(name="Score", value=a[0].score)
		embed.add_field(name="Volumes", value=a[0].volumes).add_field(name="Chapters", value=a[0].chapters)
		if jojo:
			await client.send_message(message.channel, 'You should read Jojo:')
		await client.send_message(message.channel, embed=embed)
		#await client.send_message(message.channel, 'https://myanimelist.net/anime/' + a[0].id)
	else:
		await client.send_message(message.channel, 'Sorry, I didn\'t find anything')


# isAnime = (True if message.content[1] == 'a' else False)
# jojo = False
# if len(message.content.strip()) > 6:
# 	anime = message.content[6:].strip()
# 	if anime.isdigit():
# 		a = [spice_api.search_id(int(anime), spice_api.get_medium('anime' if isAnime else 'manga'), creds)]
# 	else:
# 		a = spice_api.search(anime, spice_api.get_medium('anime' if isAnime else 'manga'), creds)
# else:#default if none are given
# 	jojo = True
# 	if isAnime:
# 		#await client.send_message(message.channel, 'You should watch Jojo:')# https://myanimelist.net/anime/14719/JoJo_no_Kimyou_na_Bouken_TV?q=jojo')
# 		a = [spice_api.search_id(14719, spice_api.get_medium('anime'), creds)]
# 	else:
# 		#await client.send_message(message.channel, 'You should read Jojo:')# https://myanimelist.net/anime/14719/JoJo_no_Kimyou_na_Bouken_TV?q=jojo')
# 		a = [spice_api.search_id(3008, spice_api.get_medium('manga'), creds)]

# if a:
# 	temp = html.unescape(a[0].synopsis).replace('<br />','').replace('[b]','**').replace('[/b]','**').replace('[i]','*')
# 	temp2 = temp.replace('[/i]','*').replace('[u]','__').replace('[/u]','__').replace('[s]','~~').replace('[/s]','~~')
# 	if temp2.endswith(']'):
# 		desc = temp2.rsplit('[', 1)[0].rstrip('\n')
# 	elif temp2.endswith(')'):
# 		desc = temp2.rsplit('(', 1)[0].rstrip('\n')
# 	elif temp2.endswith('}'):
# 		desc = temp2.rsplit('{', 1)[0].rstrip('\n')
# 	else:
# 		desc = temp2.rstrip('\n')

# 	embed = discord.Embed(title=a[0].title, description=("**" + a[0].english + "**\n" + desc if a[0].english else desc), url='https://myanimelist.net/anime/' + a[0].id, color=0x2E51A2)
# 	#embed.set_image(url=a[0].image_url)
# 	embed.set_thumbnail(url=a[0].image_url)
# 	embed.set_author(name = a[0].anime_type if isAnime else a[0].manga_type)
# 	embed.add_field(name="Score", value=a[0].score)
# 	if isAnime:
# 		embed.add_field(name="Episodes", value=a[0].episodes)
# 	else:
# 		embed.add_field(name="Volumes", value=a[0].volumes).add_field(name="Chapters", value=a[0].chapters)
# 	if jojo:
# 		await client.send_message(message.channel, 'You should ' + ("watch" if isAnime else "read") + ' Jojo:')
# 	await client.send_message(message.channel, embed=embed)
# 	#await client.send_message(message.channel, 'https://myanimelist.net/anime/' + a[0].id)
# else:
# 	await client.send_message(message.channel, 'Sorry, I didn\'t find anything')


#https://www.reddit.com/r/learnpython/comments/687y53/scraping_myanimelist_to_get_anime_genres/
def genre_scrape(message_link):

	src = urllib.request.urlopen(message_link).read()
	soup = bs.BeautifulSoup(src, 'lxml')

	genre_list = [x.text for x in soup.select('a[href^="/anime/genre/"]')]
	return genre_list
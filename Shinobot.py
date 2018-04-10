import discord
import asyncio
import os
import requests
import spice_api
import html
from io import BytesIO
from discord.ext.commands import Bot
from discord.ext import commands
import json
import random
import socket

import init

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

init.init()

with open('settings.json') as f:
    settings = json.load(f)

client  = discord.Client()
echoing = True
rip_cooldown = []
cooldownTime = 15

creds = spice_api.init_auth(settings["mal_username"], settings["mal_password"])

#                 WizardRason#6819
owner_user  = settings["owner_user"]
token       = settings["token"]

secret_channel = settings["secret_channel"]
public_channel = settings["public_channel"]

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

@client.event
async def on_message(message):
    global public_channel
    global echoing
    global rip_cooldown

    if any(x in message.content.lower() for x in ["doughnut", "donut"]):
        try:
            pid = os.fork()
        except OSError:
            exit("Could not create a child process")
        if pid == 0:
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
            msg = await client.send_message(message.channel, random.choice(doughPhrases) + "\n" + random.choice(doughLinks))
            await asyncio.sleep(cooldownTime)
            await client.delete_message(msg)
            exit()

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
        await client.send_message(message.channel, 'I need an adult\n' + "https://vignette.wikia.nocookie.net/bakemonogatari1645/images/a/af/Tumblr_n4guqbYjFN1txc8l9o1_500.gif/revision/latest?cb=20150918011928")

    #adds to the rip_map
    elif (message.content.startswith('!ripadd')): #allow for multiple quotes per picture
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

    #pm the message auther with a list of all "rip"s
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

    #gives the link to the mal page of the given anime
    elif (message.content.startswith('!anime') or message.content.startswith('!manga')):
        isAnime = (True if message.content[1] == 'a' else False)
        jojo = False;
        if len(message.content.strip()) > 6:
            anime = message.content[6:].strip()
            if anime.isdigit():
                a = [spice_api.search_id(int(anime), spice_api.get_medium('anime' if isAnime else 'manga'), creds)]
            else:
                a = spice_api.search(anime, spice_api.get_medium('anime' if isAnime else 'manga'), creds)
        else:#default if none are given
            jojo = True
            if isAnime:
                #await client.send_message(message.channel, 'You should watch Jojo:')# https://myanimelist.net/anime/14719/JoJo_no_Kimyou_na_Bouken_TV?q=jojo')
                a = [spice_api.search_id(14719, spice_api.get_medium('anime'), creds)]
            else:
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
            embed.set_author(name = a[0].anime_type if isAnime else a[0].manga_type)
            embed.add_field(name="Score", value=a[0].score)
            if isAnime:
                embed.add_field(name="Episodes", value=a[0].episodes)
            else:
                embed.add_field(name="Volumes", value=a[0].volumes).add_field(name="Chapters", value=a[0].chapters)
            if jojo:
                await client.send_message(message.channel, 'You should ' + ("watch" if isAnime else "read") + ' Jojo:')
            await client.send_message(message.channel, embed=embed)
            #await client.send_message(message.channel, 'https://myanimelist.net/anime/' + a[0].id)
        else:
            await client.send_message(message.channel, 'Sorry, I didn\'t find anything')

    #posts everything (besides commands) said in public_channel into secret_channel, including who said it
    elif (echoing and (message.channel.id == secret_channel or message.channel.id == public_channel) and client.user.id != message.author.id):
        echoing = False
        goto_channel = (public_channel if message.channel.id == secret_channel else secret_channel)
        content =     (message.content if message.channel.id == secret_channel else '**' + message.author.name +'**: ' + message.content)
        if content:
            await client.send_message(client.get_channel(goto_channel), content)
        if message.attachments:
            for k in message.attachments:
                filename, file_ext = os.path.splitext(k['url'])
                await client.send_file(client.get_channel(goto_channel), BytesIO(requests.get(k['url']).content), filename = 'file' + file_ext)
        echoing = True

client.run(token)

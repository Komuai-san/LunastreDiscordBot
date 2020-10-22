import discord
from discord.ext import commands
import random
import requests
import json
import pafy
import asyncio
import basc_py4chan as chan
import long
from udpy import UrbanClient
import wikipedia
import dateutil.parser


shoes = long.sneakers()
udclient = UrbanClient()
client = commands.Bot(command_prefix="!")

client.thetitle = ""

def listToString(s):
    str1 = "\n \n"
    return (str1.join(s).replace(" & ", " AND "))

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_message(message):
    if message.embeds:
        for content in message.embeds:
            client.thetitle = content.title 
            await client.process_commands(message)
    else:
        await client.process_commands(message)
    
@client.command()
async def hello(ctx):
    await ctx.send("Hello there!")

@client.command()
async def dogs(ctx):
    DOG_URL = 'http://api.thedogapi.com/v1/images/search'
    DOG_API_KEY = '3b392042-b329-4b00-a6f6-b14d3b585396'
    DOG_HEADERS = { 'x-api-key': DOG_API_KEY  }
    IMG_PARAMS = ['jpg,png', 'gif',]
    params = {"mime_types": random.choice(IMG_PARAMS)}
    thedog = requests.request("GET", DOG_URL, params=params, headers= DOG_HEADERS).json()
    embed = discord.Embed(color=0xffffff)
    embed.set_image(url=thedog[0]['url'])
    await ctx.send(embed=embed)

@client.command()
async def cats(ctx):
    CAT_URL = 'http://api.thecatapi.com/v1/images/search'
    CAT_API_KEY = 'fccdd277-481e-4ce8-91f6-74494640b167'
    CAT_HEADERS = { 'x-api-key': CAT_API_KEY  }
    IMG_PARAMS = ['jpg,png', 'gif',]
    params = {"mime_types": random.choice(IMG_PARAMS)}
    thecat = requests.request("GET", CAT_URL, params=params, headers= CAT_HEADERS).json()
    embed = discord.Embed(color=0xffffff)
    embed.set_image(url=thecat[0]['url'])
    await ctx.send(embed=embed)

@client.command()
async def djoke(ctx):
    url = 'https://icanhazdadjoke.com/'
    headers =  { 'Accept': 'application/json' }
    thejoke = requests.request("GET", url, headers=headers).json()
    embed = discord.Embed(title="Dad Joke", description= thejoke['joke'], color=0xffffff)
    await ctx.send(embed=embed)

@client.command()
async def ytdl(ctx, *, message):
    #title = client.thetitle
    video = pafy.new(message)
    filenom = video.title + ".m4a"
    audio = video.getbestaudio(preftype="m4a")
    file = audio.download()
    channel = ctx.message.channel
    mainfile = discord.File(filenom)
    await ctx.send("Here you go.", file=mainfile)

@client.command()
async def fourch(ctx):
    boardlist = ['g', 'pol', 'tv', 'a', 'x', 'jp', 'lit']
    boardcounter = random.choice(boardlist)
    boards = chan.Board(boardcounter)
    allthreads = boards.get_all_threads(expand=False)
    thelist = []

    try:
        while True:
            thread = random.choice(allthreads)

            for r in thread.replies:
                if r.has_file == True:
                    thelist.append(r.text_comment)
                    thelist.append(r.file_url)

            if not thelist:
                continue

            else:
                break
                
        embed = discord.Embed(title="4chan " + "/" + boardcounter + "/", description=thelist[0], color=0xffffff)
        embed.set_image(url=thelist[1])
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(e)    

@client.command()
async def quotes(ctx):
    url = 'https://api.quotable.io/random'
    quote = requests.get(url).json()
    embed = discord.Embed(title="Inspirational Quote", description=quote['content'] + " - " + quote['author'], color=0xffffff)
    await ctx.send(embed=embed)


@client.command()
async def mshoes(ctx):
    menshoes = shoes.getShoes("mshoes")
    imgurl = menshoes.pop()
    embed = discord.Embed(title="Random Shoe", description=listToString(menshoes), color=0xffffff)
    embed.set_image(url=imgurl)
    await ctx.send(embed=embed)

@client.command()
async def fshoes(ctx):
    femshoes = shoes.getShoes("wshoes")
    imgurl = femshoes.pop()
    embed = discord.Embed(title="Random Shoe", description=listToString(femshoes), color=0xffffff)
    embed.set_image(url=imgurl)
    await ctx.send(embed=embed)


@client.command()
async def urban(ctx, *, msg):
    try:
        defenesyon = udclient.get_definition(msg)
        orban = []

        for index, d in enumerate(defenesyon):
            orban.append(str(index+1) + "). " + d.definition)

            if index == 4:
                break

        embed = discord.Embed(title=msg, description=listToString(orban), color=0xffffff)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(e)

@client.command()
async def urand(ctx):
    try:
        defenesyon = udclient.get_random_definition()
        orban = []
        word = []

        for index, d in enumerate(defenesyon):
            orban.append(str(index + 1) + "). " + d.definition)
            word.append(d.word)

            if index == 4:
                break

        embed = discord.Embed(title=listToString(word), description=listToString(orban), color=0xffffff)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(e)


@client.command()
async def news(ctx):
    thenews = long.getNews()
    img = thenews.pop()
    #embed = discord.Embed(color=0xffffff)
    #embed.set_image(url=img)
    await ctx.send(thenews[0])


@client.command()
async def corona(ctx):
    url = 'https://covid-193.p.rapidapi.com/statistics'
    querystring = { "country": "Philippines" }

    headers = {
        'x-rapidapi-host': 'covid-193.p.rapidapi.com',
        'x-rapidapi-key': 'be7f37114bmsh38c0486c35a5050p1bc1e5jsnf574155ad041'
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    data = response['response']
    d = data[0]
    disease = ['All: ' + str(d['cases']['total']), 'Recovered: ' + str(d['cases']['recovered']), 'Deaths: ' + str(d['deaths']['total']), 'New: ' + str(d['cases']['new']), 'Critical: ' + str(d['cases']['critical']), 'Time: ' + (str(dateutil.parser.parse(d['time'])))]

    await ctx.send("Let's hope that the virus ends as soon as possible. Here is the latest report in the Philippines:" + "\n \n" + listToString(disease))


@client.command()
async def wlist(ctx, *, msg):
    try:
        wiki_results = wikipedia.search(msg)
        text = "Here are the results for {}: ".format(msg)
        wikilist = []
        for results in wiki_results:
            try:
                wikilist.append(wikipedia.page(results).url)

            except: 
                pass

        await ctx.send(text + "\n \n" + listToString(wikilist))

    except:
        await ctx.send("It looks like an error occurred!")

@client.command()
async def wiki(ctx, *, msg):
    try:
        wigi = msg
        thewik = wikipedia.summary(str(wigi), sentences=3)
        thelink = wikipedia.page(str(wigi))
        await ctx.send("**Wikipedia Article For:** " + msg + "\n\n" + thewik + "\n\n **Link/Read More:** \n\n" + thelink.url)

    except Exception as e: 
        await ctx.send(e)






client.run("NzYxOTU5MjExMDE3ODMwNDQw.X3iL0A.uHpFCKj4QY42-Zqn4SFXtuJwhZA")
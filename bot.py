# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
import random
import requests
import os
import json
import pafy
import asyncio
import basc_py4chan as chan
import long
from PIL import ImageEnhance
from udpy import UrbanClient
import wikipedia
import dateutil.parser
import config
from PIL import Image
import praw
import pybooru
import youtube_dl
import topiclist

make = long.makeup()

reddit = praw.Reddit(client_id = config.client_id,
                     client_secret = config.client_secret,
                     username = config.username,
                     password = config.password,
                     user_agent = config.user_agent)

shoes = long.sneakers()
udclient = UrbanClient()
client = commands.Bot(command_prefix="~")
client.remove_command("help")

status = ["with myself.", "Reading War and Peace.", "Practicing my juggling skills"]

client.thetitle = ""




def deepfried(img):
    # Generate color overlay
    overlay = img.copy()
    overlay = ImageEnhance.Contrast(overlay).enhance(random.uniform(0.7, 1.8))
    overlay = ImageEnhance.Brightness(overlay).enhance(random.uniform(0.8, 1.3))
    overlay = ImageEnhance.Color(overlay).enhance(random.uniform(0.7, 1.4))

    # Blend random colors onto and sharpen the image
    img = Image.blend(img, overlay, random.uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(random.randint(5, 200))

    return img

def listToString(s):
    str1 = "\n \n"
    return (str1.join(s).replace(" & ", " AND "))

@client.event
async def on_ready():
    change_status.start()
    print("Bot is ready")

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(random.choice(status)))

@client.event
async def on_message(message):
    if message.embeds:
        for content in message.embeds:
            client.thetitle = content.title 
            await client.process_commands(message)
    else:
        await client.process_commands(message)

#MOD
@client.command()
@commands.has_permissions(manage_channels = True)
async def lock(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send(ctx.channel.mention + " ***is now under siege, under lockdown.***")
    except:
        await ctx.send("I don't have permission to do this!")

@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
        await ctx.send(ctx.channel.mention + " ***is now unlocked.***")
    except:
        await ctx.send("I don't have permission to do this!")

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, *, msg):
    try:
        await ctx.send("Messages Purged: {}".format(msg))
        await ctx.channel.purge(limit=int(msg) + 1)

    except:
        await ctx.send("I didn't receive a number! Or I don't have permission to do this.")
    
@client.command()
@commands.has_permissions(ban_members=True, kick_members=True)
async def kick(ctx, member : discord.Member, *, msg):
    try:
        if ctx.message.author.server_permissions.administrator:
            await member.kick(reason=msg)
            await ctx.send(f'Yeeted {member.mention}')
        else:
            await ctx.send("Sorry, you're not an administrator.")

    except:
        await ctx.send("Member not found, or I don't have any permissions to do this.")

@client.command()
@commands.has_permissions(ban_members=True, kick_members=True)
async def ban(ctx, member : discord.Member, *, msg):
    try:
        if ctx.message.author.server_permissions.administrator:
            await member.ban(reason=msg)
            await ctx.send(f'Banned {member.mention}!!!')

        else:
            await ctx.send("Sorry, you're not an administrator.")
    except:
        await ctx.send("Member not found, or I don't have any permissions to do this.")

@client.command()
@commands.has_permissions(ban_members=True, kick_members=True)
async def unban(ctx, *, member):
    try:
        if ctx.message.author.server_permissions.administrator:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split()

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f'Ubanned {user.mention}!')
                    return 
        else:
            await ctx.send("Sorry, you're not an administrator.")

    except:
        await ctx.send("User not found, or I don't have permissions to do this!")

@client.command()
async def super(ctx, member : discord.Member):
    try:
        index = 0
        while index <= 14:
            await ctx.send(member.mention)
            index +=1 
    except:
        await ctx.send("User not found!")

@client.command()
@commands.has_permissions(manage_channels = True)
async def mute(ctx, member : discord.Member):
    try:
        guild = ctx.guild

        for role in guild.roles:
            if role.name == "Muted":
                await member.add_roles(role)
                await ctx.send("{} has been muted by {}".format(member.mention, ctx.author.mention))
                return

                overwrite = discord.PermissionOverwrite(send_messages=False)
                newRole = await guild.create_role(name="Muted")

                for channel in guild.text_channels:
                    await channel.set_permissions(newRole, overwrite=overwrite)

                await member.add_roles(newRole)
                await ctx.send("{} has been muted by {}".format(member.mention, ctx.author.mention))

    except:
        await ctx.send("User not found, or I don't have the permissions.")

@client.command()
@commands.has_permissions(manage_channels = True)
async def unmute(ctx, member : discord.Member):
    try:
        guild = ctx.guild

        for role in guild.roles:
            if role.name == "Muted":
                await member.remove_roles(role)
                await ctx.send("{} has been unmuted by {}".format(member.mention, ctx.author.mention))
                return

    except:
        await ctx.send("Member must be an administrator or I don't have permission to do that!")


@client.command()   
async def hello(ctx):
    await ctx.send("Hello there!")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="I really love doing useless things.", description=topiclist.helptext, color=0xff00ff)
    await ctx.send(embed=embed)

@client.command()
async def advice(ctx):
    url = "https://api.adviceslip.com/advice"
    advice = requests.get(url).json()
    await ctx.send(advice['slip']['advice'])

@client.command(name='ping', help="This command returns the latency.")
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

@client.command(name='dogs', help="I'll return a random dog pic/gif")
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

@client.command(name="cats", help="Returns a random cat pic/gif")
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
async def bnw(ctx):
    try:
        thename = ctx.message.attachments[0].filename
        bnwname = "bw_" + str(thename)
        await ctx.message.attachments[0].save(thename)

        img = Image.open(thename)
        blackAndWhite = img.convert("L")
        blackAndWhite.save(bnwname)
        theFile = discord.File(bnwname)
        await ctx.send("Here you go.", file=theFile)

    except:
        await ctx.send("I need an attached file to make this work 🤡")

    #finalname = "bw_" + str(attachment_url)
    #file_request = requests.get(attachment_url)

@client.command()
async def meme(ctx):
    url = "https://no-api-key.com/api/v1/memes"
    memes = requests.get(url).json()
    embed = discord.Embed(title="Random Meme", color=0xff00ff)
    embed.set_image(url=memes['image'])
    await ctx.send(embed=embed)

@client.command()
async def deepfry(ctx):
    try:
        thename = ctx.message.attachments[0].filename
        deep = "deep_" + str(thename)
        await ctx.message.attachments[0].save(thename)

        img = Image.open(thename)
        theimg = deepfried(img)

        theimg.save(deep)

        mainFile = discord.File(deep)

        await ctx.send("Here you go.", file=mainFile)

    except:
        await ctx.send("I need an attached file to make this work 🤡")

@client.command()
async def topic(ctx):
    topics = [random.choice(topiclist.randlist), random.choice(topiclist.randlist2), random.choice(topiclist.resto), random.choice(topiclist.together), random.choice(topiclist.family), random.choice(topiclist.adults), random.choice(topiclist.kids), random.choice(topiclist.deep)]
    await ctx.send(random.choice(topics))

@client.command(name="djoke", help="This returns a dad joke.")
async def djoke(ctx):
    url = 'https://icanhazdadjoke.com/'
    headers =  { 'Accept': 'application/json' }
    thejoke = requests.request("GET", url, headers=headers).json()
    embed = discord.Embed(title="Dad Joke", description= thejoke['joke'], color=0xffffff)
    await ctx.send(embed=embed)

@client.command(name="youtube", help="Send a Youtube link and I'll return an m4a audio file.")
async def youtube(ctx, *, message):
    #title = client.thetitle
    video = pafy.new(message)
    filenom = video.title + ".m4a"
    audio = video.getbestaudio(preftype="m4a")
    file = audio.download()
    channel = ctx.message.channel
    mainfile = discord.File(filenom)
    await ctx.send("Here you go.", file=mainfile)

@client.command(name="fourch", help="Sends a random 4chan comment from various boards.")
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

@client.command(name="quotes", help="Returns an inspirational quote from famous figures.")
async def quotes(ctx):
    url = 'https://api.quotable.io/random'
    quote = requests.get(url).json()
    embed = discord.Embed(title="Inspirational Quote", description=quote['content'] + " - " + quote['author'], color=0xffffff)
    await ctx.send(embed=embed)


@client.command(name="mshoes", help="Returns a random, newly-released pair of men's shoes.")
async def mshoes(ctx):
    menshoes = shoes.getShoes("mshoes")
    imgurl = menshoes.pop()
    embed = discord.Embed(title="Random Shoe", description=listToString(menshoes), color=0xffffff)
    embed.set_image(url=imgurl)
    await ctx.send(embed=embed)

@client.command(name="fshoes", help="Returns a random, newly-released pair of women's shoes.")
async def fshoes(ctx):
    femshoes = shoes.getShoes("wshoes")
    imgurl = femshoes.pop()
    embed = discord.Embed(title="Random Shoe", description=listToString(femshoes), color=0xffffff)
    embed.set_image(url=imgurl)
    await ctx.send(embed=embed)


@client.command(name="flip", help="Flips a coin.")
async def flip(ctx):
    coin = ['heads', 'tails']
    await ctx.send("I flipped a coin and it's {}".format(random.choice(coin)))



@client.command(name="urban", help="Add it with a word you want to search, and I'll return its urban definition.")
async def urban(ctx, *, msg):
    try:
        defenesyon = udclient.get_definition(msg)
        orban = []

        for index, d in enumerate(defenesyon):
            orban.append(str(index+1) + "). " + d.definition)

            if index == 4:
                break

        embed = discord.Embed(title=msg, description=listToString(orban), color=0xffffff)
        #embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(e)

#NO API COMMANDS
@client.command()
async def simp(ctx):
    thename = ctx.message.attachments[0].url
    url = 'https://api.no-api-key.com/api/v2/simpcard?image=' + thename
    embed = discord.Embed(title="SIMP", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def crap(ctx):
    thename = ctx.message.attachments[0].url
    url = 'https://api.no-api-key.com/api/v2/crap?stepped=' + thename
    embed = discord.Embed(title="SHIT", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def smart(ctx):
    thename = ctx.message.attachments[0].url
    url = 'https://api.no-api-key.com/api/v2/smrt?image=' + thename
    embed = discord.Embed(title="Matalino", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def timeout(ctx):
    thename = ctx.message.attachments[0].url
    url = 'https://api.no-api-key.com/api/v2/timeout?image=' + thename
    embed = discord.Embed(title="TIMEOUT", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def trash(ctx):
    thename = ctx.message.attachments[0].url
    url = 'https://api.no-api-key.com/api/v2/trash?image=' + thename
    embed = discord.Embed(title="TRASH", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def rip(ctx):
    thename = ctx.message.attachments[0].url
    url = 'https://api.no-api-key.com/api/v2/rip?image=' + thename
    embed = discord.Embed(title="REST IN PEACE", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def punch(ctx):
    thename = ctx.message.attachments[0].url
    url = 'https://api.no-api-key.com/api/v2/punch?punch=' + thename
    embed = discord.Embed(title="PUNCHED", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def kicked(ctx):
    thename = ctx.message.attachments[0].url
    url = 'https://api.no-api-key.com/api/v2/punch?kicked=' + thename
    embed = discord.Embed(title="KICKED", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)


@client.command()
async def shoot(ctx):
    thename = ctx.message.attachments[0].url
    url = 'https://api.no-api-key.com/api/v2/shoot?image=' + thename
    embed = discord.Embed(title="SIMP", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def trump(ctx, *, msg):
    msg = msg.replace(" ", "%20")
    url = 'https://api.no-api-key.com/api/v2/trump?message=' + msg
    embed = discord.Embed(title="Important tweet", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command()
async def captcha(ctx, *, msg):
    msg = msg.replace(" ", "%20")
    url = 'https://api.no-api-key.com/api/v2/recaptcha?text=' + msg
    embed = discord.Embed(title="Important tweet", color=0xff00ff)
    embed.set_image(url=url)
    await ctx.send(embed=embed)

@client.command(name="zalgofy", help="Send some text and I'll fuck it up!")
async def zalgofy(ctx, *, text):
    
    zal_chars = ' ̷̡̛̮͇̝͉̫̭͈͗͂̎͌̒̉̋́͜ ̵̠͕͍̩̟͚͍̞̳̌́̀̑̐̇̎̚͝ ̸̻̠̮̬̻͇͈̮̯̋̄͛̊͋̐̇͝͠ ̵̧̟͎͈̪̜̫̪͖̎͛̀͋͗́̍̊͠ ̵͍͉̟͕͇͎̖̹̔͌̊̏̌̽́̈́͊ͅ ̷̥͚̼̬̦͓͇̗͕͊̏͂͆̈̀̚͘̚ ̵̢̨̗̝̳͉̱̦͖̔̾͒͊͒̎̂̎͝ ̵̞̜̭̦̖̺͉̞̃͂͋̒̋͂̈́͘̕͜ ̶̢̢͇̲̥̗̟̏͛̇̏̊̑̌̔̚ͅͅ ̷̮͖͚̦̦̞̱̠̰̍̆̐͆͆͆̈̌́ ̶̲͚̪̪̪͍̹̜̬͊̆͋̄͒̾͆͝͝ ̴̨̛͍͖͎̞͍̞͕̟͑͊̉͗͑͆͘̕ ̶͕̪̞̲̘̬͖̙̞̽͌͗̽̒͋̾̍̀ ̵̨̧̡̧̖͔̞̠̝̌̂̐̉̊̈́́̑̓ ̶̛̱̼̗̱̙͖̳̬͇̽̈̀̀̎̋͌͝ ̷̧̺͈̫̖̖͈̱͎͋͌̆̈̃̐́̀̈'.replace(" ", "")
    
    
    zalgo_text = ""
    
    for letter in text:
        if letter == " ":
            zalgo_text += letter
            continue

        letter += random.choice(zal_chars)
        letter += random.choice(zal_chars)
        letter += random.choice(zal_chars)
        zalgo_text += letter

    
    
    await ctx.send(zalgo_text)

@client.command(name="emojify", help="Send some text and I'll emoji the shit out of it. 🅱️")
async def emojify(ctx, *, text):
    emoji = list("😂😝🤪🤩😤🥵🤯🥶😱🤔😩🙄💀👻🤡😹👀👁👌💦🔥🌚🌝🌞🔫💯")
    b_emoji = "🅱️"
    a_emoji = "🅰️"
    i_emoji = "ℹ️"

    text = text.replace("ab", "🆎")
    text = text.replace("cl", "🆑")
    text = text.replace("b", "🅱️")
    text = text.replace("a", "🅰️")
    text = text.replace("i", "ℹ️")
    text = text.replace("AB", "🆎")
    text = text.replace("CL", "🆑")
    text = text.replace("B", "🅱️")
    text = text.replace("A", "🅰️")
    text = text.replace("I", "ℹ️")

    emoji_text = ""

    for letter in text:
        if letter == " ":
            emoji_text += random.choice(emoji)
        else:
            emoji_text += letter

    await ctx.send(emoji_text)
    
@client.command(name="cheemify", help="Ever wonder how your text will sound if Cheems spoke it? Why not try this one.")
async def cheemify(ctx, *, text):
    text = text.replace("ese", "ms")
    text = text.replace("se", "mse")
    text = text.replace("ck", "mk")
    text = text.replace("ake", "amke")
    text = text.replace("as", "ams")
    text = text.replace("n", "m")
    text = text.replace("ab", "amb")
    text = text.replace("lp", "lmp")
    text = text.replace("ke", "mke")
    text = text.replace("ec", "emc")
    text = text.replace("ig", "img")
    text = text.replace("ob", "omb")
    text = text.replace("pep", "pemp")
    text = text.replace("pop", "pomp")
    text = text.replace("rib", "rimb")

    await ctx.send(text)

@client.command(name="owofy", help="Imma convert your text into owo. You know, that cringy anime shit.")
async def owofy(ctx, *, text):
    owo_faces = "owo uwu owu uwo u-u o-o OwO UwU @-@ ;-; ;_; ._. (._.) (o-o) ('._.) (｡◕‿‿◕｡)" \
    " (｡◕‿◕｡) (─‿‿─) ◔⌣◔ ◉_◉".split(sep=" ")

    text = text.replace("r", "w")
    text = text.replace("R", "W")
    text = text.replace("n", "ny")
    text = text.replace("N", "NY")
    text = text.replace("ll", "w")
    text = text.replace("LL", "W")
    text = text.replace("l", "w")
    text = text.replace("L", "W")

    text += f" {random.choice(owo_faces)}"

    await ctx.send(text)

@client.command(name="av", help="Returns avatar.")
async def av(ctx, user: discord.User):
    try:
        embed = discord.Embed(title=str(user.name) + "'s Avatar: ", color=0xffffff)
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("Mention the guy, my guy. 🅱️")

@client.command(name="urand", help="Returns a random urban dictionary definition.")
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
        #embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(e)


@client.command(name="news", help="Returns a random news from BBC.")
async def news(ctx):
    thenews = long.getNews()
    img = thenews.pop()
    #embed = discord.Embed(color=0xffffff)
    #embed.set_image(url=img)
    await ctx.send(thenews[0])


@client.command(name="corona", help="Returns the latest Coronavirus news in the Philippines")
async def corona(ctx, *, msg):
    try:
        url = 'https://covid-193.p.rapidapi.com/statistics'
        querystring = { "country": msg }

        headers = {
            'x-rapidapi-host': 'covid-193.p.rapidapi.com',
            'x-rapidapi-key': 'be7f37114bmsh38c0486c35a5050p1bc1e5jsnf574155ad041'
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()
        data = response['response']
        d = data[0]
        disease = ['\n\n**All:** ' + str(d['cases']['total']), '**Recovered:** ' + str(d['cases']['recovered']), '**Deaths:** ' + str(d['deaths']['total']), '**New:** ' + str(d['cases']['new']), '**Critical:** ' + str(d['cases']['critical']), '**Time:** ' + (str(dateutil.parser.parse(d['time'])))]
        embed = discord.Embed(title="**" + msg + " Coronavirus Updates as of {}".format((str(dateutil.parser.parse(d['time'])))) +"**", description=listToString(disease))
        await ctx.send(embed=embed)

    except:
        await ctx.send("I might have received nothing. I need a country!")


@client.command(name="wlist", help="Returns a list of Wikipedia articles based on your query.")
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

@client.command(name="wiki", help="Returns a single Wikipedia article about said query.")
async def wiki(ctx, *, msg):
    try:
        wigi = msg
        thewik = wikipedia.summary(str(wigi), sentences=3)
        thelink = wikipedia.page(str(wigi))
        try:
            theimg = thelink.images[random.randit(0, 3)]
        except:
            theimg = thelink.images[0]

        embed = discord.Embed(title="**Wikipedia Article For: "+ msg + "**", description=thewik + "\n\n **Link/Read More:** \n\n" + "<" + thelink.url + ">", color=0xffffff)
        try:
            embed.set_image(url=theimg)
        except:
            pass
        
        await ctx.send(embed=embed)

    except Exception as e: 
        await ctx.send(e)

#REDDIT
@client.command()
async def rrising(ctx):
    try:
        thesub = reddit.random_subreddit()
        submission = thesub.rising()

        for index, subs in enumerate(submission):
            await ctx.send(subs.title + "\n \n" + subs.selftext + "\n" + subs.url)
            if index == 5:
                break
    
    except:
        await ctx.send("There seems to be an error.")

@client.command()
async def rsubpost(ctx):
    try:
        thesub = reddit.random_subreddit()
        submission = thesub.random()
        embed = discord.Embed(title=submission.title, description=submission.selftext + "\n" + submission.url, color=0xffffff)
        
        if submission.url[-3:] == "jpg" or submission.url[-3:] == "png" or submission.url[-3:] == "gif":
            embed.set_image(url=submission.url)

        await ctx.send(embed=embed)


    except:
        await ctx.send("There seems to be an error.")


@client.command(name="rrand", help="I'll return a single random reddit post from your desired subreddit.")
async def rrand(ctx, *, msg):
    try:
        submission = reddit.subreddit(msg).random()
        embed=discord.Embed(title=submission.title, description=submission.selftext + "\n" + submission.url, color=0xffffff)
        
        if submission.url[-3:] == "jpg" or submission.url[-3:] == "png" or submission.url[-3:] == "gif":
            embed.set_image(url=submission.url)
        
        embed.set_footer(text="Command invoked by {}".format(ctx.message.author.name))
        
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(e)

@client.command(name="dict", help="I'll return a dictionary definition from your desired word.")
async def dict(ctx, *, msg):
    dictlogic = long.googledict()
    try:
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en/' + msg
        response = requests.get(url).json()
        words = dictlogic.parsetext(response)
        words[0] = "**" + words[0] + "**"
        embed = discord.Embed(title="", description=listToString(words), color=0xffffff)
        embed.set_footer(text="Command invoked by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(e)

@client.command(name="rhot", help="Returns 5 hottest posts from your desired subreddit.")
async def rhot(ctx, *, msg):
    redditlogic = long.reddit()
    try:
        subreddit = reddit.subreddit(msg)
        hot = subreddit.hot(limit=5)
        redlist = redditlogic.hotornew(hot)
        await ctx.send("Here are the hottest topics at " + msg + ": " + "\n\n" + listToString(redlist))

    except Exception as e:
        await ctx.send(e)

@client.command(name="rnew", help="Returns 5 new posts from your desired subreddit.")
async def rnew(ctx, *, msg):
    redditlogic = long.reddit()
    try:
        subreddit = reddit.subreddit(msg)
        new = subreddit.new(limit=5)
        redlist = redditlogic.hotornew(new)
        await ctx.send("Here are the hottest topics at " + msg + ": " + "\n\n" + listToString(redlist))

    except Exception as e:
        await ctx.send(e)


@client.command(name="rnsfw", help="Returns an **NSFW** reddit post.")
async def rnsfw(ctx):
    try:
        if ctx.channel.is_nsfw():
            thesub = reddit.random_subreddit(nsfw=True)
            submission = thesub.random()
            await ctx.send(submission.title + "\n" + submission.selftext + "\n" + submission.url)
        
        else:
            await ctx.send("There must be an error or this might be a non-NSFW channel.")
    
    except:
        await ctx.send("There must be an error in general")

@client.command(name="facts", help="Returns a random fact, albeit useless.")
async def facts(ctx):
    url = "https://uselessfacts.jsph.pl/random.json"
    facts = requests.get(url, params={"language": "en"}).json()

    embed = discord.Embed(title="**Useless Fact** \n\n", description=facts['text'], color=0xffffff)

    await ctx.send(embed=embed)

@client.command(name="words", help="Returns a word that **does not exist.**")
async def words(ctx):
    url = "https://www.thisworddoesnotexist.com/api/random_word.json"
    word = requests.get(url).json()
    arrange = []
    arrange.append("**" + word['word']['word'] + "**")
    arrange.append("*" + word['word']['pos'] + "*")
    arrange.append(word['word']['definition'])
    embed = discord.Embed(title="**Fake Word: ** \n\n\n", description=listToString(arrange), color=0xffffff)
    
    await ctx.send(embed=embed)

@client.command()
async def moe(ctx):
    bruh = pybooru.Moebooru('konachan')
    tags = bruh.tag_list(order='name', limit= 10000, type=1)

    if ctx.channel.is_nsfw():
        taglist = []
    
        
        for tag in tags:
            taglist.append(tag['name'])

        imglist = []
        
        posts = bruh.post_list(limit=10, type=0, tags=random.choice(taglist))

        for post in posts:
            imglist.append(post['file_url'])

        
        final = random.choice(imglist)
        
        embed = discord.Embed(title="**Random Anime Pampagana: **", color=0xffffff)
        embed.set_image(url=final)

        await ctx.send(embed=embed)

    else:

        taglist = []
    
        for tag in tags:
            taglist.append(tag['name'])

        imglist = []
        
        posts = bruh.post_list(limit=10, type=1, tags=random.choice(taglist))

        for post in posts:
            imglist.append(post['file_url'])
        
        final = random.choice(imglist)
        
        embed = discord.Embed(title="**Random Anime SFW pero Pampagana: **", color=0xffffff)
        embed.set_image(url=final)

        await ctx.send(embed=embed)


@client.command()
async def dans(ctx):
    bruh = pybooru.Danbooru('danbooru')
    tags = bruh.tag_list(order='name')

    if ctx.channel.is_nsfw():
        taglist = []
    
        
        for tag in tags:
            taglist.append(tag['name'])

        imglist = []
        
        posts = bruh.post_list(limit=10, type=0, tags=random.choice(taglist))

        for post in posts:
            imglist.append(post['file_url'])

        
        final = random.choice(imglist)
        
        embed = discord.Embed(title="**Random Anime Pampagana: **", color=0xffffff)
        embed.set_image(url=final)

        await ctx.send(embed=embed)

    else:
        
        taglist = []
    
        for tag in tags:
            taglist.append(tag['name'])

        imglist = []
        
        posts = bruh.post_list(limit=10, type=1, tags=random.choice(taglist))

        for post in posts:
            imglist.append(post['file_url'])
        
        final = random.choice(imglist)
        
        embed = discord.Embed(title="**Random Anime SFW pero Pampagana: **", color=0xffffff)
        embed.set_image(url=final)

        await ctx.send(embed=embed)

@client.command()
async def neko(ctx):
    NEKO_URL = "https://nekos.life/api/v2/img/"
    NEKO_TYPES = ['lewd', 'smug', 'tits', 'trap', 'anal', 'cuddle', 'hug', 'goose', 'waifu', 'gasm', 'slap', 'spank', 'pat', 'feet', 'woof', 'baka', 'blowjob']
    #REPLY_TYPES = ['cuddle', 'hug', 'slap', 'spank', 'pat', 'baka', 'blowjob']
    params = random.choice(NEKO_TYPES)
    if ctx.channel.is_nsfw():
        neko = requests.get(NEKO_URL + params).json()

    else:
        neko = requests.get(NEKO_URL + "neko").json()


    embed = discord.Embed(title="Random Cat Pic (sort of)")
    embed.set_image(url=neko['url'])

    await ctx.send(embed=embed)

@client.command()
async def hug(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/hug"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="hug", description= "**" + ctx.message.author.name + " just hugged " + str(user.name) + "!!!!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command(name="smug", help="Haha fuck someone.")
async def smug(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/smug"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="Smuggery", description= "**" + ctx.message.author.name + " is underestimating " + str(user.name) + " for his/her foolishness!!!!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command(name="slap", help="Show your anger. Slap him/her!")
async def slap(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/slap"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="Slapped!", description= "**" + ctx.message.author.name + " just slapped " + str(user.name) + "**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command(name="baka", help="Haha I'm with stupid.")
async def baka(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/baka"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="Stupid!", description= "**" + ctx.message.author.name + " just called " + str(user.name) + "stupid!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command(name="cuddle", help="Mention someone to cuddle him/her.")
async def cuddle(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/cuddle"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="cuddle", description= "**" + ctx.message.author.name + " is cuddling with " + str(user.name) + "!!!!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command(name="pat", help="Mention someone to pat him/her in the head.")
async def pat(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/pat"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="Patting Session", description= "**" + ctx.message.author.name + " just patted " + str(user.name) + "!!!!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command(name="kiss", help="Mention someone in the server to kiss him/her.")
async def kiss(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/kiss"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="Laplapan Session", description= "**" + ctx.message.author.name + " just kissed " + str(user.name) + "!!!!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command(name="blowjob", help="NSFW (duh). Mention someone in the server to blow him/her.")
async def blowjob(ctx, user: discord.User):

    if ctx.channel.is_nsfw():
        NEKO_URL = "https://nekos.life/api/v2/img/blowjob"
        neko = requests.get(NEKO_URL).json()
        embed = discord.Embed(title="Blowjob", description= "**" + ctx.message.author.name + " just fucking blowed " + str(user.name) + "!!!!**")
        embed.set_image(url=neko['url'])
        await ctx.send(embed=embed)

    else:
        await ctx.send("This command is for NSFW channels only!!")

@client.command(name="fuck", help="NSFW feature. Mention someone to fuck him/her.")
async def fuck(ctx, user: discord.User):

    if ctx.channel.is_nsfw():
        NEKO_URL = "https://nekos.life/api/v2/img/anal"
        neko = requests.get(NEKO_URL).json()
        embed = discord.Embed(title="Fucked", description= "**" + ctx.message.author.name + " fucked " + str(user.name) + "in the ass!!!!**")
        embed.set_image(url=neko['url'])

        await ctx.send(embed=embed)
    
    else:
        await ctx.send("This command is for NSFW channels only!!")

@client.command(name="spank", help="Mention someone in the server to spank him/her.")
async def spank(ctx, user: discord.User):

    if ctx.channel.is_nsfw():
        NEKO_URL = "https://nekos.life/api/v2/img/spank"
        neko = requests.get(NEKO_URL).json()
        embed = discord.Embed(title="Spanking Session", description= "**" + ctx.message.author.name + " just spanked " + str(user.name) + "!!!!**")
        embed.set_image(url=neko['url'])
        await ctx.send(embed=embed)

    else:
        await ctx.send("This command is for NSFW channels only!!")
    
@client.command(name="ratewaifu", help="I'll rate your waifu if he/she trash or not.")
async def ratewaifu(ctx, user: discord.User):
    try:
        rating = str(random.randint(1, 10))
        await ctx.send("Let me think.... I'll rate {0} a {1}/10".format(user.name, rating))

    except:
        await ctx.send("Hmmm.. That isn't a valid user.")

@client.command()
async def weather(ctx, *, msg):
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1b453b589a0691c857ddc95f0921df69'
        r = requests.get(url.format(msg)).json()
        temperature = str(r['main']['temp'])
        description = r['weather'][0]['description'].capitalize()
        icon = r['weather'][0]['icon']
        imgurl = 'http://openweathermap.org/img/w/{}.png'.format(icon)

        embed = discord.Embed(title="Weather for {}".format(msg), description= "**Temperature: " + temperature + "°C**\n" + "**Description: " + description + "**")
        embed.set_thumbnail(url=imgurl)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("It looks like the source doesn't have any data over that city, or maybe what I read was not a city.")

@client.command()
async def ball(ctx, *, msg):
    choices = ["As I see it, yes,", "Ask again later,", "Better not tell you now,", "Cannot predict now,", "Concentrate and ask again,", "Don’t count on it,","It is certain,", "It is decidedly so,", "Most likely,", "My reply is no,", "My sources say no.", "Outlook not so good.", "Outlook good.", "Reply hazy, try again,", "Signs point to yes,", "Very doubtful,", "Without a doubt,", "Yes,", "Yes – definitely,", "You may rely on it,"]
    
    await ctx.send("🎱| " + random.choice(choices) + " " + "**" + ctx.message.author.name + "**")

@client.command()
async def lipstick(ctx):
    url = 'http://makeup-api.herokuapp.com/api/v1/products.json?product_type=lipstick'
    a, color, tags = make.makeapp(url)

    embed = discord.Embed(title="Lipstick", description=listToString(a))
    
    try:
        img = a[4].replace("Image: ", "")
        embed.set_image(url=img)
    
    except:
        pass

    await ctx.send(embed=embed)


@client.command()
async def blush(ctx):
    url = 'http://makeup-api.herokuapp.com/api/v1/products.json?product_type=blush'
    a, color, tags = make.makeapp(url)

    embed = discord.Embed(title="Blush", description=listToString(a))
    
    try:
        img = a[4].replace("Image: ", "")
        embed.set_image(url=img)

    except:
        pass

    await ctx.send(embed=embed)

@client.command()
async def mascara(ctx):
    url = 'http://makeup-api.herokuapp.com/api/v1/products.json?product_type=mascara'
    a, color, tags = make.makeapp(url)

    embed = discord.Embed(title="Mascara", description=listToString(a))
    
    try:
        img = a[4].replace("Image: ", "")
        embed.set_image(url=img)

    except:
        pass

    await ctx.send(embed=embed)


@client.command()
async def eyeliner(ctx):
    url = 'http://makeup-api.herokuapp.com/api/v1/products.json?product_type=eyeliner'
    a, color, tags = make.makeapp(url)

    embed = discord.Embed(title="Eyeliner", description=listToString(a))
    
    try:
        img = a[4].replace("Image: ", "")
        embed.set_image(url=img)

    except:
        pass

    await ctx.send(embed=embed)

@client.command()
async def foundation(ctx):
    url = 'http://makeup-api.herokuapp.com/api/v1/products.json?product_type=foundation'
    a, color, tags = make.makeapp(url)

    embed = discord.Embed(title="Foundation", description=listToString(a))
    
    try:
        img = a[4].replace("Image: ", "")
        embed.set_image(url=img)

    except:
        pass

    await ctx.send(embed=embed)

@client.command()
async def polish(ctx):
    url = 'http://makeup-api.herokuapp.com/api/v1/products.json?product_type=nail_polish'
    a, color, tags = make.makeapp(url)

    embed = discord.Embed(title="Nail Polish", description=listToString(a))
    
    try:
        img = a[4].replace("Image: ", "")
        embed.set_image(url=img)

    except:
        pass

    await ctx.send(embed=embed)

@client.command()
async def lipliner(ctx):
    url = 'http://makeup-api.herokuapp.com/api/v1/products.json?product_type=lip_liner'
    a, color, tags = make.makeapp(url)

    embed = discord.Embed(title="Lip Liner", description=listToString(a))
    
    try:
        img = a[4].replace("Image: ", "")
        embed.set_image(url=img)

    except:
        pass

    await ctx.send(embed=embed)


@client.command()
async def op(ctx, *, msg):
    try:
        url = 'https://onepiececover.com/api/chapters/{}'.format(msg)
        ep = requests.get(url).json()
        img = ep['cover_images']
        bruh = []

        i = 0

        while i <= 83:
            bruh.append(img[i])
            i+=1

        img = "".join(bruh)

        embed = discord.Embed(title=ep['title'], description=ep['summary'])
        embed.set_image(url=img)

        await ctx.send(embed=embed)


    except Exception as e:
        await ctx.send(e)
        #await ctx.send("I need a number, or maybe I've received a very high number?")
    
@client.command()
async def randpic(ctx):
    urls = ['https://source.unsplash.com/random', 'https://picsum.photos/500/500']
    url = random.choice(urls)
    img = requests.get(url)
    embed= discord.Embed(title="Random Pic")
    embed.set_image(url=img.url)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_channels = True)
async def say(ctx, channel: discord.TextChannel, *msg):
    msg = " ".join(msg)
    await channel.send(msg)

#client.run(os.environ['KEY'])
client.run('NzYxOTU5MjExMDE3ODMwNDQw.X3iL0A.hpvKZmwyEldI2-Sa7huGb-ta1-Y')
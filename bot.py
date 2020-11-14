# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
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
import config
import praw
import pybooru
import youtube_dl
import topiclist

queue = []
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = { 
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL(ytdl_format_options).extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else youtube_dl.YoutubeDL(ytdl_format_options).prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

reddit = praw.Reddit(client_id = config.client_id,
                     client_secret = config.client_secret,
                     username = config.username,
                     password = config.password,
                     user_agent = config.user_agent)

shoes = long.sneakers()
udclient = UrbanClient()
client = commands.Bot(command_prefix="//")

status = ["Playing with myself.", "Reading War and Peace.", "Practicing my juggling skills"]

client.thetitle = ""



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
    
@client.command()
async def hello(ctx):
    await ctx.send("Hello there!")

@client.command()
async def advice(ctx):
    url = "https://api.adviceslip.com/advice"
    advice = requests.get(url).json()
    await ctx.send(advice['slip']['advice'])

@client.command(name='ping', help="This command returns the latency.")
async def ping(ctx):
    await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

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
async def topic(ctx):
    topics = [random.choice(topiclist.adults), random.choice(topiclist.kids), random.choice(topiclist.deep), random.choice(topiclist.couples)]
    await ctx.send(random.choice(topics))

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
async def flip(ctx):
    coin = ['heads', 'tails']
    await ctx.send("I flipped a coin and it's {}".format(random.choice(coin)))



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
        #embed.set_thumbnail(url=ctx.message.author.avatar_url)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(e)

@client.command()
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

@client.command()
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
    
@client.command()
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

@client.command()
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

@client.command()
async def av(ctx, user: discord.User):
    try:
        embed = discord.Embed(title=str(user.name) + "'s Avatar: ", color=0xffffff)
        embed.set_image(url=user.avatar_url)
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
        #embed.set_thumbnail(url=ctx.message.author.avatar_url)

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
    embed = discord.Embed(title="**Philippines Coronavirus Updates as of {}".format((str(dateutil.parser.parse(d['time'])))) +"**", description=listToString(disease))
    await ctx.send(embed=embed)


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
        try:
            embed.set_image(submission.url)
        except:
            pass

        await ctx.send(embed=embed)


    except:
        await ctx.send("There seems to be an error.")


@client.command()
async def rrand(ctx, *, msg):
    try:
        submission = reddit.subreddit(msg).random()
        embed=discord.Embed(title=submission.title, description=submission.selftext + "\n" + submission.url, color=0xffffff)
        
        try:
            embed.set_image(submission.url)

        except:
            pass
        
        embed.set_footer(text="Command invoked by {}".format(ctx.message.author.name))
        
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(e)

@client.command()
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

@client.command()
async def rhot(ctx, *, msg):
    redditlogic = long.reddit()
    try:
        subreddit = reddit.subreddit(msg)
        hot = subreddit.hot(limit=5)
        redlist = redditlogic.hotornew(hot)
        await ctx.send("Here are the hottest topics at " + msg + ": " + "\n\n" + listToString(redlist))

    except Exception as e:
        await ctx.send(e)

@client.command()
async def rnew(ctx, *, msg):
    redditlogic = long.reddit()
    try:
        subreddit = reddit.subreddit(msg)
        new = subreddit.new(limit=5)
        redlist = redditlogic.hotornew(new)
        await ctx.send("Here are the hottest topics at " + msg + ": " + "\n\n" + listToString(redlist))

    except Exception as e:
        await ctx.send(e)


@client.command()
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

@client.command()
async def facts(ctx):
    url = "https://uselessfacts.jsph.pl/random.json"
    facts = requests.get(url, params={"language": "en"}).json()

    embed = discord.Embed(title="**Useless Fact** \n\n", description=facts['text'], color=0xffffff)

    await ctx.send(embed=embed)

@client.command()
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

@client.command()
async def smug(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/smug"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="Smuggery", description= "**" + ctx.message.author.name + " is underestimating " + str(user.name) + " for his/her foolishness!!!!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command()
async def slap(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/slap"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="Slapped!", description= "**" + ctx.message.author.name + " just slapped " + str(user.name) + "**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command()
async def cuddle(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/cuddle"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="cuddle", description= "**" + ctx.message.author.name + " is cuddling with " + str(user.name) + "!!!!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command()
async def pat(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/pat"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="Patting Session", description= "**" + ctx.message.author.name + " just patted " + str(user.name) + "!!!!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command()
async def kiss(ctx, user: discord.User):
    NEKO_URL = "https://nekos.life/api/v2/img/kiss"
    neko = requests.get(NEKO_URL).json()
    embed = discord.Embed(title="Laplapan Session", description= "**" + ctx.message.author.name + " just kissed " + str(user.name) + "!!!!**")
    embed.set_image(url=neko['url'])
    await ctx.send(embed=embed)

@client.command()
async def blowjob(ctx, user: discord.User):

    if ctx.channel.is_nsfw():
        NEKO_URL = "https://nekos.life/api/v2/img/blowjob"
        neko = requests.get(NEKO_URL).json()
        embed = discord.Embed(title="Blowjob", description= "**" + ctx.message.author.name + " just fucking blowed " + str(user.name) + "!!!!**")
        embed.set_image(url=neko['url'])
        await ctx.send(embed=embed)

    else:
        await ctx.send("This command is for NSFW channels only!!")

@client.command()
async def fuck(ctx, user: discord.User):

    if ctx.channel.is_nsfw():
        NEKO_URL = "https://nekos.life/api/v2/img/anal"
        neko = requests.get(NEKO_URL).json()
        embed = discord.Embed(title="Fucked", description= "**" + ctx.message.author.name + " fucked " + str(user.name) + "in the ass!!!!**")
        embed.set_image(url=neko['url'])

        await ctx.send(embed=embed)
    
    else:
        await ctx.send("This command is for NSFW channels only!!")

@client.command()
async def spank(ctx, user: discord.User):

    if ctx.channel.is_nsfw():
        NEKO_URL = "https://nekos.life/api/v2/img/spank"
        neko = requests.get(NEKO_URL).json()
        embed = discord.Embed(title="Spanking Session", description= "**" + ctx.message.author.name + " just spanked " + str(user.name) + "!!!!**")
        embed.set_image(url=neko['url'])
        await ctx.send(embed=embed)

    else:
        await ctx.send("This command is for NSFW channels only!!")
    
@client.command()
async def ratewaifu(ctx, user: discord.User):
    try:
        rating = str(random.randint(1, 10))
        await ctx.send("Let me think.... I'll rate {0} a {1}/10".format(user.name, rating))

    except:
        await ctx.send("Hmmm.. That isn't a valid user.")

@client.command()
async def ball(ctx, *, msg):
    choices = ["As I see it, yes,", "Ask again later,", "Better not tell you now,", "Cannot predict now,", "Concentrate and ask again,", "Don’t count on it,","It is certain,", "It is decidedly so,", "Most likely,", "My reply is no,", "My sources say no.", "Outlook not so good.", "Outlook good.", "Reply hazy, try again,", "Signs point to yes,", "Very doubtful,", "Without a doubt,", "Yes,", "Yes – definitely,", "You may rely on it,"]
    
    await ctx.send("🎱| " + random.choice(choices) + " " + "**" + ctx.message.author.name + "**")
        
#MUSIC
@client.command(name='queue', help='This command adds a song to the queue')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')


@client.command(name='remove', help='This command removes an item from the list')
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')
    
    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')

@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@client.command(name='play', help='This command plays songs')
async def play(ctx, *, url):
    global queue

    if not queue:
        queue.append(url)
        await ctx.send(f'`{url}` added to queue!')

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))

    try:
        del(queue[0])
    except:
        pass



@client.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@client.command(name='view', help='This command shows the queue')
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')


@client.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

client.run()
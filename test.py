# -*- coding: utf-8 -*-
import requests
import json 
import pybooru
import random
"""url = "https://uselessfacts.jsph.pl/random.json"
facts = requests.get(url, params={"language": "en"}).json()
print(facts['text'])"""

"""url = "https://www.thisworddoesnotexist.com/api/random_word.json"

word = requests.get(url).json()
print(word['word']['definition'])"""



"""client = pybooru.Moebooru('konachan')

tags = client.tag_list(order='name', type=0, limit=10000)
taglist=[]


for tag in tags:
    #print("Tag: {0} ----- {1}".format(tag['name'], tag['type']))   
    taglist.append(tag['name'])

posts = client.post_list(limit=100, tags=random.choice(taglist), type=0)

for post in posts:
    print("URL image: {0}".format(post['file_url']))"""


"""NEKO_URL = "https://nekos.life/api/v2/img/"
NEKO_TYPES = ['lewd', 'smug', 'tits', 'trap', 'anal', 'cuddle', 'hug', 'goose', 'waifu', 'gasm', 'slap', 'spank', 'pat', 'feet', 'woof', 'baka', 'blowjob']
REPLY_TYPES = ['cuddle', 'hug', 'slap', 'spank', 'pat', 'baka', 'blowjob']
params = random.choice(NEKO_TYPES)
neko = requests.get(NEKO_URL + params).json()

print(neko['url'])"""

"""url = "https://api.adviceslip.com/advice"
advice = requests.get(url).json()
print(advice['slip']['advice'])"""

text = """rant incoming, and I'll probably offend some people

Lele is literally a fucking embarrassment. She targeted normies and half-assed weebs with little to no knowledge on how to behave properly in a livestream.

Lele is nowhere near the point where she should be called a "VTuber", she's just an "uwu" girl using a VTuber avatar to appeal to the weeb community. Fucking hell she's closer to an e-girl than a VTuber. In one of her livestream titles, "ako muna bago ang modules" says it all, a fucking e-girl. Also she would moan for no fucking reason, and her attitude isn't even that cute. I expected good content from her, but instead got the opposite.

Also, she even allowed her fans to trace only if they post the original one. AND THATS THE FUCKING PROBLEM. These so-called "artists" trace art from well known artists like Hews, AND SOME EVEN PUT THEIR SIGNATURE IN THE FUCKING ART TRACE JUSTIFYING THAT ITS "ORIGINAL".

I myself am no artist, but I am against tracing. These artists put their time and effort into making those original art, AND YOU LELETARDS WOULD TRACE IT AND PUT YOUR FUCKING SIGNATURE IN IT. I CANT BELIEVE YOU RETARDS STILL GET NOTICED BY LELE

If you guys want good content, please, don't go anywhere near her streams. Go to Twitch or something idk just don't go anywhere near her. It's a cesspool of cringe content and cringe comments.

TL;DR: Lele and her fanbase is cringe af, don't even bother with them."""

zal_chars = ' ̷̡̛̮͇̝͉̫̭͈͗͂̎͌̒̉̋́͜ ̵̠͕͍̩̟͚͍̞̳̌́̀̑̐̇̎̚͝ ̸̻̠̮̬̻͇͈̮̯̋̄͛̊͋̐̇͝͠ ̵̧̟͎͈̪̜̫̪͖̎͛̀͋͗́̍̊͠ ̵͍͉̟͕͇͎̖̹̔͌̊̏̌̽́̈́͊ͅ ̷̥͚̼̬̦͓͇̗͕͊̏͂͆̈̀̚͘̚ ̵̢̨̗̝̳͉̱̦͖̔̾͒͊͒̎̂̎͝ ̵̞̜̭̦̖̺͉̞̃͂͋̒̋͂̈́͘̕͜ ̶̢̢͇̲̥̗̟̏͛̇̏̊̑̌̔̚ͅͅ ̷̮͖͚̦̦̞̱̠̰̍̆̐͆͆͆̈̌́ ̶̲͚̪̪̪͍̹̜̬͊̆͋̄͒̾͆͝͝ ̴̨̛͍͖͎̞͍̞͕̟͑͊̉͗͑͆͘̕ ̶͕̪̞̲̘̬͖̙̞̽͌͗̽̒͋̾̍̀ ̵̨̧̡̧̖͔̞̠̝̌̂̐̉̊̈́́̑̓ ̶̛̱̼̗̱̙͖̳̬͇̽̈̀̀̎̋͌͝ ̷̧̺͈̫̖̖͈̱͎͋͌̆̈̃̐́̀̈'.replace(" ", "")
    
    
"""zalgo_text = ''
    
for letter in text:
    if letter == " ":
        zalgo_text += letter
        continue

    letter += random.choice(zal_chars)
    letter += random.choice(zal_chars)
    letter += random.choice(zal_chars)
    zalgo_text += letter

print(zalgo_text)"""

"""url = 'https://onepiececover.com/api/chapters/123'
ep = requests.get(url).json()
print(ep['cover_images'])"""

"""url = 'https://picsum.photos/500/500'
ep = requests.get(url)
print(ep.url)"""

"""url = "https://no-api-key.com/api/v1/memes"
memes = requests.get(url).json()
print(memes['image'])"""


img = 'https://i.pinimg.com/originals/4a/06/03/4a0603d0b59dbb9033b38bf6cbc9d853.jpg'
url= 'https://api.no-api-key.com/api/v2/simpcard?image={}'.format(img)
memes=requests.get(url).json()
print(memes['image'])
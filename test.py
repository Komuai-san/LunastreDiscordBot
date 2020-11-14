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

url = "https://api.adviceslip.com/advice"
advice = requests.get(url).json()
print(advice['slip']['advice'])



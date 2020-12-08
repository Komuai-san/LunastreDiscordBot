import requests
import random
import json
import datetime
import dateutil.parser
from newsapi import NewsApiClient

class sneakers:
    def getShoes(self, gender):
        if gender == "mshoes":
            gender = 'men'

        elif gender == "wshoes":
            gender = 'women'

        url = 'https://api.thesneakerdatabase.com/v1/sneakers'
        params = { 'limit': '100', 'gender': gender }
        shoes = requests.request("GET", url, params=params).json()
        shoeslist = []
        numba = random.randint(1, 100)
        price = str(shoes['results'][numba]['retailPrice'])
        imgurl = shoes['results'][numba]['media']['imageUrl']
        shoename = shoes['results'][numba]['title']
        release = shoes['results'][numba]['releaseDate'].replace(" 23:59:59", "").split("-")
        converted = datetime.date(int(release[0]), int(release[1]), int(release[2]))
        thetime = converted.strftime("%B %d, %Y, %A")


        shoeslist.append("Name: " + shoes['results'][numba]['title'])
        shoeslist.append("Brand Name: " + shoes['results'][numba]['brand'])
        shoeslist.append("Colours: " + shoes['results'][numba]['colorway'])
        shoeslist.append("Date Released: " + thetime)
        
        if price == "None":
            price = ""
            shoeslist.append("Price: Nope. No price indicated in the database.")

        else:
            shoeslist.append("Price: $" + price)

        shoeslist.append(imgurl)
        
        return shoeslist

def getNews():
        newsapi = NewsApiClient(api_key='4f1571a2b1af4f2089d6ab2d33d67109')
        topheadlines = newsapi.get_top_headlines(sources="bbc-news")

        articles = topheadlines['articles']

        news = []

        for i in range(len(articles)):
            myarticles = articles [i]

            news.append(myarticles['title'] + "\n\n\nArticle by: " + myarticles['author'] + "\n\n\nDate Posted: " + str(dateutil.parser.parse(myarticles['publishedAt'])) + "\n\n\n" + myarticles['description'] + "\n\n\n" + myarticles['url'] + "\n\n\n" +  myarticles['urlToImage'])

        return news


class reddit:
    def __init__(self):
        pass

    def hotornew(self, redit):
        redlist = []
        
        for index, submission in enumerate(redit, start=1):
            redlist.append(str(index) + "). " + submission.title)

            if(submission.selftext == ""):
                pass
            else:
                redlist.append("- " + submission.selftext)
                
            redlist.append(submission.url)

            if index == 5:
                break
        
        return redlist

class makeup:
    def __init__(self):
        pass

    def makeapp(self, url):
        mek = requests.get(url).json()
        color = []
        rando = 2

        try:
            while True:
                try:
                    rando = random.randint(0, 500)
                    a = ["Brand: " + mek[rando]['brand'], "Name: " + mek[rando]['name'], "Price: $" + str(mek[rando]['price']), "Link: " + mek[rando]['product_link'], "Image: " + mek[rando]['image_link'], "Description: " + mek[rando]['description'], "Rating: " + str(mek[rando]['rating'])]
                    break
                except:
                    continue

            try:
                index = 0
                while index <=10:
                    try:
                        color.append(mek[rando]['product_colors'][index]['colour_name'])
                        index+=1
                                
                    except:
                        break
            except:
                pass

            if len(mek[rando]['tag_list']) == 0:
                    tags = "No Tags."

            else:
                tags = "Tags: " + str(mek[rando]['tag_list'])[1:-1]

                        
            #reply = "You might like this one: \n\n" + listToString(a) + "\n\nColours: " + str(color)[1:-1] + "\n\n" + tags
            return a, color, tags

        except Exception as e:
            return e


class googledict:
    def __init__(self):
        pass
    
    def parsetext(self, response):
        index = 0
        mgawords = []
        mgawords.append(response[0]['word'])
        mgawords.append(response[0]['phonetics'][0]['text'])
        while index <= 10:
            try:
                str1 = ", "
                mgawords.append(response[0]['meanings'][index]['partOfSpeech'])
                mgawords.append(response[0]['meanings'][index]['definitions'][0]['definition'])
                try: 
                    mgawords.append("-" + response[0]['meanings'][index]['definitions'][1]['definition'])
                except:
                    pass
                
                try:
                    mgawords.append("-" + response[0]['meanings'][index]['definitions'][2]['definition'])
                except:
                    pass

                try:
                    mgawords.append("synonyms: \n\n" +  str1.join(response[0]['meanings'][0]['definitions'][index]['synonyms']))
                except:
                    mgawords.append("synonyms: Nope. source didn't return anything.")
                try:
                    mgawords.append("\nExample: \n\n" + "-" + (str.capitalize(response[0]['meanings'][index]['definitions'][0]['example'])))
                except:
                    mgawords.append("Example: N/A")

                index += 1

            except:
                break

        mgawords.append(response[0]['phonetics'][0]['audio'])

        return mgawords
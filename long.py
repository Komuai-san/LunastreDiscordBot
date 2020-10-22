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

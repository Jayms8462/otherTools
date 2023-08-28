### This script will grab all the links on the Priceguide URLs listed in the urls list.

import os
import requests
import json
from bs4 import BeautifulSoup

os.system('cls' if os.name == 'nt' else 'clear')
if os.path.exists('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\count.txt'):
    os.remove('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\count.txt')
if os.path.exists('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\errorUrl.txt'):
    os.remove('C:\\Users\\ajpor\\OneDrive\\Desktop\\cardData\\errorUrl.txt')


urls = [
    "https://www.priceguide.cards/collection/5792/1989-fleer-baseball-cards",
    "https://www.priceguide.cards/collection/1450/1989-procards-baseball-cards",
    "https://www.priceguide.cards/collection/5973/1989-score-baseball-cards",
    "https://www.priceguide.cards/collection/4895/1989-topps-baseball-cards",
    "https://www.priceguide.cards/collection/1284/1989-topps-toys-r-us-rookies-baseball-cards",
    "https://www.priceguide.cards/collection/7267/1989-upper-deck-baseball-cards#google_vignette",
    "https://www.priceguide.cards/collection/4863/1989-donruss-baseball-cards#google_vignette"
    "https://www.priceguide.cards/collection/6650/1990-cmc-colorado-springs-sky-sox-baseball-cards",
    "https://www.priceguide.cards/collection/6561/1990-donruss-baseball-cards",
    "https://www.priceguide.cards/collection/7042/1990-fleer-baseball-cards",
    "https://www.priceguide.cards/collection/382/1990-score-baseball-cards",
    "https://www.priceguide.cards/collection/4297/1990-topps-baseball-cards",
    "https://www.priceguide.cards/collection/2410/1990-topps-bazooka-baseball-cards",
    "https://www.priceguide.cards/collection/7259/1990-topps-bowman-baseball-cards",
    "https://www.priceguide.cards/collection/2790/1990-topps-toys-r-us-rookies-baseball-cards",
    "https://www.priceguide.cards/collection/5684/1990-topps-traded-baseball-cards",
    "https://www.priceguide.cards/collection/4963/1990-upper-deck-baseball-cards",
    "https://www.priceguide.cards/collection/2031/1991-donruss-baseball-cards",
    "https://www.priceguide.cards/collection/3479/1991-fleer-baseball-cards",
    "https://www.priceguide.cards/collection/5701/1991-fleer-ultra-baseball-cards",
    "https://www.priceguide.cards/collection/622/1991-megacards-the-sporting-news-conlon-collection-tsn-baseball-cards",
    "https://www.priceguide.cards/collection/359/1991-o-pee-chee-premier-baseball-cards",
    "https://www.priceguide.cards/collection/5742/1991-score-baseball-cards",
    "https://www.priceguide.cards/collection/4761/1991-score-hottest-100-players-baseball-cards",
    "https://www.priceguide.cards/collection/732/1991-score-rookie-&-traded-baseball-cards",
    "https://www.priceguide.cards/collection/501/1991-topps-baseball-cards",
    "https://www.priceguide.cards/collection/4224/1991-topps-bowman-baseball-cards",
    "https://www.priceguide.cards/collection/6596/1991-upper-deck-baseball-cards",
    "https://www.priceguide.cards/collection/2003/1992-donruss-baseball-cards",
    "https://www.priceguide.cards/collection/3373/1992-dowbrands-ziploc-baseball-cards",
    "https://www.priceguide.cards/collection/4523/1992-fleer-baseball-cards",
    "https://www.priceguide.cards/collection/4784/1992-fleer-ultra-baseball-cards",
    "https://www.priceguide.cards/collection/6319/1992-post-cereal-baseball-cards",
    "https://www.priceguide.cards/collection/5317/1992-score-baseball-cards",
    "https://www.priceguide.cards/collection/1727/1992-topps-baseball-cards",
    "https://www.priceguide.cards/collection/7127/1992-upper-deck-baseball-cards",
    "https://www.priceguide.cards/collection/3511/1992-upper-deck-dennys-grand-slam-baseball-cards",
    "https://www.priceguide.cards/collection/6152/1993-fleer-ultra-baseball-cards",
    "https://www.priceguide.cards/collection/4484/1993-hostess-baseball-cards",
    "https://www.priceguide.cards/collection/5610/1994-donruss-baseball-cards",
    "https://www.priceguide.cards/collection/6646/1994-donruss-triple-play-baseball-cards",
    "https://www.priceguide.cards/collection/5708/1994-pinnacle-baseball-cards",
    "https://www.priceguide.cards/collection/6506/1994-post-cereal-baseball-cards",
    "https://www.priceguide.cards/collection/4351/1994-score-baseball-cards",
    "https://www.priceguide.cards/collection/1275/1994-score-tombstone-pizza-super-pro-series-baseball-cards",
    "https://www.priceguide.cards/collection/2637/1994-topps-stadium-club-baseball-cards",
    "https://www.priceguide.cards/collection/458/1994-topps-stadium-club-team-baseball-cards",
    "https://www.priceguide.cards/collection/1/1995-pinnacle-baseball-cards",
    "https://www.priceguide.cards/collection/2367/1995-topps-stadium-club-baseball-cards",
    "https://www.priceguide.cards/collection/2706/1995-upper-deck-collector's-choice-baseball-cards",
    "https://www.priceguide.cards/collection/7455/1995-upper-deck-collector's-choice-special-edition-baseball-cards"
]

for url in urls:
    idxUrl = 0
    try:
        ### Gets JSON data that is imbeded in the script id
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        script = soup.find("script", {"id": "__NEXT_DATA__"}).text

        ### Converts the JSON data to JSON Objects
        data = json.loads(script)
        json_formatted = data['props']['pageProps']['data']['data']['auto_memo']
        obj_len = len(json_formatted)
        idx = 0
        while idx < obj_len:
            jsonData = json_formatted[idx]
            baseSet = jsonData['name'] # Prints Base Set name, either Autograph & Momorabilia, Autograph, Memorabilia and other main base set names
            subsetDetails = jsonData['types']
            setPub = data['props']['pageProps']['data']['data']['publisher']['name']
            setYear = data['props']['pageProps']['data']['data']['year']
            for items in subsetDetails:
                for sets in items['colors']:    # Gets the Individual Sets in the base set
                    urlData = 'https://www.priceguide.cards/checklist/' + str(items['id']) + '/' + sets['colorCode'] + '/' + sets['url']
                    print(urlData)
                    with open("priceguideUrls.txt", "a") as f:
                        f.write(urlData + "\n")
            idx += 1
        print(str(idxUrl), 'Complete: ', url)
        idxUrl += 1
    except KeyError:
        with open("errorUrl.txt", 'a', encoding="utf-8") as f:
            f.write(url + "\n")
        f.close()
        print('ErrorUrl:', url)

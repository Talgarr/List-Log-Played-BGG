from datetime import datetime
from time import sleep
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


def get_collection(username):
    url = 'https://boardgamegeek.com/xmlapi2/collection?username=' + username + '&own=1&excludesubtype=boardgameexpansion'
    response = requests.get(url)
    while b'Your request for this collection has been accepted and will be processed.  Please try again later for access.' in response.content:
        sleep(3)
        response = requests.get(url)

    Bs_data = BeautifulSoup(response.content, 'xml')
    return [i.getText() for i in Bs_data.find_all('name')]


def get_plays(username, owns):
    page = 1
    plays = {}
    while True:
        url = 'https://boardgamegeek.com/xmlapi2/plays?username=' + username + '&page=' + str(page)
        page += 1
        response = requests.get(url)
        Bs_data = BeautifulSoup(response.content, 'xml')
        plays_data = Bs_data.find_all('play')

        if len(plays_data) == 0:
            break
        for i in plays_data:
            name = i.find('item').get('name')
            if name in owns:
                time = datetime.strptime(i['date'], "%Y-%m-%d")
                plays[name] = time
                owns.remove(name)

    return plays


plays = {}
owns = get_collection('fredl751')
for game in owns:
    if game not in plays.keys():
        plays[game] = datetime(1, 1, 1)
for name in ['fredl751', 'Talgarr']:
    for game, time in get_plays(name, owns).items():
        plays[game] = max(time, plays[game])

plays = sorted(plays.items(), key=lambda x: x[1], reverse=True)
for i in range(len(plays)):
    plays[i] = [plays[i][0], plays[i][1].strftime("%d %b %Y")]

print(tabulate(plays, headers=['Game', 'Last Played']))

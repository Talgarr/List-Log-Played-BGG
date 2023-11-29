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


def get_plays(username, owns, plays):
    url = 'https://boardgamegeek.com/xmlapi2/plays?username=' + username
    response = requests.get(url)

    Bs_data = BeautifulSoup(response.content, 'xml')

    for i in Bs_data.find_all('play'):
        name = i.find('item').get('name')
        if name in owns:
            time = datetime.strptime(i['date'], "%Y-%m-%d")
            if name in plays:
                plays[name] = max(time, plays[name])
            else:
                plays[name] = time
            owns.remove(name)

    return plays


plays = {}
for name in ['Talgarr', 'fredl751']:
    owns = get_collection(name)
    plays = get_plays(name, owns, plays)

plays = sorted(plays.items(), key=lambda x: x[1], reverse=True)
for i in range(len(plays)):
    plays[i] = [plays[i][0], plays[i][1].strftime("%d %b %Y")]
for game in owns:
    if game not in plays:
        plays.append([game, 0])
print(tabulate(plays, headers=['Game', 'Last Played']))

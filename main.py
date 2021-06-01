from bs4 import BeautifulSoup as bs
from urllib.error import HTTPError,URLError
from urllib.request import urlopen
##webscrapping players details from NBA site and storing them in CSV file.
import requests
import csv

csv_file = open('nbaplayers.csv','w')
csv_writer=csv.writer(csv_file)
csv_writer.writerow(['PlayerName', 'PlayerLink', 'PlayerPosition'])

try:
    nbaPage = urlopen('https://www.nba.com/players')
except HTTPError as e:
    print('e')
except URLError as e:
    print('The Server could not be found')

try:
     soup = bs(nbaPage.read(),'html.parser')
     badContent = soup.find("nonExistingTag")
except AttributeError as e:
     print('Tag was not found')
else:
    if badContent == None:
       print('Tag was not found')
    else:
       print(badContent)
nbaPage.close()
items = soup.find('section', class_="row nba-player-index__row")
for item in items.children:
    player = item.a['title']
    player_link = 'https://www.nba.com/players' + item.a['href']
    player_pos = item.find('div',class_="nba-player-index__details").span.text
    # print(item.a.img['data-src'])
    csv_writer.writerow([player,player_link,player_pos])
print('File successfully created')
csv_file.close()





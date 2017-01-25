'''
GENIUS LYRICS ANALYSIS

Setup:
1. get an account at genius.com
2. suffer
3. created html page to get token
4. had to have 'bearer
5. had to change data=data to params=data
6.installing bs4 - had to do as admin
'''

import requests
from bs4 import BeautifulSoup

base_url = 'http://api.genius.com'
headers = {'Authorization': 'Bearer TOKEN'}

artist_name = "Tom Misch"
song_title = "in the midst of it all"

def lyrics_from_song_api_path(song_api_path):
  song_url = base_url + song_api_path
  response = requests.get(song_url, headers=headers)
  json = response.json()
  path = json["response"]["song"]["path"]

  #gotta go regular html scraping... come on Genius
  page_url = "http://genius.com" + path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")

  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]

  #at least Genius is nice and has a tag called 'lyrics'!
  lyrics = html.find("lyrics").get_text()
  return lyrics

if __name__ == "__main__":

    search_url = base_url + '/search'
    data = {'q': song_title}
    response = requests.get(search_url, params=data, headers=headers)

    song_info = None
    json = response.json()

    for hit in json['response']['hits']:
        if hit['result']['primary_artist']['name'] == artist_name:
            song_info = hit
    if song_info:
        song_api_path = song_info['result']['api_path']
        print (lyrics_from_song_api_path(song_api_path))




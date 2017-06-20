'''GENIUS LYRICS SCRAPER 
* Python 3
* For informational purposes only
** Based on this blog post: https://tinyurl.com/geniusscraper

Setup:
1. Get an account at http://genius.com/. 
2. Get your token at http://genius.com/api-clients or... You can use the client access token associated 
with your API instead of tokens for authenticated users, get one at https://docs.genius.com/. These 
tokens are only valid for read-only endpoints that are not restricted by a required scope.
'''

import requests
from bs4 import BeautifulSoup

base_url = 'http://api.genius.com'
headers = {'Authorization': 'Bearer YOURTOKENHERE'}

song_title = 'Sad but True'
artist_name = 'Metallica'

def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json['response']['song']['path']

    # Regular HTML scraping
    page_url = 'http://genius.com' + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find(class_='lyrics').get_text()
    return lyrics

if __name__ == '__main__':
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
        print(song_info['result']['full_title'])
        print(lyrics_from_song_api_path(song_api_path))
    else:
        print(artist_name + ' - ' + song_title + ': Not found')
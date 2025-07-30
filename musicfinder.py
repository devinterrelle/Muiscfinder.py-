from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import lyricsgenius

app = Flask(__name__)

# Genius API setup
GENIUS_API_KEY = "JTKb0CG2Y-UWAfZDHnhLqXH3ZyS1zRYeRo9xjhF4um-F_0_hpJrRqJhmM6OygkCY"
genius = lyricsgenius.Genius(GENIUS_API_KEY, timeout=15)
genius.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_lyrics(song_title, artist_name):
    try:
        song = genius.search_song(song_title, artist_name)
        return song.lyrics if song else "Lyrics not found"
    except Exception as e:
        print(f"⚠️ Genius API error: {e}")
        return "Lyrics not available due to an error."

def search_whosampled(song_title, artist):
    search_url = f"https://www.whosampled.com/search/?q={song_title.replace(' ', '+')}+{artist.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    results = []
    for link in soup.find_all('a', href=True):
        if '/track/' in link['href']:
            results.append("https://www.whosampled.com" + link['href'])
    return results[:1]

@app.route('/', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        song = request.form['song']
        artist = request.form['artist']
        lyrics = get_lyrics(song, artist)
        sample_links = search_whosampled(song, artist)
        return render_template('results.html', song=song, artist=artist, lyrics=lyrics, sample_links=sample_links)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
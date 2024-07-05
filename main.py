from flask import Flask, redirect, url_for, session, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import os

app = Flask(__name__)

# Set up Flask configuration
app.config['SECRET_KEY'] = os.urandom(64)

# Spotify API credentials
client_id = '4b25d28dda304700a3171fad5c5907de'
client_secret = 'a2d71986176741c2a97fef411aacdb47'
redirect_uri = 'https://localhost:5000/callback'
scope = 'playlist-read-private'

# Initialize the cache handler for Spotify OAuth
cache_handler = FlaskSessionCacheHandler(session)

# Initialize the Spotify OAuth object
sp_oauth = SpotifyOAuth(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        scope=scope,
                        cache_handler=cache_handler,
                        show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def index():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_playlists'))
    

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))

@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_html = '<br>'.join([f'{name}: {url}' for name, url in playlists_info])

    return playlists_html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=('cert.pem', 'key.pem'))

from flask import request

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

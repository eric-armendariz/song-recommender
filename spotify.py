from __future__ import print_function
import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read'

def count_artists(results, artists, artistSet):
    if ('items' in results):
        for i, item in enumerate(results['items']):
            track = item['track']
            artist_name = track['artists'][0]['name'].lower()
            artists[artist_name] = artists.get(artist_name, 0) + 1

            if artist_name not in artistSet:
                artistSet.add(artist_name)

    return artists, artistSet

class SpotipyWrapper:
    def __init__(self, user_name, client_id, client_secret, redirect_uri="http://localhost:8080"):
        scope = 'user-library-read'
        self.token = util.prompt_for_user_token(user_name, scope, client_id, client_secret,
                                            redirect_uri)
        self.artistFreq = {}
        self.artistNames = set()
        self.username = user_name

    def recommend_playlists(self):
        if self.token:
            sp = spotipy.Spotify(auth=self.token)
            results = sp.current_user_playlists()
            for playlist in results['items']:
                playlist_info = sp.playlist(playlist['id'], fields="tracks, next")
                tracks = playlist_info["tracks"]
                self.artistFreq, self.artistNames = count_artists(tracks, self.artistFreq, self.artistNames)

                while tracks['next']:
                    tracks = sp.next(tracks)
                    self.artistFreq, self.artistNames = count_artists(tracks, self.artistFreq, self.artistNames)
        else:
            print("Don't have token for ", self.username)

    def get_artist_names(self):
        return self.artistNames
    
    def get_artist_freq(self):
        return self.artistFreq
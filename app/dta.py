import spotipy
from spotipy.util import prompt_for_user_token
from spotipy.oauth2 import SpotifyClientCredentials
from app.config import Config
cid=Config.cid
sec=Config.sec

ccm=SpotifyClientCredentials(client_id=cid,client_secret=sec)
sp=spotipy.Spotify(client_credentials_manager=ccm)

def search_artist(artist):
    ss = sp.search(artist, limit=1, type='artist')
    artist_info={
        'name':ss['artists']['items'][0]['name'],
        'id':ss['artists']['items'][0]['id'],
        'genres':ss['artists']['items'][0]['genres'],
        'popularity':ss['artists']['items'][0]['popularity'],
        'followers':ss['artists']['items'][0]['followers']['total']
    }
    return artist_info


def related_artist(art):
    ss = sp.artist_related_artists(search_artist(art)['id'])
    artist_info=[{'name':ss['artists'][i]['name'],
                  'id':ss['artists'][i]['id']}
                 for i in range(len(ss['artists'])) ]
    return artist_info

def top_tracks(artist):
    tr = sp.artist_top_tracks(search_artist(artist)['id'])
    top_tracks= [{'track name':tr['tracks'][i]['name'] ,
             'track id':tr['tracks'][i]['id'],
             'album':tr['tracks'][i]['album']['name'],
             'track popularity':tr['tracks'][i]['popularity']
              }for i in range(len(tr['tracks']))]

    return top_tracks

def nr():
    a = [
        {'album name':sp.new_releases()['albums']['items'][i]['name'],
         'artist':sp.new_releases()['albums']['items'][i]['artists'][0]['name']
        }
        for i in range(10)]
    return a
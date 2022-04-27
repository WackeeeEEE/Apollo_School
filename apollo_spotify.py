import requests
from requests.auth import HTTPBasicAuth
import datetime
import json
from apollo_config import CONF


# Disable Warnings
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CONF = CONF()

BASE = "https://api.spotify.com/v1/tracks/"

class SpotifyTrack:
    def __init__(self, info):
        try:
            self.artists = []
            for artist in info["artists"]:
                self.artists.append(artist["name"])
            self.name = info["name"]
            self.album = info["album"]["name"]
            self.id = info["id"]
            self.uri = info["uri"]
            self.valid = True
        except Exception as e:
            print(e)
            self.valid = False

def getToken():
    global SPOTIFYTOKEN
    global tokenTimer
    resp = requests.post("https://accounts.spotify.com/api/token", {
        'grant_type': 'client_credentials',
        'client_id': CONF.SPOTIFYAPPID,
        'client_secret': CONF.SPOTIFYSECRET
        })
    resp_json = resp.json()
    try:
        SPOTIFYTOKEN = resp_json['access_token']
        tokenTimer = datetime.datetime.now()
        print(f"New Spotify Token: {SPOTIFYTOKEN}")
        return SPOTIFYTOKEN
    except:
        print("Token acquisition failed!")

def refreshToken():
    if (datetime.datetime.now() - tokenTimer).seconds >= 3500:
        getToken()

def GetIdFromLink(link):
    return link.split('/')[-1].split('?')[0]

def GetSpotifyTrackInfo(id):
    refreshToken()
    url = BASE + id
    info = requests.get(url + "?market=ES", headers={
        'Authorization':f"Bearer {SPOTIFYTOKEN}",
        'Accept': 'application/json',
        'Content-Type':'application/json',
        }).json()
    track = SpotifyTrack(info)
    if track.valid == True:
        return track
    else:
        return False


    
getToken()
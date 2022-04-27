import json
import os

CONFIG = json.load(open("CONFIG.json", "r"))
CREDENTIALS = json.load(open("CREDS.json", "r"))

class CONF:
    def __init__(self):
        self.CWD = os.getcwd()
        self.DOWNLOADS_FOLDER = CONFIG["DownloadPathRel"]
        self.YT_DESTINATION_FOLDER = CONFIG["YoutubeDestinationPath"]
        self.SP_DESTINATION_FOLDER = CONFIG["SpotifyDestinationPath"]
        self.VC = CONFIG["VC"]
        self.DOS_LOC = CONFIG["DownOnSpotPathAbs"]

        self.APPID = CREDENTIALS["AppId"]
        self.PUBLIC_KEY = CREDENTIALS["Public_Key"]
        self.TOKEN = CREDENTIALS["Token"]
        self.PERMISSIONS = CREDENTIALS["Permissions"]
        self.ADDURL = CREDENTIALS["AddUrl"]
        self.SPOTIFYAPPID = CREDENTIALS["SpotifyAppId"]
        self.SPOTIFYSECRET = CREDENTIALS["SpotifySecret"]
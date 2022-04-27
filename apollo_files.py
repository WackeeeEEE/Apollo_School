#import discord
#import pytube
# import shutil
from asyncio import subprocess
import json
import pafy

# from subprocess import Popen, PIPE
import subprocess
import os

import apollo_config
import apollo_spotify as spotify

CONF = apollo_config.CONF()

def getYoutubeTitle(link):
    try:
        return pafy.new(link).title
    except Exception as e:
        return e

# def getSpotifyInfo(link):
#     try:
#         proc = Popen([CONF.DOS_LOC, link])
#         (output, err) = proc.communicate()
#     except:
#         print()

def downloadYoutube(link):
    try:
        ytLink = pafy.new(link, basic=True)
        aBest = ytLink.getbestaudio()
        aBest.title
        print(f"Downloading {aBest.title} from {link} to {os.path.join(CONF.CWD, CONF.YT_DESTINATION_FOLDER)}...")
        file_path=os.path.join(CONF.CWD, CONF.YT_DESTINATION_FOLDER, ytLink.title) + "." + aBest.extension
        file = aBest.download(filepath=file_path)
        print("Done!")
        return file_path
    except Exception as e:
        return e

def downloadSpotify(link):
    try:
        proc = subprocess.run([CONF.DOS_LOC, link])
        #(output, err) = proc.communicate()
        print(proc)
        id = spotify.GetIdFromLink(link)
        file_path = os.path.join(CONF.CWD, "downloads", id) + ".ogg"
        return file_path
    except:
        print(f"Downloading '{link}' failed D:")
    return # do things

def pollDirectory():
    absolute_downloads = os.path.join(CONF.CWD, CONF.SP_DESTINATION_FOLDER)
    files = [f for f in os.listdir(absolute_downloads) if os.path.isfile(os.path.join(absolute_downloads, f))]
    if files != []:
        for file in files:
            # migrate(file)
            return

            #tagAndMigrate(file)

# def migrate(file):
#     head, tail = os.path.split(file)
#     shutil.copy2(file, os.path.join(DESTINATION_FOLDER, tail))
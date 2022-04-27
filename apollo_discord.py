from enum import auto
from multiprocessing import context
from multiprocessing.sharedctypes import Value
import discord
from discord.ext import commands


import json
import requests
import asyncio
#from pytube.helpers import regex_search
from apollo_config import CONF
from apollo_queue import Player, Song
import apollo_queue
import apollo_files as files
import apollo_spotify as spotify

# Disable Warnings
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CONF = CONF()
print(discord.__version__)

apollo = commands.Bot(command_prefix='!')

@apollo.event
async def on_connect():
    print("Connected to Discord!")


@apollo.event
async def on_ready():
    print('Guilds:')
    for guild in apollo.guilds:
        print("  - " + str(guild))
    print(f"Initializing Player...")
    global lyre
    lyre = Player(apollo)
    asyncio.ensure_future(lyre.manager())
    lyre.loopollo.run_forever()

# @apollo.event
# async def on_command(msg):
#     command = msg_to_com(msg)
#     print("on_command:", command)

# Whiteboard

# @apollo.event
# async def on_message(msg):
#     print(f"Detected command: {msg.content}")

# Commands

# Play from Link (agnostic)
@apollo.command(name='play')
async def _play_from_link_A(ctx: commands.Context, *args):
    url = args[-1]
    print("Attempting to play song from any link:", url)
    site = urlType(url)

    if site == 0:
        await respond(ctx, f"Invalid link?")

    if site == 1:
        if verifyYT(url) == True:
            title = files.getYoutubeTitle(url)
            print(f"Downloading {title}...")
            s = Song(url, ctx.author, title, files.downloadYoutube(url))
            lyre.playlist.addToBack(s)
            await ctx.send(f"<@{ctx.author.id}> Successfully added {title} to the start of the queue (position {lyre.playlist.getSize() - 1}/{lyre.playlist.getSize() - 1})")
            
    if site == 2:
        if verifySpotify(url) == True:
            info = spotify.GetSpotifyTrackInfo(spotify.GetIdFromLink(url))
            title = f"{info.name} - {' | '.join(info.artists)}"
            print(f"Downloading {title}...")
            s = Song(url, ctx.author, title, files.downloadSpotify(url))
            lyre.playlist.addToBack(s)
            await ctx.send(f"<@{ctx.author.id}> Successfully added {title} to the start of the queue (position {lyre.playlist.getSize() - 1}/{lyre.playlist.getSize() - 1})")

    # Initial Condition
    if lyre.vc.is_connected() == None:
        lyre.vc.connect()

    if lyre.playlist.getSize() == 1:
        print("Starting new playlist session...")
        await ctx.send(f"<@{ctx.author.id}> Starting new playlist session...")
        await lyre.start()

@apollo.command(name='resume')
async def _resume(ctx: commands.Context, *args):
    await lyre.resume()
    await ctx.send(f"<@{ctx.author.id}> Resuming...")
    # else:
    #     await ctx.send(f"<@{ctx.authorid}> Failed to resume D:")

@apollo.command(name='start')
async def _start(ctx:commands.Context, *args):
    await lyre.start()

@apollo.command(name='trackinfo')
async def _get_track_info_spotify(ctx: commands.Context, *args):
    result = verifySpotify(args[-1])
    if result == True:
        await ctx.send()

# @apollo.command(name='playnext')
# async def _playnext_from_link_A(ctx, *args):
#     return

@apollo.command(name='skip')
async def _skip(ctx: commands.Context, *args):
    await lyre.pause()
    await respond(ctx, f"Skipping {lyre.playlist.q.popleft().getTitle()}...")
    await lyre.playNext()

@apollo.command(name='pause')
async def _pause(ctc: commands.Context, *args):
    await lyre.pause()

@apollo.command(name='upnext')
async def _up_next(ctx: commands.Context, *args):
    ret: list[Song] = lyre.playlist.getTop()
    e = ""
    for index, song in enumerate(ret):
        if e == "":
            e += f"{index}: {song.getTitle()}"
        else:
            e += f"\n{index}: {song.getTitle()}"
    if e == "":
        e += "No songs are currently in the queue D:"
    await respond(ctx, e)

@apollo.command(name='nowplaying')
async def _now_playing(ctx: commands.Context, *args):
    await respond(ctx, f"Now Playing:\n{lyre.getNowPlaying().getTitle()}\n{lyre.getNowPlaying().getUrl()}")




# Helpers

# Strings

  # Message to command
def msg_to_com(s):
    words = s.split(" ")
    print(words)
    return words

  # URL detection
def urlType(url): # 1-youtube 2-spotify
    if "spotify" in url:
        print("spotify link detected...")
        return 2
    elif "youtu" in url:
        print("youtube link detected...")
        return 1
    else:
        print("bad link detected...")
        return 0 # fail

def verifyYT(url):
    title = files.getYoutubeTitle(url)
    if title != Exception:
        return True
    else:
        print(title)
        return False

def verifySpotify(url):
    info = spotify.GetSpotifyTrackInfo(spotify.GetIdFromLink(url))
    if info != False:
        print(f"Name: {info.name}\nArtists: {info.artists}\nUrl: {info.uri}")
        return True
    else:
        print(f"{url} could not not be verified D:")
        return False

async def respond(ctx: commands.Context, resp):
    await ctx.send(f"<@{ctx.author.id}>\n{resp}")

# async def playerMain():
#     # Main state loop
#     asyncio.sleep(1)
#     # if lyre.playlist.getSize() > 0: empty = False
#     # else: empty = True
#     vcs = lyre.player.voice_clients()
#     for vc in vcs:
#         if vc.channel.id == CONF.VC:
#             lyreVC = vc
apollo.run(CONF.TOKEN)

import asyncio
from typing import List
from collections import deque
import discord
from discord.ext import commands
from pkg_resources import ensure_directory

from apollo_config import CONF

CONF = CONF()

import asyncio

class Song:
    def __init__(self, source, user, title, location):
        self.source = source
        self.user = user
        self.title = title
        self.location = location

    def getUser(self):
        return self.user

    def getUrl(self):
        return self.source

    def getTitle(self):
        return self.title

    def getLocation(self):
        return self.location

class Playlist:
    def __init__(self, TOP):
        self.top = TOP
        self.q = deque() # list of Song Objects

    def getTop(self):
        if len(self.q) > self.top:
            return list(self.q)[0:(self.top)]
        else:
            return self.q
    
    def promote(self, src):
        try:
            obj: Song = self.q[src]
            del self.q[src]
            self.q.appendleft(obj)
            resp = f"Moved {obj.getTitle()} to the top of the playlist."
            print(resp)
        except Exception as e:
            print(e)
            return False
        
    def getSize(self):
        return len(self.q)

    def addToBack(self, obj: Song):
        try:
            self.q.append(obj)
            resp = f"Successfully added {obj.getTitle()} to the end of the queue (position {len(self.q) - 1}/{len(self.q) - 1})"
            print(resp)
            print(f"playlist size: {self.getSize()}")
            return resp
        except Exception as e:
            print(e)
            return False

    def addToFront(self, obj: Song):
        try:
            self.q.append(obj)
            resp = f"Successfully added {obj.getTitle()} to the start of the queue (position {0}/{len(self.q) - 1})"
            print(resp)
        except Exception as e:
            print(e)
            return False

class Player:
    def __init__(self, player: commands.Bot):
        self.player = player
        self.playlist = Playlist(5)
        asyncio.create_task(self.ensureConnected())
        self.state = None
        self.loopollo = asyncio.get_event_loop()

    def getNowPlaying(self):
        return self.playlist.q[0]

    async def manager(self):
        while True:
            await asyncio.sleep(1)
            if self.state == "playall":
                if not self.vc.is_playing():
                    await self.playNext()
            print("Hello, manager is working! :D")

    async def playNext(self):
        await self.ensureConnected()
        try:
            if self.playlist.getSize() > 0:
                song: Song = self.playlist.q[0]
                if self.vc.is_playing():
                    return
                self.vc.play(discord.FFmpegPCMAudio(song.getLocation()))
                while self.vc.is_playing():
                    await asyncio.sleep(1)
                print(f"Song completed: {self.playlist.q.popleft().getTitle()}")
        except:
            print(f"Could not find any songs in the playlist D:")
            return

    async def pause(self):
        if not self.vc.is_connected():
            print(f"VC not connected")
            return False
        if not self.vc.is_playing():
            print(f"VC not playing")
            return False
        else:
            self.vc.pause()
            self.state = "pause"

    async def resume(self):
        if not self.vc.is_connected():
            print(f"VC not connected")
            return False
        if not self.vc.is_paused():
            print(f"VC not paused")
            return False
        else:
            await self.vc.resume()
            self.state = "playall"
            return True

    async def start(self):
        await self.ensureConnected()
        if not self.vc.is_connected():
            print(f"VC not connected")
            return False
        if self.vc.is_paused():
            self.vc.resume()
            while self.vc.is_playing():
                await asyncio.sleep(1)
            self.state = "playall"
            await self.playNext()
        else:
            self.state = "playall"
            await self.playNext()

    async def ensureConnected(self):
        vcs: list[discord.VoiceClient] = list(self.player.voice_clients)
        for vc in vcs:
            if vc.channel.id == CONF.VC:
                self.vc = vc
                print(f"Found voice channel {vc.channel.id}")
                return
        voice_channel: discord.VoiceChannel = self.player.get_channel(CONF.VC)
        await voice_channel.connect()
        vcs: list[discord.VoiceClient] = list(self.player.voice_clients)
        for vc in vcs:
            if vc.channel.id == CONF.VC:
                self.vc = vc
                print(f"Found voice channel {vc.channel.id}")
        print("Lyre is tuned!")
        

    




    # async def leave(self):
    #     try:
    #         await self.vc.disconnect()
    #         return True
    #     except Exception as e:
    #         print(e)
    #         return False

# class Queue:
#     TOP = 5 # size of top list
#     def __init__(self, TOP):
#         self.top = TOP
#         self.data = [list[Song]] # list of Song Objects

#     def getTop(self):
#         return self.data[0:self.top]

    # def promote(self, src):
    #     self.move(src, 0)

    # def move(self, src, dst):
    #     if src != len(self.data) - 1:
    #         obj: Song = self.data.pop(src)
    #         for e in self.data[src + 1:]:
    #             self.data[e-1] = self.data[e]
    #     else:
    #         obj = self.data.pop(src)
    #     print(f"Successfully moved {obj.getTitle()} from position {src} to position {dst}.")

    # def insert(self, obj: Song, dst): # obj: Song
    #     self.data.insert(dst, obj)
    #     print(f"Successfully inserted {obj.getTitle()} into position {dst}.")



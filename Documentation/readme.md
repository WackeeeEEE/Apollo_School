# Cutting the Cloud
This project was the beginning of an effort to become less reliant on multiple cloud services, and condense the use of multiple media platforms into one seamless and externally available solution. This includes:
 - Personal server build:
   - NAS (Network Accessible Storage)
   - OpenVPN (Global access to personal cloud storage)
   - Plex (Personal storage/playback of all locally stored media)
   - Apollo (Personal discord request/playback jukebox)



# Apollo - The all-in-one jukebox for Discord
![Apollo logo, credit Hi-Rez Studios](/Apollo.png)

The goal here is to have a Discord Bot streaming music to whatever channel(s) it's bound to, using Plex as a storage medium, but also with live request functions through spotify and youtube links. I'm using DownOnSpot as the mechanism for ripping the music from Spotify (Disclaimer: This is not for commercial use and I own all of the content I'm ripping yadayada.)

## Building DownOnSpot
### Repo: https://github.com/oSumAtrIX/DownOnSpot
Some of the key steps that were a little hairy:
   - Install Rust: https://www.rust-lang.org/tools/install ![Rust installation](/Documentation/Install_Rust.png)
   - Update Rust for Nightly Release
     - DownOnSpot is written for Nightly Rust, so we'll need to download that toolchain as well; thankfully, the Cargo system does this painlessly.
![Rust Nightly](/Documentation/Rust_Update_For_Nightly.png)
   - Setting up SSH private key for free account use:
  ![SSH in VM during DownOnSpot Build](/Documentation/SSH_build.png)
     To access the LibreSpot library, we need to use a private key. So let's make a config file at ~/.ssh/ and follow the guide to import the key.
   - Install the mp3lame library: `sudo apt-get install libmp3lame-dev`
   - Depending on your OS, you may need to install additional build tools

## Youtube Support
I tried the pytube3 library here - `pip install pytube3` but it had issues parsing new youtube links; I might try to patch it to work properly later

Next attempt is the pafy library - `pip install youtube-dl pafy` - it doesn't require the youtube-dl backend but it's recommended

Youtube made this a bit rough, when they removed Dislikes from the API - this library still expects them to be visible, and doesn't catch errors associated with missing that data.

So let's just dive into the youtube-dl backend and rip out the dislike stuff, since we don't really care about it anyway. 

![youtube-dl backend 1](/Documentation/youtube-dl_extract_info.png)

![youtube-dl backend 2](/Documentation/youtube-dl_info.png)


## Scripting the Migration (TODO)
We're gonna migrate the files from DownOnSpot to the Plex Library once downloaded. Let's use a quick python script that reads a folder constantly, and copies files over

## Scripting DownOnSpot (TODO)

## Automatic Tagging with MusicBrainz Picard (TODO)
When songs are downloaded using DownOnSpot, their tags are very scuffed - So we'll fix that by fingerprinting the content with MusicBrainz Picard, a great open-source utility for tagging and re-structuring a large music library.

## Discord Bot
Let's get some user input, eh? We'll start by creating a new app in the Discord Dev Portal, recording its credentials for later use, and inviting it to the servers we're intending to use with the general oauth link `https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID_HERE&permissions=8&scope=bot`
![Discord 1](/Documentation/Discord_General.png)
![Discord 2](/Documentation/Discord_Token.png)
![Discord 3](/Documentation/Discord_Creds.png)
![Discord 4](/Documentation/Discord_Permissions.png)

We'll probably need FFMpeg as well, so make sure that's set up correctly and PATHed - even if we don't use it here, it's probably showing up later with conversion stuff and decontainerization.

Follow that link, and using Discord's own authorization, we get the bot to join a server.

![Discord 5](/Documentation/Discord_Connect.png)

Now let's play a song! we'll need the Discord Library for Python: `pip install -U discord.py[voice]`

There are some issues with the library's recent rewrite that makes it install oddly, but the documentation seems to line up with it, and autocomplete worked for me - I'll revisit if I run into issues.

We need to identify what discord channel we want the bot to join, write that ID into the config file, and write up some code to make sure the bot can join and leave as we desire

Then we write some play, pause, resume, etc... methods into out Player class, essentially wrapping the discord library's voice call methods (ended up using the FFMpeg methods).


## Config
I created a simple module to handle all the credentials and settings in one spot, that can be reused

## Queue
Let's create some classes for Song, Playlist, and Player. I started out with some simple playlist manipulations like adding to front or back, promotion, deletion.

To easily get track info without downloading the file and parsing the metadata, we'll use the spotify developer API. Setting up the client authorization was a pain, with the documentation all in javascript but we sorted it out. `https://developer.spotify.com/dashboard/` create a spotify developer account and app here.

Go through the token acquisition process, and write in token refresh logic to call whenever the token is about to expire. Job done.
![Spotify 1](/Documentation/Spotify_Bias.png)

Moving on to playback, we've got to link a few of these modules together. When a user asks to play a song, we need to figure out what kind of link that is, so let's write a few helper functions to distinguish between a valid spotify link, a valid youtube link, and garbage. I started out with some simple comparisons, but can make it more robust in the future.

Then we have to tell another library to download them, check for success, and pass those file paths back to us for adding to the playlist's queue structure. This turned out to be quite a doozie.

Youtube was pretty simple, you can easily specify where the file ought to be downloaded right out of the gate.
Spotify, however, always wants to download to the "downloads" folder alongside the down_on_spot executable. I'll deal with that later, and work around it for now.

Once we have the files, we add them to the queue (with some extra safety checks).

With the files in the queue, we then need some methods for properly traversing the queue. THIS WAS AWFUL and i'm surprised it even works at all in its current state, I'm definitely going to need to rewrite it. Short version: anything asynchronous is a brain melter.


## The Server
I've got a box sitting under my living room TV. Specs are:
 - Ryzen 1600
 - 16GB DDR4 @2666MHz, custom timings because the sticks are different, and XMP wouldn't enable
 - Nvidia NVS300: SUPER cheap dual-monitor GPU mass-produced for office workstations. Terrible performance, but for $6 on eBay you can't beat the value. I needed a GPU in the system because the Ryzen 1600 doesn't have an integrated GPU, and neither did the moterboard I was using

I fooled around with using ESXi to manage multiple VMs for some nice segmentation of services. This was a huge headache for a while, because the NIC (Network Interface Controller) built onto the motherboard isn't officially supported by ESXi. To solve this, I had to repackage an image of ESXi sideloading the NIC drivers using a translated guide from a Russian website. It worked, and I was able to get the server going. It worked out OK for most things (built a NAS, plex server, and discord bot) but the GPU Passthrough functionality wasn't quite there and I wanted to have SOME level of GUI somewhere in the build. 

Here's a similar guide that goes over the general flow: https://www.v-front.de/p/esxi-customizer-ps.html

And some community drivers, among which my Realtek 8111 is counted: https://vibsdepot.v-front.de/wiki/index.php/List_of_currently_available_ESXi_packages

After scrapping ESXi, I decided instead to run a bare-metal Debian installation, which leveraged the NVS300 for a native desktop environment. Using AnyDesk (A nice, free, cross-platform, remote desktop solution) I could then do the comfortable high-level desktop management activities I desired.

On Debian I set up KVM. The goal was for each of the VMs to talk to each other on the host-level network, and that turned out to be a headache too, they're not configured initially to be able to do that. This was a great video that explained how to set it up the way I wanted. https://www.youtube.com/watch?v=DYpaX4BnNlg&t=651s

![Server 1](/Documentation/AnyDesk_VM_Manager.png)

 Let's start with the NAS.

### FreeNAS
FreeNAS probably shouldn't be set up in a VM, for most use cases. But this is a pretty low-risk setting so I'm not going to worry too much about the performance implications.

I set up FreeNAS with virtual disks managed by KVM (Again, yes, it's a bad idea, but performance isn't a huge concern, I'll fix it eventually when I have more time to rebuild the thing.) And exposed the datasets to my local network using Samba sharing. I set up some accounts to access the shares under different conditions. NOTE: Windows 10 sharing is awful and suffers from really strange issues when you try to use multiple sets of credentials to access network drives, so things can get hairy - be wary.

![Freenas 1](/Documentation/FreeNAS_Dash1.png)
![Freenas 2](/Documentation/FreeNAS_Data.png)
![Freenas 3](/Documentation/FreeNAS_Pools.png)
![Freenas 4](/Documentation/FreeNAS_Users.png)

In bare-metal Debian, I set up the fstab to automatically mount the samba shares on boot. Can you guess what issue I ran into with this?

*That's right* - The drives try to mount *before the VM is finished booting*. So I have been manually calling `mount -a` whenever I need to reset the server - which isn't often so I haven't bothered yet.

So now I have access to a shared set of storage drives on my network, from mostly every PC in my house. Nice! Now I'll migrate most of my steam library from my SSD and free up some space on my gaming PC.

## Plex Server Setup
I have a Plex server running on bare-metal, with Libraries that are linked right to the NAS we set up earlier. I won't go into specifics, as it's a very simple process to get up and running, and all the configuration you need to do is within the web GUI, provided you've properly set up the networking. Enable outside access, and I can now listen to all my music on the go, ad-free, streamed right to my phone!

![Plex 1](/Documentation/Plex_Public.png)
![Plex 2](/Documentation/Plex_Library.png)
![Plex 3](/Documentation/Plex_Mobile.jpg)
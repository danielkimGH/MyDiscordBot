import discord
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


class MyClient(discord.Client):
    # Event: Called when client login is successful
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    # Event: Called when a Message is created and sent
    async def on_message(self, message):
        # Prevents infinite loop from bot replying to itself
        if message.author.id == self.user.id:
            return

        # Reply to command '!hello', mention_author parameter is for direct reply (e.g. @user-name)
        if message.content.startswith('!hello'):
            await message.reply('Hello there!', mention_author=True)

        # Adds reaction to message for a quick yes/no poll
        if message.content.startswith('YES/NO') or message.content.startswith('yes/no'):
            yes = '\N{THUMBS UP SIGN}'
            no = '\N{THUMBS DOWN SIGN}'
            await message.add_reaction(yes)
            await message.add_reaction(no)

        # Show song queue list
        if message.content.startswith('!queue'):
            queue_list = []

            for item in sp.queue()['queue']:
                artist_name = item['artists'][0]['name']
                song_name = item['name']
                if len(queue_list) <= 5:
                    queue_list.append(f"* {artist_name} : {song_name}\n")
                else:
                    break

            if queue_list:
                await message.channel.send(f'>>> **Queue** *(next 5)*\n'
                                           f'{"".join(queue_list)}')
            else:
                await message.channel.send(">>> Queue is empty")

    ## Events: Shows current song playing on Spotify
    async def on_presence_update(self, before, after):
        if after.activities:
            for activity in after.activities:
                if isinstance(activity, discord.Spotify):
                    channel = discord.utils.get(after.guild.text_channels, name="general")
                    if channel:
                        await channel.send(f'>>> :headphones: **Now Playing**\n'
                                           f'**Artist:** {activity.artist}\n'
                                           f'**Song:** [{activity.title}](<{activity.track_url}>)')

# Load token
load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")

# Intents specifies which events the bot will receive from Discord
# default enables everything except presences, members, and message_content
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                                             client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                                             redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                                                             scope=scope))

client = MyClient(intents=intents)
client.run(token)

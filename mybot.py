import discord
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv


class MyClient(discord.Client):

    def _get_track_URI(self, url_link: str) -> str or None:
        """
        Returns Spotify track URI (str), None otherwise

        Input: Spotify track URL (str)
        """
        url_link_list = url_link.split("/")

        if len(url_link_list) <= 1 or url_link_list[-2] != "track":
            return None

        uri_index = url_link_list.index('track') + 1
        uri = url_link_list[uri_index].split('?si')[0]

        # Track URI validity check
        try:
            uri_check = sp.audio_features(uri)
            if uri_check[0] is None:
                return None
            else:
                return f"spotify:track:{uri}"
        except:
            return None

    def _check_queue_URI(self, uri: str) -> bool:
        """
        Returns True if track URI is not in queue, False otherwise

        Input: uri (str)
        """
        queue_obj = sp.queue()
        current_uri = queue_obj['currently_playing']['uri']
        uri_list = [item['uri'] for item in queue_obj['queue']]
        if uri == current_uri or uri in uri_list:
            return False
        return True

    async def _get_track(self, message):
        """
        Returns currently playing track (str)

        Input: message (Discord Message object)
        """
        track_object = sp.current_playback()
        if track_object is None or track_object['currently_playing_type'] != 'track':
            await message.channel.send(f'>>> **No songs in play**')
        else:
            artist_name = track_object['item']['artists'][0]['name']
            song_name = track_object['item']['name']
            song_URL = track_object['item']['external_urls']['spotify']
            await message.channel.send(f'>>> :headphones: **Now Playing**\n'
                                       f'**Artist:** {artist_name}\n'
                                       f'**Song:** [{song_name}](<{song_URL}>)')

    async def _get_queue(self, message):
        """
        Returns track queue (str)

        Input: message (Discord Message object)
        """
        queue_list = []
        queue_object = sp.queue()
        queue_display_limit = 5

        if queue_object is None or queue_object['currently_playing']['type'] == 'episode':
            await message.channel.send(">>> **Queue is empty**")
        else:
            for item in queue_object['queue']:
                artist_name = item['artists'][0]['name']
                song_name = item['name']
                if len(queue_list) < queue_display_limit:
                    queue_list.append(f"* {artist_name} - {song_name}\n")
                else:
                    break
            await message.channel.send(f'>>> **Queue** *(next {queue_display_limit})*\n'
                                       f'{"".join(queue_list)}')

    async def _add_queue(self, message):
        """
        Adds track to queue

        Input: message (Discord Message object)
        """
        track_uri = self._get_track_URI(message.content)
        if not track_uri:
            await message.channel.send(f'>>> **Invalid track URL**')
        else:
            # Check if song is already in queue
            queue_check = self._check_queue_URI(track_uri)
            if queue_check:
                sp.add_to_queue(track_uri)
                await message.add_reaction('\N{BLACK RIGHT-POINTING TRIANGLE}')
            else:
                await message.channel.send(f'>>> **Track already in queue**')

    # Event: Called when client login is successful
    async def on_ready(self):
        print(f'Bot activated as {self.user}')

    # Event: Called when a Message is created and sent
    async def on_message(self, message):
        # Prevents infinite loop from bot replying to itself
        if message.author.id == self.user.id:
            return

        # Get current song
        if message.content == '!song':
            await self._get_track(message)

        # Get song queue list
        if message.content == '!queue':
            await self._get_queue(message)

        # Add song to queue
        if message.content.startswith('!add'):
            await self._add_queue(message)


# Load token
load_dotenv()
discord_token = os.getenv("DISCORD_BOT_TOKEN")
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                                             client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                                             redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
                                                             scope=scope))

# Intents specifies which events the bot will receive from Discord
# default enables everything except presences, members, and message_content
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

client = MyClient(intents=intents)
client.run(discord_token)

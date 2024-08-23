<h3>My Discord Bot</h3>

Have you ever streamed to an audience while listening to Spotify and wanted to take in
song requests from your audience? This bot can deliver that capability! It shows the information
on the current song, song queue list, and adds song to the queue list!

<h4>Commands</h4>

* <b>!song</b> - Shows the artist and title of current song
* <b>!queue</b> - Shows the next five (5) songs in queue (<i>limited to only show 5 to reduce chat clutter</i>)
* <b>!add <i>{Spotify song URL}</i></b> - Adds song to queue (<i>note: will not add the song if it's already in queue</i>)

<h4>Required Software</h4>

* PyCharm
* Python Libraries: discord, os, spotipy, dotenv
* Spotify desktop

<h4>Setup</h4>

1. Clone this repo and within the root directory of the project folder, create a file called `.env`,
within this file copy and paste the following four (4) lines of text:<p>
`DISCORD_BOT_TOKEN=`<p>
`SPOTIFY_CLIENT_ID=`<p>
`SPOTIFY_CLIENT_SECRET=`<p>
`SPOTIFY_REDIRECT_URI=`<p>
2. We need a Discord bot now. Follow these [instructions](https://discordpy.readthedocs.io/en/stable/discord.html) 
to create one and invite it to your server. Make sure you take note of the token!
3. We also need a Spotify token. Follow these [instructions](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
to create one. Make sure you take note of the client ID, client secret, and redirect URI!
4. With the Discord bot token, Spotify client ID, Spotify client secret, and Spotify redirect URI we just created, 
paste them over to its respective parts within the `.env` file. Remember to save the file too!
5. Open up Spotify and execute `mybot.py`, your bot should now be showing as online within your server
6. Start playing any music on Spotify and then go back to Discord and try out the `!song` command, the bot
will reply with the artist and title of the current song
7. Try out the `!queue` command, the bot will reply with the next 5 songs in queue
8. To add songs to the queue, we need the song URL. This can be obtained by selecting the <b>three-dot icon</b>
on a Spotify track, selecting <b>Share</b>, and then <b>Copy Song Link</b>.<p>For example, I want to add the song
"Like a G6" from the Far East Movement. This is how the command is used after I copy the song URL from Spotify:<p>
`!add https://open.spotify.com/track/4DvhkX2ic4zWkQeWMwQ2qf?si=dcd87cfbf50748a9`

<h4>References</h4>

* [Spotipy.py](https://spotipy.readthedocs.io/en/2.24.0/#)
* [Discord.py](https://discordpy.readthedocs.io/en/stable/index.html#)
* [Spotify](https://developer.spotify.com/documentation/web-api)
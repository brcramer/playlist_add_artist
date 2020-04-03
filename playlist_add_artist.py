# import libraries
import config
import spotipy
import spotipy.util as util

# obtain playlist id from user-input playlist name
def get_playlist_id(spotifyObject):
    playlist_name = input("  Enter playlist name: ")
    searchResults = spotifyObject.search(playlist_name,1,0,"playlist")
    playlist = searchResults['playlists']['items'][0]
    return playlist['id']

# obtain artist id from user-input artist name
def get_artist_id(sp):
    artist_name = input("  Enter artist name: ")
    searchResults = sp.search(artist_name,1,0,"artist")
    artist = searchResults['artists']['items'][0]
    return artist['id']

# obtain all user playlists
def get_all_playlist_id(sp, username):
    playlists = sp.current_user_playlists()
    playlist_ids = []
    for item in playlists['items']:
        playlist_ids.append(item['id'])
    return playlist_ids

# obtain all tracks from playlist
def get_playlist_tracks(sp, playlist_id):
    playlist = sp.user_playlist(username,playlist_id)
    tracks = playlist["tracks"]
    songs = tracks["items"]
    while tracks['next']:
        tracks = sp.next(tracks)
        for item in tracks["items"]:
            songs.append(item)
    return songs

# find tracks by specific artist
def get_tracks_artist(songs, artist_id):
    tracks = []
    for song in songs:
        artists = song['track']['artists']
        for artist in artists:
            if artist_id == artist['id']:
                tracks.append(song['track']['id'])
    return tracks

# get token
username = input("Enter Spotify username: ")
scope = config.scope
client_id = config.client_id
client_secret = config.client_secret
redirect_uri = config.redirect_uri
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

# create Spotify object
sp = spotipy.Spotify(auth=token)

# select playlist to update
print()
print("Choose playlist to update")
playlist_id = get_playlist_id(sp)

# select playlists to add from
print()
if input("Add from all playlists? y/n: ")=='y':
    playlist_add = get_all_playlist_id(sp, username)
else:
    playlist_add = []
    while input("Add songs from another playlist? y/n: ")=='y':
        playlist_add.append(get_playlist_id(sp))

# get current songs in playlist
current_songs = get_playlist_tracks(sp, playlist_id)
current_tracks = []
for song in current_songs:
    current_tracks.append(song['track']['id'])

add_tracks = []
# add artist songs to playlist
while True:
    if input("Add another artist to playlist? y/n: ")!='y':
        break
    artist_id = get_artist_id(sp)

    for playlist in playlist_add:
        # create list of all tracks to add
        new_tracks = get_playlist_tracks(sp, playlist)
        new_tracks = get_tracks_artist(new_tracks, artist_id)
        i = 0
        for i in range(len(new_tracks)):
            if (new_tracks[i] in add_tracks) or (new_tracks[i] in current_tracks):
                continue
            else:
                add_tracks.append(new_tracks[i])

i = 0
for i in range(len(add_tracks)):
    sp.user_playlist_add_tracks(username, playlist_id, [add_tracks[i]])



# import libraries
import config
import spotipy
import spotipy.util as util

# obtain playlist id list from user-input playlist name
def select_playlists(sp, username):
    print()
    print("PLAYLIST SELECTION")
    playlists = []
    playlist_names = []
    playlist_ids = []
    while True:
        # print options
        print()
        print("  Select playlists to add songs from")
        print("    0: finished selection")
        print("    1: add playlists")
        print("    2: add all user playlists")
        print("    3: remove playlists")
        print("    4: list playlists")
        print()
        choice = input("  Select an option: ")

        # return option
        if choice == '0':
            return playlist_ids

        # add playlists
        elif choice=='1':
            while True:
                print()
                playlist = input("    Enter playlist name or RETURN to stop adding: ")
                if playlist:
                    try:
                        search_results = sp.search(playlist,1,0,"playlist")
                        playlist = search_results['playlists']['items'][0]
                        print("         name: " + playlist['name'])
                        print("      made by: " + playlist['owner']['display_name'])
                    except:
                        print("      ERROR: playlist not valid")
                        continue
                    playlists.append(playlist)
                    playlist_ids.append(playlist['id'])
                    playlist_names.append(playlist['name'])
                else:
                    break

        # add all playlists
        elif choice=='2':
            all_playlists = (sp.current_user_playlists())
            playlist_ids = []
            for playlist in all_playlists['items']:
                playlists.append(playlist)
                playlist_ids.append(playlist['id'])
                playlist_names.append(playlist['name'])

        # remove playlists
        elif choice=='3':
            while True:
                i = 0
                print()
                print("    Current playlists:")
                for playlist_name in playlist_names:
                    print("      " + str(i) + ": " + playlist_name)
                    i+=1
                print()
                index = input(("      Enter playlist # or RETURN to stop removing: "))
                if not(len(list(index))):
                    break
                index = int(index)
                if index in range(0,len(playlist_names)):
                    playlists.remove(playlists[index])
                    playlist_names.remove(playlist_names[index])
                    playlist_ids.remove(playlist_ids[index])
                else:
                    print("        ERROR: index not in range")
                    continue

        # list all playlists with details
        elif choice=='4':
            print()
            for playlist in playlists:
                print("    " + playlist['name'])
                print("                 owner: " + playlist['owner']['display_name'])
                print("           description: " + playlist['description'])
                print("      number of tracks: " + str(playlist['tracks']['total']))
                print("                  link: " + playlist['external_urls']['spotify'])
                print()

        # user input invalid
        else:
            print("      ERROR: invalid choice")
            continue

# obtain playlist id list from user-input playlist name
def select_artists(sp, username):
    print()
    print("ARTIST SELECTION")
    artists = []
    artist_names = []
    artist_ids = []
    while True:
        # print options
        print()
        print("  Select artists to add songs from")
        print("    0: finished selection")
        print("    1: add artists")
        print("    2: remove artists")
        print("    3: list artists")
        print()
        choice = input("    Select an option: ")

        # return option
        if choice == '0':
            return artist_ids

        # add artists
        elif choice=='1':
            while True:
                print()
                artist = input("    Enter artist name or RETURN to stop adding: ")
                if artist:
                    try:
                        search_results = sp.search(artist,1,0,"artist")
                        artist = search_results['artists']['items'][0]
                        print("       name: " + artist['name'])
                        print("      genre: " + str(artist['genres']))
                    except:
                        print("      ERROR: artist not valid")
                        continue
                    artists.append(artist)
                    artist_ids.append(artist['id'])
                    artist_names.append(artist['name'])
                else:
                    break

        # remove artists
        elif choice=='2':
            while True:
                i = 0
                print()
                print("    Current artists:")
                for artist_name in artist_names:
                    print("      " + str(i) + ": " + artist_name)
                    i+=1
                print()
                index = input(("      Enter artist # or RETURN to stop removing: "))
                if not(len(list(index))):
                    break
                index = int(index)
                if index in range(0,len(artist_names)):
                    artists.remove(artists[index])
                    artist_names.remove(artist_names[index])
                    artist_ids.remove(artist_ids[index])
                else:
                    print("      ERROR: index not in range")
                    continue

        # list all artists with details
        elif choice=='3':
            print()
            for artist in artists:
                print("    " + artist['name'])
                print("            genre: " + str(artist['genres']))
                print("        followers: " + str(artist['followers']['total']))
                print("       popularity: " + str(artist['popularity']))
                print("             link: " + artist['external_urls']['spotify'])
                print()

        # user input invalid
        else:
            print("      ERROR: invalid choice")
            continue

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
def select_artist_tracks(tracks, artist_id):
    artist_tracks = []
    for track in tracks:
        artists = track['track']['artists']
        for artist in artists:
            if artist_id == artist['id']:
                artist_tracks.append(track['track'])
    return artist_tracks

# determine if track is duplicate
def duplicate_track(track, names):
    duplicate = track['name'] in names
    return duplicate

# add songs to playlist
def add_songs(username, playlist_id, track_ids):
    error = 0
    try:
        for id in track_ids:
            sp.user_playlist_add_tracks(username, playlist_id, [id])
    except:
        print("unable to add songs")
        error = 1
    return error

# get token
print()
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
new_text = ''
while True:
    playlist_name = input("  Enter " + new_text + "playlist name: ")
    try:
        search_results = sp.search(playlist_name,1,0,"playlist")
        playlist = search_results['playlists']['items'][0]
        playlist_id = playlist['id']
    except:
        playlist_id = []
        print("    ERROR: playlist not valid")
        continue
    print()
    print("  Do you want to modify this  playlist?")
    print("              name: " + playlist['name'])
    print("             owner: " + playlist['owner']['display_name'])
    print("       description: " + playlist['description'])
    print("  number of tracks: " + str(playlist['tracks']['total']))
    print("              link: " + playlist['external_urls']['spotify'])
    print()
    if input("  y/n: ")=='y':
        break
    new_text = "new "
    print()

# get minimum number of tracks for each artist
print()
min_tracks = int(input("Enter the minimum number of tracks from each artist: "))

# select playlists to add from
source_playlists = select_playlists(sp, username)

# get current songs in playlist
current_tracks = get_playlist_tracks(sp, playlist_id)
current_ids = []
current_names = []
for track in current_tracks:
    current_ids.append(track['track']['id'])
    current_names.append(track['track']['name'])

# select artists to add
print()
artists = select_artists(sp, username)

print()
print("Adding songs to playlist...")

# add artist songs to playlist
track_ids = []
for artist_id in artists:
    count = 0
    for playlist in source_playlists:
        # create list of all tracks to add
        new_tracks = get_playlist_tracks(sp, playlist)
        new_tracks = select_artist_tracks(new_tracks, artist_id)
        for track in new_tracks:
            if duplicate_track(track, current_names):
                continue
            else:
                count+=1
                track_ids.append(track['id'])
                current_names.append(track['name'])
    if count<min_tracks:
        new_tracks = sp.artist_top_tracks(artist_id,country='US')
        new_tracks = new_tracks['tracks']
        for track in new_tracks:
            if not(count<min_tracks):
                break
            else:
                if duplicate_track(track, current_names):
                    continue
                else:
                    count+=1
                    track_ids.append(track['id'])
                    current_names.append(track['name'])

# add songs to playlist
error = add_songs(username, playlist_id, track_ids)
print()
if error:
    print("ERROR: unable to add songs to playlist")
else:
    print("Successfully added songs to playlist")
print()

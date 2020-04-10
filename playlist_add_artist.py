# import libraries
import config
import spotipy
import spotipy.util as util


# select_playlists
# purpose: obtain playlist id list from user-input playlist name
# inputs: sp (Spotify  object), username (Spotify username)
# outputs: playlist_ids (list if playlist ids for playlists that user wants to add from)
def select_playlists(sp, username):
    # print playlist selection message
    print()
    print("PLAYLIST SELECTION")

    # initialize lists
    playlists = []  # stores playlist objects
    playlist_names = []  # stores playlist names
    playlist_ids = []  # stores playlist ids

    # playlist selection
    while True:
        # print options
        print()
        print("  Select playlists to add songs from")
        print("    0: finished selection")
        print("    1: add playlists")
        print("    2: add all user playlists")
        print("    3: remove playlists")
        print("    4: remove all playlists")
        print("    5: list playlists without details")
        print("    6: list playlists with details")
        print()

        # get user choice
        choice = input("  Select an option: ")

        # option 0: end playlist selection
        if choice == '0':
            return playlist_ids

        # option 1: add playlists
        elif choice == '1':
            while True:
                print()
                playlist = input("    Enter playlist name or RETURN to stop adding: ")
                if playlist:
                    try:
                        search_results = sp.search(playlist, 1, 0, "playlist")
                        playlist = search_results['playlists']['items'][0]
                        print("       name: " + playlist['name'])
                        print("      owner: " + playlist['owner']['display_name'])
                    except:
                        print("      ERROR: playlist not valid")
                        continue
                    if not (playlist['id'] in playlist_ids):
                        playlists.append(playlist)
                        playlist_ids.append(playlist['id'])
                        playlist_names.append(playlist['name'])
                    else:
                        print()
                        print("      ERROR: playlist already added")
                        continue
                else:
                    break

        # option 2: add all playlists
        elif choice == '2':
            print("    All playlists added")
            all_playlists = (sp.current_user_playlists())
            for playlist in all_playlists['items']:
                if not (playlist['id'] in playlist_ids):
                    playlists.append(playlist)
                    playlist_ids.append(playlist['id'])
                    playlist_names.append(playlist['name'])
                else:
                    continue

        # option 3: remove playlists
        elif choice == '3':
            while True:
                i = 1
                print()
                print("    Current playlists:")
                for playlist_name in playlist_names:
                    print("      " + str(i) + ": " + playlist_name)
                    i += 1
                print()
                index = input("      Enter playlist # or RETURN to stop removing: ")

                # check if input is empty
                if not (len(list(index))):
                    break

                try:
                    index = int(index) - 1  # fails if input is not a number
                except:
                    print("        ERROR: index not valid")  # error message
                    continue

                # check if index corresponds to a playlist
                if index in range(0, len(playlist_names)):
                    # remove playlist from playlists, playlist_names, playlist_ids
                    playlists.remove(playlists[index])
                    playlist_names.remove(playlist_names[index])
                    playlist_ids.remove(playlist_ids[index])
                else:
                    print("        ERROR: index not in range")  # error message
                    continue

        # option 4: remove all playlists
        elif choice == '4':
            # empty all playlists
            playlists = []
            playlist_ids = []
            playlist_names = []
            print("    All playlists removed")

        # option 5: list all playlists without details
        elif choice == '5':
            i = 1  # count playlists
            print()
            print("    Current playlists:")
            for playlist in playlists:
                print("      " + str(i) + ": " + playlist['name'])
                i += 1

        # option 6: list all playlists with details
        elif choice == '6':
            i = 1  # count playlists
            print()
            print("    Current playlists:")
            for playlist in playlists:
                print("      " + str(i) + ": " + playlist['name'])
                print("                       owner: " + playlist['owner']['display_name'])
                print("                 description: " + playlist['description'])
                print("            number of tracks: " + str(playlist['tracks']['total']))
                print("                        link: " + playlist['external_urls']['spotify'])
                print()
                i += 1

        # invalid option: user input invalid
        else:
            print("      ERROR: invalid choice")  # error message
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
        print("    3: remove all artists")
        print("    4: list artists without details")
        print("    5: list artists with details")
        print()
        choice = input("    Select an option: ")

        # return option
        if choice == '0':
            return artist_ids

        # add artists
        elif choice == '1':
            while True:
                print()
                artist = input("    Enter artist name or RETURN to stop adding: ")
                if artist:
                    try:
                        search_results = sp.search(artist, 1, 0, "artist")
                        artist = search_results['artists']['items'][0]
                        print("       name: " + artist['name'])
                        print("      genre: " + str(artist['genres']))
                    except:
                        print("      ERROR: artist not valid")
                        continue
                    if not (artist['id'] in artist_ids):
                        artists.append(artist)
                        artist_ids.append(artist['id'])
                        artist_names.append(artist['name'])
                    else:
                        print()
                        print("      ERROR: artist already added")
                        continue
                else:
                    break

        # remove artists
        elif choice == '2':
            while True:
                i = 1
                print()
                print("    Current artists:")
                for artist_name in artist_names:
                    print("      " + str(i) + ": " + artist_name)
                    i += 1
                print()
                index = input("      Enter artist # or RETURN to stop removing: ")
                if not (len(list(index))):
                    break
                try:
                    index = int(index) - 1
                except:
                    print("        ERROR: index not valid")
                    continue
                if index in range(0, len(artist_names)):
                    artists.remove(artists[index])
                    artist_names.remove(artist_names[index])
                    artist_ids.remove(artist_ids[index])
                else:
                    print("        ERROR: index not in range")
                    continue

        # remove all artists
        elif choice == '3':
            artists = []
            artist_names = []
            artist_ids = []
            print("      All artists removed")

        # list all artists without details
        elif choice == '4':
            i = 1
            print()
            print("    Current artists:")
            for artist in artists:
                print("      " + str(i) + ": " + artist['name'])
                i += 1

        # list all artists with details
        elif choice == '5':
            i = 1
            print()
            print("    Current artists:")
            for artist in artists:
                print("      " + str(i) + ": " + artist['name'])
                print("                  genre: " + str(artist['genres']))
                print("              followers: " + str(artist['followers']['total']))
                print("             popularity: " + str(artist['popularity']))
                print("                   link: " + artist['external_urls']['spotify'])
                print()
                i += 1

        # user input invalid
        else:
            print("      ERROR: invalid choice")
            continue


# obtain all tracks from playlist
def get_playlist_tracks(sp, username, playlist_id):
    playlist = sp.user_playlist(username, playlist_id)
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
def add_songs(sp, username, playlist_id, track_ids):
    try:
        for id in track_ids:
            sp.user_playlist_add_tracks(username, playlist_id, [id])
    except:
        return 1
    return 0


def main():
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
            search_results = sp.search(playlist_name, 1, 0, "playlist")
            playlist = search_results['playlists']['items'][0]
            playlist_id = playlist['id']
        except:
            playlist_id = []
            print("    ERROR: playlist not valid")
            print()
            continue
        print("                name: " + playlist['name'])
        print("               owner: " + playlist['owner']['display_name'])
        print("         description: " + playlist['description'])
        print("    number of tracks: " + str(playlist['tracks']['total']))
        print("                link: " + playlist['external_urls']['spotify'])
        print()
        if input("  Do you want to modify this playlist? y/n: ") == 'y':
            break
        new_text = "new "
        print()

    # get minimum number of tracks for each artist
    while True:
        print()
        try:
            min_tracks = int(input("Enter the minimum number of tracks from each artist: "))
        except:
            print("  ERROR: input invalid")
            continue
        break

    # select playlists to add from
    source_playlists = select_playlists(sp, username)

    # get current tracks in playlist
    current_tracks = get_playlist_tracks(sp, username, playlist_id)

    # for each track in playlist, get id and name
    current_ids = []
    current_names = []
    for track in current_tracks:
        current_ids.append(track['track']['id'])
        current_names.append(track['track']['name'])

    # select artists to add
    print()
    artists = select_artists(sp, username)

    # print message to indicate songs added to playlist
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
                    count += 1
                    track_ids.append(track['id'])
                    current_names.append(track['name'])
        if count < min_tracks:
            new_tracks = sp.artist_top_tracks(artist_id, country='US')
            new_tracks = new_tracks['tracks']
            for track in new_tracks:
                if not (count < min_tracks):
                    break
                else:
                    if duplicate_track(track, current_names):
                        continue
                    else:
                        count += 1
                        track_ids.append(track['id'])
                        current_names.append(track['name'])

    # add songs to playlist
    error = add_songs(sp, username, playlist_id, track_ids)
    print()
    if error:
        print("ERROR: unable to add songs to playlist")  # add unsuccessful
    else:
        print("Successfully added songs to playlist")  # add successful
    print()

    return 0

if __name__ == "__main__":
    main()

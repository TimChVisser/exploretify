import spotipy
from spotipy.oauth2 import SpotifyOAuth

auth_url = "https://accounts.spotify.com/api/token"


def count_occurrences(obj_list):
    count_dict = {}
    for item in obj_list:
        if item in count_dict:
            count_dict[item] += 1
        else:
            count_dict[item] = 1
    return sorted(count_dict.items(), key=lambda x: x[1], reverse=True)


def analyze_items(name, items):
    tracks_in_current_playlist = collect_tracks(items)
    print(f'{name}: {len(tracks_in_current_playlist)}')

    artist_ids = collect_artist_ids(tracks_in_current_playlist)
    sorted_artist_ids = count_occurrences(artist_ids)
    artist_id_list = [i[0] for i in sorted_artist_ids]
    artist_tuple_list = []
    genre_count_dict = {}
    i = 0
    while len(artist_id_list[i * 50:i * 50 + 50]) > 0:
        for idx, artist in enumerate(sp.artists(artist_id_list[i * 50:i * 50 + 50])["artists"]):
            if len(sorted_artist_ids) < i * 50 + idx:
                break
            if artist["id"] == sorted_artist_ids[i * 50 + idx][0]:
                artist_tuple_list.append((artist["name"], sorted_artist_ids[i * 50 + idx][1]))
                for genre in artist["genres"]:
                    if genre in genre_count_dict:
                        genre_count_dict[genre] += sorted_artist_ids[i * 50 + idx][1]
                    else:
                        genre_count_dict[genre] = sorted_artist_ids[i * 50 + idx][1]
            else:
                print("WARN: MISMATCHED ARTIST ID")
        i += 1

    print(artist_tuple_list)
    print(sorted(genre_count_dict.items(), key=lambda x: x[1], reverse=True))
    print("")


def collect_tracks(items):
    tracks_in_current_playlist = items["items"]
    while items["next"]:
        items = sp.next(items)
        tracks_in_current_playlist.extend(items["items"])
    return tracks_in_current_playlist


def collect_artist_ids(tracks_in_current_playlist):
    artist_ids = []
    for track in tracks_in_current_playlist:
        for artist in (track["track"]["artists"]):
            artist_ids.append(artist["id"])
    return artist_ids


def analyze_liked_tracks():
    liked_tracks = sp.current_user_saved_tracks()
    analyze_items("Liked tracks", liked_tracks)


def analyze_owned_playlists():
    playlists = collect_playlists()
    owned_playlists = list(filter(lambda playlist: playlist["owner"]["display_name"] == sp.current_user()["display_name"], playlists))
    for playlist in owned_playlists:
        analyze_playlist(playlist)


def collect_playlists():
    results = sp.current_user_playlists()
    playlists = results["items"]

    while results["next"]:
        results = sp.next(results)
        playlists.extend(results['items'])

    return playlists


def analyze_playlist(playlist):
    playlist_items = sp.playlist_items(playlist["id"])
    analyze_items(playlist["name"], playlist_items)


if __name__ == '__main__':
    scope = ["user-library-read", "playlist-read-private"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    analyze_owned_playlists()
    analyze_liked_tracks()

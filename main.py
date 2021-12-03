import spotipy as sp
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pandas as pd
import numpy as np
import time


def main():
    spot_cxn = sp.Spotify(auth_manager=SpotifyOAuth(scope='user-read-recently-played'))
    # TODO: loop 50 at a time to max recently played
    new_batch = spot_cxn.current_user_recently_played(limit=50)
    results = new_batch['items']
    while len(new_batch) > 0:
        before = new_batch['cursors']['before']  # oldest played track gathered
        new_batch = spot_cxn.current_user_recently_played(50, before=before)
        results.extend(new_batch['items'])

    df = pd.DataFrame(data=[item['track']['id'] for item in results],
                      columns=['track_id'])
    df['played_at'] = np.array([item['played_at'] for item in results])
    # TODO: handle other artists in case of multiple
    df['artist_name'] = np.array([item['track']['artists'][0]['name']
                                  for item in results])
    df['artist_id'] = np.array([item['track']['artists'][0]['id']
                                for item in results])
    df['artist_url'] = np.array([item['track']['artists'][0]['external_urls']
                                 ['spotify'] for item in results])
    df['album_name'] = np.array([item['track']['album']['name']
                                 for item in results])
    df['album_release_date'] = np.array([item['track']['album']['release_date']
                                        for item in results])
    df['album_release_date_precision'] = np.array([item['track']['album']['release_date_precision']
                                                   for item in results])
    df['album_url'] = np.array([item['track']['album']['external_urls']['spotify']
                                for item in results])
    df['track_duration_ms'] = np.array([item['track']['duration_ms']
                                        for item in results])
    df['track_name'] = np.array([item['track']['name']
                                 for item in results])
    df['track_id'] = np.array([item['track']['id']
                               for item in results])
    df['track_explicit'] = np.array([item['track']['explicit']
                                     for item in results])
    df['track_url'] = np.array([item['track']['external_urls']['spotify']
                                for item in results])
    df['track_popularity'] = np.array([item['track']['popularity']
                                       for item in results])
    df['track_local_file'] = np.array([item['track']['is_local']
                                       for item in results])
    df['track_number'] = np.array([item['track']['track_number']
                                   for item in results])

    df.to_csv('recentlyplayed_' + time.strftime('%Y%m%d-%H%M%S') + '.csv')


if __name__ == '__main__':
    main()

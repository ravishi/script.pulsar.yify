# -*- coding: utf-8 -*-
from pulsar import provider
import itertools


API_ENDPOINT = "https://yts.to/api/v2"

# All results have the same trackers.
TRACKERS = [
    'udp://open.demonii.com:1337',
    'udp://tracker.istole.it:80',
    'http://tracker.yify-torrents.com/announce',
    'udp://tracker.publicbt.com:80',
    'udp://tracker.openbittorrent.com:80',
    'udp://tracker.coppersurfer.tk:6969',
    'udp://exodus.desync.com:6969',
    'http://exodus.desync.com:6969/announce',
]

# All results have the same rip type. I don't really know if
# all they are ripped blurays, but since the API doesn't give us
# that info, and I usually think YIFY rips are always awesome...
DEFAULT_RIP_TYPE = provider.RIP_BLURAY


def pulsarify(movie):
    return [{
        "name": movie['title_long'],
        "uri": movie['url'],
        "info_hash": t['hash'],
        "trackers": TRACKERS,
        "size": t['size_bytes'],
        "seeds": t['seeds'],
        "peers": t['peers'],
        "resolution": pulsarify_resolution(t['resolution']),
        #"video_codec": int,
        #"audio_codec": int,
        "rip_type": DEFAULT_RIP_TYPE,
        "scene_rating": provider.RATING_PROPER,
        #"language": '',
    } for t in movie['torrents'] if not t['quality'].strip().lower() == '3d']


def pulsarify_resolution(resolution):
    return getattr(provider, 'RESOLUTION_{0}'.format(resolution.upper()), provider.RESOLUTION_UNKNOWN)


def search(query):
    return []


def search_episode(episode):
    return []


def search_movie(movie):
    r = provider.GET(API_ENDPOINT + "/list_movies.json", params={
        "query_term": movie['imdb_id']
    })

    movies = r.json().get('data', {}).get('movies', [])

    result = list(itertools.chain(*map(pulsarify, movies)))

    return result


provider.register(search, search_movie, search_episode)

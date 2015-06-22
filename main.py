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

# The API won't give us any type info, so we have to coin our on.
# Now I don't really know if all YIFY rips are BRRips, but I want
# them to have higher priority on Pulsar.
RIP_TYPE = provider.RIP_BLURAY

# Same thing with the scene rating. We wan't to look cool.
SCENE_RATING = provider.RATING_PROPER


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
        "rip_type": RIP_TYPE,
        "scene_rating": SCENE_RATING,
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

    return list(itertools.chain(*map(pulsarify, movies)))


provider.register(search, search_movie, search_episode)

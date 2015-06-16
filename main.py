# -*- coding: utf-8 -*-
from pulsar import provider
import itertools
import string


API_ENDPOINT = "https://yts.to/api/v2"


def pulsarify(movie):
    return [{
        "name": movie['title_long'],
        "uri": movie['url'],
        "info_hash": t['hash'],
        #"trackers": string,
        "size": t['size_bytes'],
        "seeds": t['seeds'],
        "peers": t['peers'],
        "resolution": int(''.join(c for c in t['quality'] if c in string.digits)),
        #"video_codec": int,
        #"audio_codec": int,
        #"rip_type": int,
        "scene_rating": int(movie['rating'] * 100),
        #"language": '',
    } for t in movie['torrents'] if not t['quality'].strip().lower() == '3d']


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

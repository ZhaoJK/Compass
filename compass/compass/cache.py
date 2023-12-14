import os
import json
import pathlib

from ..globals import RESOURCE_DIR
from ..models import init_model

#Jiakuan ZHAO
#2023.12.14
#bug for non-root user or apptainer container
#no permission for writing cache file back to rescource folder 
#solution: define cache in user's home 

#find home directory according user
HOME_DIR = str(pathlib.Path.home())
PREPROCESS_CACHE_DIR = os.path.join(HOME_DIR, ".COMPASS")

#PREPROCESS_CACHE_DIR = os.path.join(RESOURCE_DIR, 'COMPASS')
if not os.path.isdir(PREPROCESS_CACHE_DIR):
    os.mkdir(PREPROCESS_CACHE_DIR)

# Keys are tuple of (model, media)
_cache = {}
_new_cache = {}

def load(model, media=None):
    global _cache

    if media is None:
        media = model.media

    if not isinstance(model, str):
        model = model.name

    if (model, media) not in _cache:

        cache_file = os.path.join(PREPROCESS_CACHE_DIR,
                                  model, media, "preprocess.json")

        if os.path.exists(cache_file):
            with open(cache_file) as fin:
                out = json.load(fin)

            _cache[(model, media)] = out

        else:
            _cache[(model, media)] = {}
            _new_cache[(model, media)] = True

    return _cache[(model, media)]


def save(model, media=None):
    global _cache

    if media is None:
        media = model.media

    if not isinstance(model, str):
        model = model.name

    cache_data = _cache[(model, media)]

    cache_dir = os.path.join(PREPROCESS_CACHE_DIR, model, media)

    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)

    cache_file = os.path.join(cache_dir, 'preprocess.json')

    with open(cache_file, 'w') as fout:
        json.dump(cache_data, fout, indent=1)

def is_new_cache(model, media=None):
    if media is None:
        media = model.media

    if not isinstance(model, str):
        model = model.name

    if (model, media) in _new_cache:
        return _new_cache[(model, media)]
    else:
        return False

def clear(model, media=None):
    global _cache

    if media is None:
        media = model.media

    if not isinstance(model, str):
        model = model.name

    _cache[(model, media)] = {}

    save(model, media)
"""Spectral-Kit for Asteroids."""

import os

from .filter import Filter  # noqa
from .spectrum import Spectrum  # noqa
from . import svo  # noqa
from .cache import download_sun_vega  # noqa

__version__ = "1.0.0"

# Cache location
PATH_CACHE = os.path.join(os.path.expanduser("~"), ".cache/ska")
os.makedirs(PATH_CACHE, exist_ok=True)

# SKA Auxiliary data
PATH_VEGA = os.path.join(PATH_CACHE, "spectrum_vega.csv")
PATH_SUN = os.path.join(PATH_CACHE, "spectrum_sun.csv")
PATH_FILTER_LIST = os.path.join(PATH_CACHE, "svo_filters.txt")

if not os.path.isfile(PATH_FILTER_LIST):
    svo.download_filter_list()

if not os.path.isfile(PATH_VEGA) or not os.path.isfile(PATH_SUN):
    download_sun_vega()

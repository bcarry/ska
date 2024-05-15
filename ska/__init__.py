"""Spectral-Kit for Asteroids."""

from .filter import Filter  # noqa
from .spectrum import Spectrum  # noqa
from . import svo  # noqa

import os

# Expose API to use
# from .tools import get_svo_filter
# import .core

__version__ = "alpha"

# Cache location
PATH_CACHE = os.path.join(os.path.expanduser("~"), ".cache/ska")
os.makedirs(PATH_CACHE, exist_ok=True)

# SKA Auxiliary data
PATH_VEGA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "lte096-4.0-0.5a+0.0.BT-NextGen.7.dat.csv",
)
PATH_SUN = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "hst_sun.csv"
)

PATH_FILTER_LIST = os.path.join(PATH_CACHE, "svo_filters.txt")

"""Spectral-Kit for Asteroids."""
import os

# Expose API to use
#from .tools import get_svo_filter
#import .core

__version__ = "alpha"

# Path to ska auxilliary files
PATH_CACHE = os.path.join(os.path.expanduser("~"), ".cache/ska")
PATH_VEGA = os.path.dirname(os.path.abspath(__file__))+'/data/lte096-4.0-0.5a+0.0.BT-NextGen.7.dat.csv'


# Check for existence of index file and cache directory
os.makedirs(PATH_CACHE, exist_ok=True)


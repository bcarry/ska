"""Spectral-Kit for Asteroids."""
import os

# Expose API to use
#from .tools import get_svo_filter
#import .core

__version__ = "alpha"

# Path to SKA auxilliary files
PATH_CACHE = os.path.join(os.path.expanduser("~"), ".cache/ska")
PATH_VEGA = os.path.dirname(os.path.abspath(__file__))+'/data/lte096-4.0-0.5a+0.0.BT-NextGen.7.dat.csv'
PATH_SUN = os.path.dirname(os.path.abspath(__file__))+'/data/hst_sun.csv'

# Check for existence of index file and cache directory
os.makedirs(PATH_CACHE, exist_ok=True)


"""Spectral-Kit for Asteroids."""
import os

# Expose API to user
from .core import ska

__version__ = "alpha"

# Path to ska auxilliary files
PATH_CACHE = os.path.join(os.path.expanduser("~"), ".cache/ska")

# Check for existence of index file and cache directory
os.makedirs(PATH_CACHE, exist_ok=True)


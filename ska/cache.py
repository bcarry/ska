"""Cache management for ska"""

import os
import glob
import requests

import ska


# ------
# Functions for cache management
def clear():
    """Remove the cached filters and the acceptable list"""

    filter_ids, filter_files = take_inventory()

    # Remove cached filters
    for f in filter_files:
        os.unlink(os.path.join(ska.PATH_CACHE, f))

    # Remove list of SVO Filters
    os.unlink(os.path.join(ska.PATH_CACHE, "svo_filters.txt"))


def take_inventory():
    """Create lists of the cached filter VOTables.

    Returns
    -------
    list of str
        The path to the cached VOTables.
    """

    # Get all XML in cache
    cached_xmls = set(
        file_ for file_ in glob.glob(os.path.join(ska.PATH_CACHE, "*.xml"))
    )
    cached_ids = set(
        os.path.basename(FILT).replace("_", "/")[:-4] for FILT in cached_xmls
    )

    return cached_ids, cached_xmls


def update_filter_list():
    # TBD doc / handle issue
    ska.svo.download_filter_list()


def update_filters(ids, force=False):
    """Update the cached filters (VOTable files).

    Parameters
    ----------
    ids : list
        List of SVO IDs corresponding to the filters to update.
    """

    # Download filters
    for f in ids:
        ska.svo.download_filter(f, force=force)


# Get Vega and Sun
def download_sun_vega():
    """Download the spectra of the Sun and Vega"""

    try:

        # Get Solar Spectrum
        r = requests.get(
            "https://raw.githubusercontent.com/bcarry/ska/main/data/hst_sun.csv"
        )
        with open(ska.PATH_SUN, "w") as file:
            file.write(r.text)

        # Get Vega Spectrum
        r = requests.get(
            "https://raw.githubusercontent.com/bcarry/ska/main/data/lte096-4.0-0.5a%2B0.0.BT-NextGen.7.dat.csv"
        )

        with open(ska.PATH_VEGA, "w") as file:
            file.write(r.text)

        return True

    except:
        return False

"""Cache management for ska."""

import os
import glob

import ska


# ------
# Functions for cache management
def clear():
    """Remove the cached filters and the acceptable list."""

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
    #cached_xmls = set(file_ for file_ in glob.glob(ska.PATH_CACHE, "*.xml"))
    cached_xmls = set(file_ for file_ in glob.glob(
        os.path.join(ska.PATH_CACHE, "*.xml"))
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

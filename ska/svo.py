import os
import pathlib

import wget

import ska

PATH_FILTERS = os.path.dirname(os.path.abspath(__file__)) + "/../data/svo_filters.txt"

FILTERS = []

with open(PATH_FILTERS, "r") as file:
    FILTERS = [filt.strip() for filt in file]


def download_filter(id):
    """Retrieve a filter VOTable from SVO Filter Service
    http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=voservice

    Parameters
    ==========
    path : str
        The path to a directory in which filters will be stored

    Returns
    =======
    str
        The path to the filter
    """

    # SVO Base URL for queries
    url = f"http://svo2.cab.inta-csic.es/theory/fps3/fps.php?ID={id}"

    # Parse filter name
    parts = id.split("/")
    if len(parts) > 1:
        rep = ska.PATH_CACHE + "/" + parts[0] + "/"
        name = parts[1]
    else:
        rep = ska.PATH_CACHE + "/"
        name = id
    out = rep + name + ".xml"

    # Create directory and download VOTable
    if not os.path.isfile(out):
        pathlib.Path(rep).mkdir(parents=True, exist_ok=True)
        wget.download(url, out=out)

    # Return path to filter VOTable
    return out

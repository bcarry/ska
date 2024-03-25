import io
import os
import requests
from astropy.io.votable import parse

import ska

PATH_FILTERS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "svo_filters.txt"
)

FILTERS = []

with open(PATH_FILTERS, "r") as file:
    FILTERS = [filt.strip() for filt in file]


def download_filter(id):
    """Download a filter VOTable from SVO Filter Service
    http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=voservice

    Parameters
    ==========
    id : str
        The unique SVO filter identifier

    Returns
    =======
    str
        The path to the filter VOTable file
    """

    # Test if the filter ID is valid
    if id not in FILTERS:
        raise ValueError(f"Unknown filter ID {id}. Choose from\n {ska.svo.FILTERS}")

    # SVO Base URL for queries
    url = f"http://svo2.cab.inta-csic.es/theory/fps3/fps.php?"

    # Output name for the filter VOTable
    parts = id.split("/")
    if len(parts) > 1:
        rep = os.path.join(ska.PATH_CACHE, parts[0])
        name = parts[1]
    else:
        rep = ska.PATH_CACHE
        name = id
    out = os.path.join(rep, name + ".xml")

    # Download VOTable
    if not os.path.isfile(out):
        try:
            # Request the filter VOTable
            r = requests.get(url, params={"ID": id})
            SVOFilter = parse(io.BytesIO(r.content))
            filter_info = SVOFilter.get_first_table()

            # Write it to disk
            os.makedirs(rep, exist_ok=True)
            SVOFilter.to_xml(out)

        except:
            raise Exception("Error downloading filter VOTable")

    # Return path to filter VOTable
    return out

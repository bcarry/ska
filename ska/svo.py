import io
import os
import sys
import requests
from astropy.io.votable import parse
import rich

import ska


def download_filter_list():
    """Retrieve the list of filter IDs from `SVO Filter Service <http://svo2.cab.inta-csic.es/theory/fps`__

    Returns
    =======
    list
        The list of filter IDS
    """

    try:

        # Main SVO filter list
        r = requests.get(
            "https://svo.cab.inta-csic.es/files/svo/Public/HowTo/FPS/FPS_info.xml"
        )
        SVOFilters = parse(io.BytesIO(r.content))
        main_id = SVOFilters.get_first_table().to_table().to_pandas().filterID.to_list()

        # Secondary SVO filter list
        r = requests.get(
            "https://svo.cab.inta-csic.es/files/svo/Public/HowTo/FPS/others.xml"
        )
        SVOFilters = parse(io.BytesIO(r.content))
        other_id = SVOFilters.get_first_table().to_table().to_pandas()["__ID"].to_list()

        # Merge and Write to disk
        filter_id = main_id + other_id
        with open(ska.PATH_FILTER_LIST, "w") as file:
            for f in filter_id:
                file.write(f"{f}\n")
        return True

    except:
        # raise Exception("Error downloading filter list")
        rich.print(f"[red]Error downloading filter {id} VOTable[/red].")
        return False


def load_filter_list():
    """Read all filter IDs from a cache list

    Returns
    =======
    list
        The list of filter IDS

    """
    if not os.path.isfile(ska.PATH_FILTER_LIST):
        download_filter_list()

    with open(ska.PATH_FILTER_LIST, "r") as file:
        FILTERS = [filt.strip() for filt in file]
    return FILTERS


def download_filter(id, force=False):
    """Download a filter VOTable from `SVO Filter Service <http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=voservice>`__

    Parameters
    ==========
    id : str
        The unique SVO filter identifier to be downloaded

    force : bool
        If True, the filter VOTable will be downloaded even if it is already cached

    Returns
    =======
    str
        The path to the filter VOTable file
    """

    # Test if the filter ID is valid
    FILTERS = load_filter_list()
    if id not in FILTERS:
        rich.print(
            f"[red]Unknown filter ID {id}[/red]. Use [green]ska filter[/green] to list available filters"
        )
        sys.exit(1)
        # raise ValueError(f"Unknown filter ID {id}. Use ska filter to list available filters")

    # SVO Base URL for queries
    url = f"http://svo2.cab.inta-csic.es/theory/fps3/fps.php?"

    # Output name for the filter VOTable
    out = os.path.join(ska.PATH_CACHE, id.replace("/", "_") + ".xml")

    # Download VOTable
    if (not os.path.isfile(out)) or force:
        try:
            # Request the filter VOTable
            r = requests.get(url, params={"ID": id})
            SVOFilter = parse(io.BytesIO(r.content))
            filter_info = SVOFilter.get_first_table()

            # Write it to disk
            # os.makedirs(ska.PATH_CACHE, exist_ok=True)
            SVOFilter.to_xml(out)

        except:
            rich.print(f"[red]Error downloading filter {id} VOTable[/red].")
            sys.exit(1)
            # raise Exception("Error downloading filter VOTable")

    # Return path to filter VOTable
    return out

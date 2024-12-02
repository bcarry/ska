"""Cache management for ska"""

import os
import glob
import requests

import ska


# --------------------------------------------------------------------------------
# Cache management for Filters
def filter_inventory():
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


def clear_filters():
    """Remove the cached filters and the acceptable list"""

    filter_ids, filter_files = filter_inventory()

    # Remove cached filters
    for f in filter_files:
        os.unlink(os.path.join(ska.PATH_CACHE, f))

    # Remove list of SVO Filters
    os.unlink(os.path.join(ska.PATH_CACHE, "svo_filters.txt"))


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


# --------------------------------------------------------------------------------
# Cache management for Spectra
def spectra_inventory():
    """Create lists of the cached spectra and templates.

    Returns
    -------
    list of str
        The path to the cached spectra
    """

    # Get all spectra
    cached_spectra = set(
        file_ for file_ in glob.glob(os.path.join(ska.PATH_CACHE, "spectrum*.csv"))
    )

    # Get all templates
    cached_templates = set(
        file_ for file_ in glob.glob(os.path.join(ska.PATH_CACHE, "template*.csv"))
    )

    return cached_spectra, cached_templates


def clear_spectra():
    """Remove the cached spectra and templates"""

    cached_spectra, cached_templates = spectra_inventory()

    # Remove cached spectra
    for f in cached_spectra:
        os.unlink(os.path.join(ska.PATH_CACHE, f))

    # Remove cached templates
    for f in cached_templates:
        os.unlink(os.path.join(ska.PATH_CACHE, f))


def download_sun_and_vega():
    """Download the spectra of the Sun and Vega"""

    try:

        # Get the spectrum of the Sun
        r = requests.get(
            "https://raw.githubusercontent.com/bcarry/ska/main/data/e490_sun.csv"
        )
        with open(ska.PATH_SUN, "w") as file:
            file.write(r.text)

        # Get the spectrum of Vega
        r = requests.get(
            "https://raw.githubusercontent.com/bcarry/ska/main/data/vega_stis.csv"
        )

        with open(ska.PATH_VEGA, "w") as file:
            file.write(r.text)

        return True

    except:
        return False


def download_mahlke_taxonomy():
    """Download the template spectra of Mahlke+2022 taxonomy"""

    try:

        # Get the spectrum of the Sun
        r = requests.get(
            "https://raw.githubusercontent.com/bcarry/ska/main/data/template_mahlke2022.csv"
        )
        with open(ska.PATH_MAHLKE, "w") as file:
            file.write(r.text)

        return True

    except:
        return False

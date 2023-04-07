#!/usr/bin/env python
"""
Spectral conversion tools
"""
import wget
import pathlib
import os.path

import pandas as pd
import numpy as np
from astropy.io.votable import parse, parse_single_table
import matplotlib.pyplot as plt

import ska


def load_svo_transmission(filter_id, path=ska.PATH_CACHE):
    """Load a filter transmission curve from SVO Filter Service
    http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=voservice

    Parameters
    ==========
    filter_id: str
        The filter unique ID (see SVO filter service)
    path : str
        The path to a directory in which filters are stored

    Returns
    =======
    pd.DataFrame
        Filter transmission curve from SVO Filter Profile Service
    """
    # Load filter VOTable
    VOFilter = load_svo_filter(filter_id)

    # Return transmission curve
    return pd.DataFrame(data=VOFilter.get_first_table().array.data)


def load_svo_filter(filter_id, path=ska.PATH_CACHE):
    """Load a filter VOTable from SVO Filter Service
    http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=voservice

    Parameters
    ==========
    filter_id: str
        The filter unique ID (see SVO filter service)
    path : str
        The path to a directory in which filters are stored

    Returns
    =======
    VOFilter : astropy.io.votable.tree.VOTableFile
        Filter VOTable from SVO Filter Profile Service
    """
    # Download filter VOTable if not present in cache
    if ~os.path.isfile(ska.PATH_CACHE + "/" + filter_id + ".xml"):
        _ = get_svo_filter(filter_id)

    # Read, parse, return VOTable
    VOFilter = parse(ska.PATH_CACHE + "/" + filter_id + ".xml")
    return VOFilter


def get_svo_filter(filter_id, path=ska.PATH_CACHE):
    """Retrieve a filter VOTable from SVO Filter Service
    http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=voservice

    Parameters
    ==========
    filter_id: str
        The filter unique ID (see SVO filter service)
    path : str
        The path to a directory in which filters will be stored

    Returns
    =======
    str
        The path to the filter
    """

    # SVO Base URL for queries
    url = f"http://svo2.cab.inta-csic.es/theory/fps3/fps.php?ID={filter_id}"

    # Parse filter name
    parts = filter_id.split("/")
    if len(parts) > 1:
        rep = path + "/" + parts[0] + "/"
        name = parts[1]
    else:
        rep = path + "/"
        name = filter_id
    out = rep + name + ".xml"

    # Create directory and download VOTable
    if not os.path.isfile(out):
        pathlib.Path(rep).mkdir(parents=True, exist_ok=True)
        wget.download(url, out=out)

    # Return path to filter VOTable
    return out


def compute_flux(spectrum, filter_id):
    """Computes the flux of a spectrum in a given band.

    Parameters
    ----------
    spectrum : pd.DataFrame
        Wavelength: in Angstrom
        Flux: Flux density (erg/cm2/s/ang)
    filter_id: str
        The filter unique ID (see SVO filter service)

    Returns
    -------
    float
        The computed mean flux density
    """
    # Transmission curve
    VOFilter = load_svo_filter(filter_id)
    trans = load_svo_transmission(filter_id)

    # Integration grid is built from the transmission curve
    trans = trans[trans["Transmission"] >= 1e-5]
    lambda_min = trans["Wavelength"].min()
    lambda_max = trans["Wavelength"].max()

    # Wavelength range to integrate over
    lambda_int = np.arange(lambda_min, lambda_max, 0.5)

    # Detector type
    # Photon counter
    try:
        VOFilter.get_field_by_id("DetectorType")
        factor = lambda_int
    # Energy counter
    except:
        factor = lambda_int * 0 + 1

    # Interpolate over the transmission range
    interpol_transmission = np.interp(
        lambda_int, trans["Wavelength"], trans["Transmission"]
    )

    interpol_spectrum = np.interp(lambda_int, spectrum["Wavelength"], spectrum["Flux"])

    # Compute the flux by integrating over wavelength.
    nom = np.trapz(
        interpol_spectrum * interpol_transmission * factor,
        lambda_int,
    )
    denom = np.trapz(interpol_transmission * factor, lambda_int)
    flux = nom / denom
    return flux


def compute_color(spectrum, filter_id_1, filter_id_2, phot_sys="AB", vega=None):
    """Computes filter_1-filter_2 color of spectrum in the requested system.

    Parameters
    ==========
    spectrum : pd.DataFrame
        Source spectrum. Columns must be
        Wavelength: in Angstrom
        Flux: Flux density (erg/cm2/s/ang)
    filter_id_1: str
        The first filter unique ID (see SVO filter service)
    filter_id_2: str
        The second filter unique ID (see SVO filter service)
    phot_sys : str
        Photometric system in which to report the color (default=AB)
    vega : pd.DataFrame
        Spectrum of Vega. Columns must be
        Wavelength: in Angstrom
        Flux: Flux density (erg/cm2/s/ang)

    Returns
    =======
    float
        The requested color
    """

    # Compute fluxes in each filter
    flux1 = compute_flux(spectrum, filter_id_1)
    flux2 = compute_flux(spectrum, filter_id_2)

    # Magnitude in AB photometric system
    if phot_sys == "AB":
        # Get Pivot wavelength for both filters
        VOFilter_1 = load_svo_filter(filter_id_1)
        pivot_1 = VOFilter_1.get_field_by_id("WavelengthPivot").value

        VOFilter_2 = load_svo_filter(filter_id_2)
        pivot_2 = VOFilter_2.get_field_by_id("WavelengthPivot").value

        # Compute and return the color
        return -2.5 * np.log10(flux1 / flux2) - 5 * np.log10(pivot_1 / pivot_2)

    # Magnitude in Vega photometric system
    elif phot_sys == "Vega":

        # Read Vega spectrum if not provided
        if vega == None:
            vega = pd.read_csv(ska.PATH_VEGA)

        # Compute fluxes of Vega in each filter
        flux1_vega = compute_flux(vega, filter_id_1)
        flux2_vega = compute_flux(vega, filter_id_2)

        # Compute and return the color
        return -2.5 * (np.log10(flux1 / flux1_vega) - np.log10(flux2 / flux2_vega))

    # Magnitude in ST photometric system
    elif phot_sys == "ST":
        return -2.5 * np.log10(flux1 / flux2)


def reflectance_to_color(
    spectrum, filter_id_1, filter_id_2, phot_sys="AB", vega=None, sun=None
):
    """Computes filter_1-filter_2 color for a reflectance spectrum.

    Parameters
    ==========
    spectrum : pd.DataFrame
        Source reflectance spectrum. Columns must be
        Wavelength: in Angstrom
        Reflectance: arbitrary unit
    filter_id_1: str
        The first filter unique ID (see SVO filter service)
    filter_id_2: str
        The second filter unique ID (see SVO filter service)
    phot_sys : str
        Photometric system in which to report the color (default=AB)
    vega : pd.DataFrame
        Spectrum of Vega. Columns must be
        Wavelength: in Angstrom
        Flux: Flux density (erg/cm2/s/ang)
    sun : pd.DataFrame
        Spectrum of the Sun. Columns must be
        Wavelength: in Angstrom
        Flux: Flux density (erg/cm2/s/ang)

    Returns
    =======
    float
        The requested color
    """

    # Define wavelength interval
    # Transmission curves
    trans_1 = load_svo_transmission(filter_id_1)
    trans_2 = load_svo_transmission(filter_id_2)

    # Integration grid is built from the transmission curve
    trans_1 = trans_1[trans_1["Transmission"] >= 1e-5]
    trans_2 = trans_2[trans_2["Transmission"] >= 1e-5]
    lambda_min = np.min([trans_1["Wavelength"].min(), trans_2["Wavelength"].min()])
    lambda_max = np.max([trans_1["Wavelength"].max(), trans_2["Wavelength"].max()])

    # Wavelength range to integrate over
    lambda_int = np.arange(lambda_min, lambda_max, 0.5)

    # Read spectrum othe Sun if not provided
    if type(sun)!=pd.DataFrame: # == None:
        sun = pd.read_csv(ska.PATH_SUN)

    # Interpolate spectrum of the Sun
    interpol_spectrum = np.interp(lambda_int, sun.Wavelength, sun.Flux)
    interp_sun = pd.DataFrame({"Wavelength": lambda_int, "Flux": interpol_spectrum})
    interp_sun = interp_sun.astype("float")

    # Interpolate reflectance spectru,
    interpol_spectrum = np.interp(lambda_int, spectrum.Wavelength, spectrum.Reflectance)
    interp_spectrum = pd.DataFrame(
        {"Wavelength": lambda_int, "Flux": interpol_spectrum * interp_sun.Flux}
    )
    interp_spectrum = interp_spectrum.astype("float")

    # Compute color of the reflectance*Sun spectrum
    return compute_color(
        interp_spectrum, filter_id_1, filter_id_2, phot_sys=phot_sys, vega=vega
    )


def solar_color(filter_id_1, filter_id_2, phot_sys="AB", vega=None):
    """Compute the color of the Sun between two filters

    Parameters
    ==========
    filter_id_1: str
        The first filter unique ID (see SVO filter service)
    filter_id_2: str
        The second filter unique ID (see SVO filter service)
    phot_sys : str
        Photometric system in which to report the color (default=AB)
    vega : pd.DataFrame
        Spectrum of Vega. Columns must be
        Wavelength: in Angstrom
        Flux: Flux density (erg/cm2/s/ang)

    Returns
    =======
    float
        The solar color
    """

    # Load filters VOTable
    filter_1 = load_svo_filter(filter_id_1)
    filter_2 = load_svo_filter(filter_id_2)

    # Exrtract Solar Fluxes
    sun_1 = filter_1.get_field_by_id("Fsun").value
    sun_2 = filter_2.get_field_by_id("Fsun").value

    # Convert to magnitude
    mag_1 = -2.5 * np.log10(sun_1)
    mag_2 = -2.5 * np.log10(sun_2)
    colorST = mag_1 - mag_2

    # Solar color in ST photometric system
    if phot_sys == "ST":
        return colorST

    # Solar color in Vega photometric system
    elif phot_sys == "Vega":
        # Read Vega spectrum if not provided
        if vega == None:
            spec_vega = pd.read_csv(ska.PATH_VEGA)

        # Compute color of Vega
        vega_ST = compute_color(spec_vega, filter_id_1, filter_id_2, phot_sys="ST")
        return colorST - vega_ST

    # Solar color in ST photometric system
    else:
        pivot_1 = filter_1.get_field_by_id("WavelengthPivot").value
        pivot_2 = filter_2.get_field_by_id("WavelengthPivot").value
        return colorST - 5 * np.log10(pivot_1 / pivot_2)

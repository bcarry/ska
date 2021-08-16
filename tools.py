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
    """Load a filter VOTable from SVO Filter Service
    http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=voservice

    Parameters
    ==========
    filter_id: str
        The filter unique ID (see SVO filter service)
    path : str
        The path to a directory in which filters will be stored

    Returns
    =======
    pd.DataFrame
        Filter transmission curve from SVO Filter Profile Service
    """
    if ~os.path.isfile(ska.PATH_CACHE+'/'+filter_id+'.xml'):
        _ = get_svo_filter(filter_id)
    VOFilter = parse(ska.PATH_CACHE+'/'+filter_id+'.xml')
    trans = pd.DataFrame(data=VOFilter.get_first_table().array.data)
    return trans

def load_svo_filter(filter_id, path=ska.PATH_CACHE):
    """Load a filter VOTable from SVO Filter Service
    http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=voservice

    Parameters
    ==========
    filter_id: str
        The filter unique ID (see SVO filter service)
    path : str
        The path to a directory in which filters will be stored

    Returns
    =======
    VOFilter : astropy.io.votable.tree.VOTableFile
        Filter VOTable from SVO Filter Profile Service
    """
    if ~os.path.isfile(ska.PATH_CACHE+'/'+filter_id+'.xml'):
        _ = get_svo_filter(filter_id)
    VOFilter = parse(ska.PATH_CACHE+'/'+filter_id+'.xml')
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
    url = f'http://svo2.cab.inta-csic.es/theory/fps3/fps.php?ID={filter_id}'
    parts = filter_id.split('/')
    if len(parts)>1:
        rep = path+'/'+parts[0]+'/'
        name = parts[1]
    else:
        rep = path+'/'
        name = filter_id
    out = rep+name+'.xml'

    if not os.path.isfile(out):
        pathlib.Path(rep).mkdir(parents=True, exist_ok=True)
        wget.download(url, out=out)
    return out




def compute_flux(spectrum, filter_id):
    """Computes the flux of a spectrum in a given band.

    Parameters
    ----------
    spectrum : pd.DataFrame
        Flux density (erg/cm2/s/ang)
    filter_id: str
        The filter unique ID (see SVO filter service)

    Returns
    -------
    float
        The computed mean flux density
    """
    # Transmission curve
    if ~os.path.isfile(ska.PATH_CACHE+'/'+filter_id+'.xml'):
        _ = get_svo_filter(filter_id)
    VOFilter = parse(ska.PATH_CACHE+'/'+filter_id+'.xml')
        
    trans = pd.DataFrame(data=VOFilter.get_first_table().array.data)

    # Integration grid is built from the transmission curve
    trans = trans[trans["Transmission"] >= 1e-5]
    lambda_min = trans["Wavelength"].min()
    lambda_max = trans["Wavelength"].max()

    # Wavelength range to integrate over
    lambda_int = np.arange(lambda_min, lambda_max, 0.1)

    # Detector type
    # Photon counter
    try:
        VOFilter.get_field_by_id('DetectorType')
        factor = lambda_int
    # Energy counter
    except:
        factor = lambda_int*0 + 1

    # Interpolate over the transmission range
    interpol_transmission = np.interp(
        lambda_int, trans["Wavelength"], trans["Transmission"]
    )

    interpol_spectrum = np.interp(
        lambda_int, spectrum["Wavelength"], spectrum["Flux"]
    )

    # Compute the flux by integrating over wavelength.
    nom = np.trapz(
        interpol_spectrum
        * interpol_transmission
        * factor,
        lambda_int,
    )
    denom = np.trapz(interpol_transmission * factor, lambda_int)
    flux = nom / denom
    return flux


def compute_color_ST(spectrum, filter_id_1, filter_id_2):
    """Computes filter_1-filter_2 color of spectrum in ST system.

    Parameters
    ==========
    spectrum : pd.DataFrame
        Source flux density (erg/cm2/s/ang)
    filter_id_1: str
        The filter unique ID (see SVO filter service)
    filter_id_2: str
        The filter unique ID (see SVO filter service)

    Returns
    =======
    float
        The requested color
    """
    flux1 = compute_flux(spectrum, filter_id_1)
    flux2 = compute_flux(spectrum, filter_id_2)

    return -2.5*np.log10(flux1/flux2)


def compute_color_AB(spectrum, filter_id_1, filter_id_2):
    """Computes filter_1-filter_2 color of spectrum in AB system.

    Parameters
    ==========
    spectrum : pd.DataFrame
        Source flux density (erg/cm2/s/ang)
    filter_id_1: str
        The filter unique ID (see SVO filter service)
    filter_id_2: str
        The filter unique ID (see SVO filter service)

    Returns
    =======
    float
        The requested color
    """
    flux1 = compute_flux(spectrum, filter_id_1)
    flux2 = compute_flux(spectrum, filter_id_2)

    VOFilter_1 = parse(ska.PATH_CACHE+'/'+filter_id_1+'.xml')
    pivot_1 = VOFilter_1.get_field_by_id("WavelengthPivot").value

    VOFilter_2 = parse(ska.PATH_CACHE+'/'+filter_id_2+'.xml')
    pivot_2 = VOFilter_2.get_field_by_id("WavelengthPivot").value

    return -2.5*np.log10(flux1/flux2) - 5*np.log10(pivot_1/pivot_2)



def compute_color_Vega(spectrum, filter_id_1, filter_id_2, vega=None):
    """Computes filter_1-filter_2 color of spectrum in Vega system.

    Parameters
    ==========
    spectrum : pd.DataFrame
        Source flux density (erg/cm2/s/ang)
    vega : pd.DataFrame
        Vega flux density (erg/cm2/s/ang)
    filter_id_1: str
        The filter unique ID (see SVO filter service)
    filter_id_2: str
        The filter unique ID (see SVO filter service)

    Returns
    =======
    float
        The requested color
    """
    flux1 = compute_flux(spectrum, filter_id_1)
    flux2 = compute_flux(spectrum, filter_id_2)

    if vega==None:
        vega = pd.read_csv(ska.PATH_VEGA)

    flux1_vega = compute_flux(vega, filter_id_1)
    flux2_vega = compute_flux(vega, filter_id_2)

    return -2.5 * (np.log10(flux1 / flux1_vega) - np.log10(flux2 / flux2_vega))



def solar_color(filter_id_1, filter_id_2, phot_sys='AB'):
    """Compute the color of the Sun between two filters

    Parameters
    ==========
    filter_id_1: str
        The filter unique ID (see SVO filter service)
    filter_id_2: str
        The filter unique ID (see SVO filter service)
    phot_sys : str
        Photometric system in which to report the color (default=AB)

    Returns
    =======
    dict
        The solar color and the two reference wavelengths
    """    
    file_filter_1 = get_svo_filter(filter_id_1)
    filter_A = parse(file_filter_1)
    
    file_filter_2 = get_svo_filter(filter_id_2)
    filter_B = parse(file_filter_2)
    
    sun_A = filter_A.get_field_by_id("Fsun").value
    sun_B = filter_B.get_field_by_id("Fsun").value

    wave_A = filter_A.get_field_by_id("WavelengthEff").value
    wave_B = filter_B.get_field_by_id("WavelengthEff").value

    mag_A = -2.5*np.log10(sun_A)
    mag_B = -2.5*np.log10(sun_B)
    colorST = mag_A-mag_B
    
    if phot_sys=='ST':
        #return {'wave_A':wave_A, 'wave_B':wave_B, 'color': colorST}
        return colorST

    elif phot_sys=='Vega':
        spec_vega = pd.read_csv(ska.PATH_VEGA)
        vega_ST = compute_color_ST(spec_vega, filter_id_1, filter_id_2) 
        #return {'wave_A':wave_A, 'wave_B':wave_B, 'color': colorST-vega_ST}
        return (colorST-vega_ST)

    else:
        pivot_1 = filter_A.get_field_by_id("WavelengthPivot").value
        pivot_2 = filter_B.get_field_by_id("WavelengthPivot").value
        #return {'wave_A':wave_A, 'wave_B':wave_B, 'color': colorST-5*np.log10(pivot_1/pivot_2)}
        return (colorST-5*np.log10(pivot_1/pivot_2))




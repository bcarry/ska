#!/usr/bin/env python
"""
Spectral conversion tools
"""
import pandas as pd
import numpy as np

import ska


def compute_color(spectrum, filter1, filter2, phot_sys="AB", vega=None):
    """Computes filter_1-filter_2 color of spectrum in the requested system.

    Parameters
    ==========
    spectrum : pd.DataFrame
        Source spectrum. Columns must be
        Wavelength: in Angstrom
        Flux: Flux density (erg/cm2/s/ang)
    filter_1: ska.Filter
    filter_2: ska.Filter
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
    flux1 = filter1.compute_flux(spectrum)
    flux2 = filter2.compute_flux(spectrum)

    # Magnitude in AB photometric system
    if phot_sys == "AB":
        # Get Pivot wavelength for both filters
        pivot_1 = filter1.VOFilter.get_field_by_id("WavelengthPivot").value
        pivot_2 = filter2.VOFilter.get_field_by_id("WavelengthPivot").value

        # Compute and return the color
        return -2.5 * np.log10(flux1 / flux2) - 5 * np.log10(pivot_1 / pivot_2)

    # Magnitude in Vega photometric system
    elif phot_sys == "Vega":
        # Read Vega spectrum if not provided
        if vega is None:
            vega = pd.read_csv(ska.PATH_VEGA)
            # vega.Wavelength /= 10000

        # Compute fluxes of Vega in each filter
        flux1_vega = filter1.compute_flux(vega)
        flux2_vega = filter2.compute_flux(vega)

        # Compute and return the color
        return -2.5 * (np.log10(flux1 / flux1_vega) - np.log10(flux2 / flux2_vega))

    # Magnitude in ST photometric system
    elif phot_sys == "ST":
        return -2.5 * np.log10(flux1 / flux2)


def reflectance_to_color(
    spectrum, filter1, filter2, phot_sys="AB", vega=None, sun=None
):
    """Computes filter_1-filter_2 color for a reflectance spectrum.

    Parameters
    ==========
    spectrum : pd.DataFrame
        Source reflectance spectrum. Columns must be
        Wavelength: in Angstrom
        Reflectance: arbitrary unit
    filter_1: ska.Filter
    filter_2: ska.Filter
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

    # Integration grid is built from the transmission curve
    lambda_min = np.min([filter1.wave.min(), filter2.wave.min()])
    lambda_max = np.max([filter1.wave.max(), filter2.wave.max()])

    # Wavelength range to integrate over
    lambda_int = np.arange(lambda_min, lambda_max, 0.0005)

    # Read spectrum othe Sun if not provided
    if type(sun) != pd.DataFrame:  # == None:
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
        interp_spectrum, filter1, filter2, phot_sys=phot_sys, vega=vega
    )


def solar_color(filter1, filter2, phot_sys="AB", vega=None):
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

    # Exrtract Solar Fluxes
    sun_1 = filter1.VOFilter.get_field_by_id("Fsun").value
    sun_2 = filter2.VOFilter.get_field_by_id("Fsun").value

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
        if "vega" not in locals():
            spec_vega = pd.read_csv(ska.PATH_VEGA)

        # Compute color of Vega
        vega_ST = compute_color(spec_vega, filter1, filter2, phot_sys="ST")
        return colorST - vega_ST

    # Solar color in ST photometric system
    else:
        pivot_1 = filter1.VOFilter.get_field_by_id("WavelengthPivot").value
        pivot_2 = filter2.VOFilter.get_field_by_id("WavelengthPivot").value
        return colorST - 5 * np.log10(pivot_1 / pivot_2)

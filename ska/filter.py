# from pathlib import Path

import os
from astropy.io.votable import parse
import numpy as np
import pandas as pd

import ska


class Filter:
    def __init__(self, id):
        """Load a filter.

        Parameters
        ----------
        id : str
            The filter unique ID (see SVO filter service)
        """

        if id not in ska.svo.FILTERS:
            raise ValueError(f"Unknown filter ID {id}. Choose from\n {ska.svo.FILTERS}")

        self.id = id
        # self.path = os.path.join(ska.PATH_CACHE , f"{self.id}.xml" )
        self.path = os.path.join(ska.PATH_CACHE, f"{self.id.replace('/','_')}.xml")

        # Download if not cached
        if not os.path.isfile(self.path):
            ska.svo.download_filter(self.id)

        # Parse filter response
        self.VOFilter = parse(self.path)
        data = pd.DataFrame(data=self.VOFilter.get_first_table().array.data)

        # Apply transforms
        data = data[data.Transmission >= 1e-5]
        data.Wavelength /= 10000  # to micron

        # Store in attributes
        self.wave = data.Wavelength
        self.trans = data.Transmission

    def compute_flux(self, spectrum):
        """Computes the flux of a spectrum in a given band.

        Parameters
        ----------
        spectrum : pd.DataFrame
            Wavelength: in Angstrom
            Flux: Flux density (erg/cm2/s/ang)

        Returns
        -------
        float
            The computed mean flux density
        """

        # Wavelength range to integrate over
        lambda_int = np.arange(self.wave.min(), self.wave.max(), 0.0005)

        # Detector type
        # Photon counter
        try:
            self.VOFilter.get_field_by_id("DetectorType")
            factor = lambda_int
        # Energy counter
        except:
            # TODO: Catch specific error here
            factor = lambda_int * 0 + 1

        # Interpolate over the transmission range
        interpol_transmission = np.interp(lambda_int, self.wave, self.trans)

        interpol_spectrum = np.interp(
            lambda_int, spectrum["Wavelength"], spectrum["Flux"]
        )

        # Compute the flux by integrating over wavelength.
        nom = np.trapz(
            interpol_spectrum * interpol_transmission * factor,
            lambda_int,
        )
        denom = np.trapz(interpol_transmission * factor, lambda_int)
        flux = nom / denom
        return flux

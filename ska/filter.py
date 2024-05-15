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

        # Test validity of filters
        FILTERS = ska.svo.load_filter_list()
        if id not in FILTERS:
            raise ValueError(f"Unknown filter ID {id}. Use ska filter to list available filters")

        self.id = id
        self.path = os.path.join(ska.PATH_CACHE, f"{self.id.replace('/','_')}.xml")

        # Download if not cached
        if not os.path.isfile(self.path):
            ska.svo.download_filter(self.id)

        # Parse filter response
        self.VOFilter = parse(self.path)
        data = pd.DataFrame(data=self.VOFilter.get_first_table().array.data)

        # Select non-zero transmission and convert to micron
        data = data[data.Transmission >= 1e-5]
        data.Wavelength /= 10000  # to micron

        # Store attributes
        self.wave = data.Wavelength
        self.trans = data.Transmission

    def display_summary(self):
        import rich
        rich.print(f"\n[bright_cyan]Filter ID :[/bright_cyan] {self.id}")

        try: 
            rich.print("[bright_cyan]Facility  :[/bright_cyan] {:s}".format( self.VOFilter.get_field_by_id("Facility").value))
        except:
            _ = 0
        
        try: 
            rich.print("[bright_cyan]Instrument:[/bright_cyan] {:s}".format( self.VOFilter.get_field_by_id("Instrument").value))
        except:
            _ = 0

        try: 
            rich.print("[bright_cyan]Band      :[/bright_cyan] {:s}".format( self.VOFilter.get_field_by_id("Band").value))
        except:
            _ = 0

        try: 
            rich.print("[bright_cyan]Central λ :[/bright_cyan] [green]{:.3f}[/green] [bright_cyan](micron)[/bright_cyan]".format( self.VOFilter.get_field_by_id("WavelengthCen").value/1e4))
        except:
            _ = 0

        try: 
            rich.print("[bright_cyan]FWHM      :[/bright_cyan] [green]{:.3f}[/green] [bright_cyan](micron)[/bright_cyan]".format( self.VOFilter.get_field_by_id("FWHM").value/1e4))
        except:
            _ = 0

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
        if self.VOFilter.get_field_by_id("DetectorType")==1:
            factor = lambda_int
        # Energy counter
        else:
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

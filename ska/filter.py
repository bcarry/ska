import os
import sys
from astropy.io.votable import parse
import numpy as np
import pandas as pd

import rich

import ska


class Filter:
    # --------------------------------------------------------------------------------
    def __init__(self, id):
        """Initiate a SKA filter class

        Parameters
        ----------
        id : str
            The filter unique ID (see `SVO Filter Service <http://svo2.cab.inta-csic.es/theory/fps`__)
        """

        # Test validity of filters
        FILTERS = ska.svo.load_filter_list()
        if id not in FILTERS:
            rich.print(
                f"[red]Unknown filter ID {id}[/red]. Use [green]ska filter[/green] command to list available filters"
            )
            sys.exit(1)
            # raise ValueError(f"Unknown filter ID {id}. Use [green]ska filter[/green] to list available filters")

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
        data.Wavelength /= 1e4  # to micron

        # Store attributes
        self.id = id
        self.wave = data.Wavelength
        self.trans = data.Transmission
        self.central_wavelength = (
            self.VOFilter.get_field_by_id("WavelengthCen").value / 1e4
        )
        self.FWHM = self.VOFilter.get_field_by_id("FWHM").value / 1e4
        self.pivot_wavelength = (
            self.VOFilter.get_field_by_id("WavelengthPivot").value / 1e4
        )

        try:
            self.facility = self.VOFilter.get_field_by_id("Facility").value
        except:
            self.facility = None

        try:
            self.instrument = self.VOFilter.get_field_by_id("Instrument").value
        except:
            self.instrument = None

        try:
            self.band = self.VOFilter.get_field_by_id("Band").value
        except:
            self.band = None

    # --------------------------------------------------------------------------------
    def display_summary(self):
        """
        Displays a summary of the filter's properties, including:

        - Filter ID
        - Facility (if available)
        - Instrument (if available)
        - Band (if available)
        - Central wavelength in microns
        - Full Width at Half Maximum (FWHM) in microns
        - Pivot wavelength in microns
        """

        import rich

        rich.print(f"\n[bright_cyan]Filter ID :[/bright_cyan] {self.id}")

        if self.facility is not None:
            rich.print(f"[bright_cyan]Facility  :[/bright_cyan] {self.facility:s}")

        if self.instrument is not None:
            rich.print(f"[bright_cyan]Instrument:[/bright_cyan] {self.instrument:s}")

        if self.band is not None:
            rich.print(f"[bright_cyan]Band      :[/bright_cyan] {self.band:s}")

        rich.print(
            f"[bright_cyan]Central λ :[/bright_cyan] [green]{self.central_wavelength:.3f}[/green] [bright_cyan](micron)[/bright_cyan]"
        )
        rich.print(
            f"[bright_cyan]FWHM      :[/bright_cyan] [green]{self.FWHM:.3f}[/green] [bright_cyan](micron)[/bright_cyan]"
        )
        rich.print(
            f"[bright_cyan]Pivot λ   :[/bright_cyan] [green]{self.pivot_wavelength:.3f}[/green] [bright_cyan](micron)[/bright_cyan]"
        )

    # --------------------------------------------------------------------------------
    def compute_flux(self, spectrum):
        """Computes the flux of a spectrum in a given band.

        Parameters
        ----------
        spectrum : ska.Spectrum
            The spectrum to compute the flux of

        Returns
        -------
        float
            The computed mean flux density
        """

        # Wavelength range to integrate over
        lambda_int = np.arange(self.wave.min(), self.wave.max(), 0.0005)

        # Detector type
        # Photon counter
        if self.VOFilter.get_field_by_id("DetectorType") == 1:
            factor = lambda_int
        # Energy counter
        else:
            factor = lambda_int * 0 + 1

        # Interpolate over the transmission range
        interpol_transmission = np.interp(lambda_int, self.wave, self.trans)

        interpol_spectrum = np.interp(lambda_int, spectrum.wave, spectrum.flux)

        # Compute the flux by integrating over wavelength.
        nom = np.trapz(
            interpol_spectrum * interpol_transmission * factor,
            lambda_int,
        )
        denom = np.trapz(interpol_transmission * factor, lambda_int)
        flux = nom / denom
        return flux

    # --------------------------------------------------------------------------------
    def solar_color(self, filter, phot_sys="Vega", vega=None):
        """Compute the color of the Sun between current and provided filter

        Parameters
        ==========
        filter: ska.Filter or str
            A SKA Filter object of a filter unique ID (see `SVO Filter Service <http://svo2.cab.inta-csic.es/theory/fps`__)

        phot_sys : str
            Photometric system in which to report the color (default=AB)

        vega : ska.Spectrum
            The spectrum of Vega (default=None)

        Returns
        =======
        float
            The solar color
        """
        if not isinstance(filter, ska.Filter):
            filter = ska.Filter(filter)

        # Extract Solar Fluxes
        sun_1 = self.VOFilter.get_field_by_id("Fsun").value
        sun_2 = filter.VOFilter.get_field_by_id("Fsun").value

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
            if not "vega" in locals():
                vega = ska.Spectrum(ska.PATH_VEGA)
            else:
                if not isinstance(vega, ska.Spectrum):
                    vega = ska.Spectrum(ska.PATH_VEGA)

            # Compute color of Vega
            vega_ST = vega.compute_color(self, filter, phot_sys="ST")
            return colorST - vega_ST

        # Solar color in ST photometric system
        else:
            pivot_1 = self.VOFilter.get_field_by_id("WavelengthPivot").value
            pivot_2 = filter.VOFilter.get_field_by_id("WavelengthPivot").value
            return colorST - 5 * np.log10(pivot_1 / pivot_2)

    # --------------------------------------------------------------------------------
    def plot_transmission(self, figure=None, black=False):
        """Create a plot of the transmission.

        Parameters
        ----------
        figure : str
            Path to save a figure

        black : boolean
            Set True to plot the transmission on a black background (default=False)

        Returns
        -------
        figure, axe
            Matplotlib figure and axe
        """

        # Define figure
        import matplotlib.pyplot as plt

        if black:
            plt.style.use("dark_background")
        else:
            plt.style.use("default")
        fig, ax = plt.subplots()

        # Plot transmission
        ax.plot(self.wave, self.trans, label=self.id)

        # Central wavelength and FWHM
        ax.axvline(
            self.central_wavelength,
            color="gray",
            linestyle="--",
            label=r"$\lambda_c$ = {:.2f} $\mu$m".format(self.central_wavelength),
        )
        ax.plot(
            self.central_wavelength + self.FWHM / 2 * np.array([-1, 1]),
            [self.trans.max() / 2, self.trans.max() / 2],
            linestyle="dotted",
            color="gray",
            label=r"FWHM = {:.2f} $\mu$m".format(self.FWHM),
        )

        # Add labels
        ax.set_xlabel("Wavelength (micron)")
        ax.set_ylabel("Transmission")
        ax.legend(loc="lower right")
        ax.set_ylim(bottom=0)
        fig.tight_layout()

        # Save to file
        if figure is not None:
            # fig.savefig(figure, dpi=180, facecolor="w", edgecolor="w")
            fig.savefig(figure, dpi=180)

        return fig, ax

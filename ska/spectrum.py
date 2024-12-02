import os
import sys

import numpy as np
import pandas as pd

import rich
import ska


class Spectrum:
    # --------------------------------------------------------------------------------
    def __init__(self, input=None):
        """Initiate a SKA spectrum class"""

        # Store attributes
        self.wave = None
        self.flux = None
        self.is_refl = False

        if "input" in locals():

            # Initialize from a str: file or a taxonomic class
            if isinstance(input, str):

                if os.path.isfile(input):
                    self.from_csv(input)
                else:
                    self.from_taxonomy(input)

            # Initialize from a pandas.DataFrame
            if isinstance(input, pd.DataFrame):
                self.from_dataframe(input)

            # Initialize from a numpy.ndarray
            if isinstance(input, np.ndarray):
                self.from_numpy(input)

            # Initialize from a temperature (simple float or int) -> Blackbody
            if isinstance(input, int) | isinstance(input, float):
                self.from_blackbody(input)

    # --------------------------------------------------------------------------------
    def copy(self):
        """Make a deepcopy of the SKA.Spectrum object."""

        from copy import deepcopy

        return deepcopy(self)

    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------
    # Spectrum from Input

    # --------------------------------------------------------------------------------
    def from_csv(self, file):
        """Create a SKA spectrum from a CSV file.

        Parameters
        ----------
        file : str
            Path to a CSV file containing the spectrum
        """

        if not os.path.isfile(file):
            rich.print(f"[red]Spectrum file {file} not found.[/red].")
            sys.exit(1)

        # Read spectrum
        try:
            spectrum = pd.read_csv(file)
        except:
            rich.print(f"[red]Cannot read spectrum file {file}.[/red].")
            sys.exit(1)

        self.from_dataframe(spectrum)

    # --------------------------------------------------------------------------------
    def from_numpy(self, arr, reflectance=False):
        """Create a SKA spectrum from a numpy array.

        Parameters
        ----------
        arr : np.ndarray
            A numpy array containing the spectrum. Columns must be
            Wavelength (in micron), and either Flux or Reflectance.

        reflectance : boolean
            Set True if the input is a reflectance spectrum (default=False)
        """

        if not isinstance(arr, np.ndarray):
            rich.print(f"[red]Input is not a numpy array.[/red]")
            sys.exit(1)

        if arr.shape[1] < 2:
            rich.print(f"[red]Input array has less than 2 columns.[/red]")
            sys.exit(1)

        # Store attributes
        order = np.argsort(arr[:, 0])
        self.wave = arr[order, 0]
        self.flux = arr[order, 1]
        self.is_refl = reflectance

    # --------------------------------------------------------------------------------
    def from_dataframe(self, df):
        """Create a SKA spectrum from a pandas DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            A DataFrame containing the spectrum. Columns must be
            Wavelength (in micron), and either Flux or Reflectance.
        """

        # Test Wavelength column
        check_wave = True
        if not "Wavelength" in df.columns:
            check_wave = False
            rich.print(f"[red]Column 'Wavelength' missing from input.[/red]")

        # Test Flux or Reflectance column
        check_flux = True
        check_refl = True
        if not "Flux" in df.columns:
            check_flux = False
        if not "Reflectance" in df.columns:
            check_refl = False

        if not (check_flux | check_refl):
            rich.print(f"[red]Column 'Flux' or 'Reflectance' missing from input.[/red]")
            sys.exit(1)

        if not (check_wave & (check_flux | check_refl)):
            sys.exit(1)

        # Store attributes
        order = np.argsort(df.Wavelength)
        self.wave = np.array(df.loc[order, "Wavelength"].values)
        if check_flux:
            self.flux = np.array(df.loc[order, "Flux"].values)
        if check_refl:
            self.flux = np.array(df.loc[order, "Reflectance"].values)
            self.is_refl = True

    # --------------------------------------------------------------------------------
    def from_taxonomy(self, type):
        """Create a SKA reflectance spectrum from an asteroid template spectrum (Mahlke+2022 taxonomy).

        Parameters
        ----------
        type : str
            The name of the spectral type (A, B, C, D, E, K, L... V, Z)
        """

        # Read template spectra of Mahlke+2022 taxonomy
        templates = pd.read_csv(ska.PATH_MAHLKE)

        # Select the requested type
        if type in templates.columns:
            cols = ["feature", type]
            df = templates[cols]
            df.columns = ["Wavelength", "Reflectance"]
            self.from_dataframe(df)
        else:
            rich.print(
                f"[red]Type[/red] [bright_cyan]{type}[/bright_cyan] [red]not found in Mahlke+2022 taxonomy.[/red]"
            )

    # --------------------------------------------------------------------------------
    def from_blackbody(self, T):
        """Create a SKA spectrum of a blackbody at temperature T.

        Parameters
        ----------
        T : float
            The temperature of the blackbody in Kelvin
        """

        from astropy.modeling.models import BlackBody
        from astropy import units as u

        # Blackbody function
        bb = BlackBody(
            temperature=float(T) * u.K,
            scale=1.0 * u.erg / (u.s * (0.1 * u.nm) * u.sr * u.cm**2),
        )
        wave = np.linspace(0.05, 5, num=1000) * u.micron
        flux = bb(wave)
        self.from_numpy(np.array([wave.value, flux.value]).T)

    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------
    # Color computation

    # --------------------------------------------------------------------------------
    def compute_color(self, id_filter_1, id_filter_2, phot_sys="Vega", vega=None):
        """Computes filter_1-filter_2 color of spectrum in the requested system.

        Parameters
        ==========
        id_filter_1: ska.Filter or str
            The first filter, a SKA Filter object of a filter unique ID (see SVO filter service)

        id_filter_2: ska.Filter
            The second filter, a SKA Filter object of a filter unique ID (see SVO filter service)

        phot_sys : str
            Photometric system in which to report the color (default=Vega)

        vega : ska.Spectrum
            The spectrum of Vega

        Returns
        =======
        float
            The requested color
        """

        # Load Filters if provided as strings
        if isinstance(id_filter_1, ska.Filter):
            filter_1 = id_filter_1
        else:
            filter_1 = ska.Filter(id_filter_1)

        if isinstance(id_filter_2, ska.Filter):
            filter_2 = id_filter_2
        else:
            filter_2 = ska.Filter(id_filter_2)

        # Compute fluxes in each filter
        flux1 = filter_1.compute_flux(self)
        flux2 = filter_2.compute_flux(self)

        # Magnitude in AB photometric system
        if phot_sys == "AB":
            # Get Pivot wavelength for both filters
            pivot_1 = filter_1.VOFilter.get_field_by_id("WavelengthPivot").value
            pivot_2 = filter_2.VOFilter.get_field_by_id("WavelengthPivot").value

            # Compute and return the color
            return -2.5 * np.log10(flux1 / flux2) - 5 * np.log10(pivot_1 / pivot_2)

        # Magnitude in Vega photometric system
        elif phot_sys == "Vega":
            # Read Vega spectrum if not provided
            if vega is None:
                vega = ska.Spectrum(ska.PATH_VEGA)

            # Compute fluxes of Vega in each filter
            flux1_vega = filter_1.compute_flux(vega)
            flux2_vega = filter_2.compute_flux(vega)

            # Compute and return the color
            return -2.5 * (np.log10(flux1 / flux1_vega) - np.log10(flux2 / flux2_vega))

        # Magnitude in ST photometric system
        elif phot_sys == "ST":
            return -2.5 * np.log10(flux1 / flux2)

    # --------------------------------------------------------------------------------
    def reflectance_to_flux(self, sun=None):
        """Convert reflectance to flux by multiply by Solar spectrum.

        Parameters
        ==========
        sun : ska.Spectrum
            Spectrum of the Sun

        Returns
        =======
        float
            A copy of the input Spectrum, in flux units
        """

        # Test if the input is a reflectance spectrum
        if not self.is_refl:
            rich.print(f"[red]Input spectrum is not a reflectance spectrum.[/red]")

        # Read spectrum of the Sun if not provided
        if not isinstance(sun, ska.Spectrum):
            sun = ska.Spectrum(ska.PATH_SUN)

        # Interpolate spectrum of the Sun
        interpol_spectrum = np.interp(self.wave, sun.wave, sun.flux)

        # Mulitply reflectance by Solar spectrum
        spectrum = self.copy()
        spectrum.flux = self.flux * interpol_spectrum
        spectrum.is_refl = False
        return spectrum

    # --------------------------------------------------------------------------------
    def reflectance_to_color(
        self, id_filter_1, id_filter_2, phot_sys="Vega", vega=None, sun=None
    ):
        """Computes filter_1-filter_2 color for a reflectance spectrum.

        Parameters
        ==========
        id_filter_1: ska.Filter or str
            The first filter, a SKA Filter object of a filter unique ID (see SVO filter service)

        id_filter_2: ska.Filter
            The second filter, a SKA Filter object of a filter unique ID (see SVO filter service)

        phot_sys : str
            Photometric system in which to report the color (default=Vega)

        vega : ska.Spectrum
            Spectrum of Vega

        sun : ska.Spectrum
            Spectrum of the Sun

        Returns
        =======
        float
            The requested color
        """
        # Load Filters if provided as strings
        if isinstance(id_filter_1, ska.Filter):
            filter_1 = id_filter_1
        else:
            filter_1 = ska.Filter(id_filter_1)

        if isinstance(id_filter_2, ska.Filter):
            filter_2 = id_filter_2
        else:
            filter_2 = ska.Filter(id_filter_2)

        # Integration grid is built from the transmission curve
        lambda_min = np.min([filter_1.wave.min(), filter_2.wave.min()])
        lambda_max = np.max([filter_1.wave.max(), filter_2.wave.max()])

        # Wavelength range to integrate over
        lambda_int = np.arange(lambda_min, lambda_max, 0.0005)

        # Read spectrum of the Sun if not provided
        if not isinstance(sun, ska.Spectrum):
            sun = ska.Spectrum(ska.PATH_SUN)

        # Interpolate spectrum of the Sun
        interpol_spectrum = np.interp(lambda_int, sun.wave, sun.flux)
        interp_sun = pd.DataFrame({"Wavelength": lambda_int, "Flux": interpol_spectrum})
        interp_sun = interp_sun.astype("float")

        # Interpolate reflectance spectrum
        interpol_spectrum = np.interp(lambda_int, self.wave, self.flux)
        interp_spectrum = ska.Spectrum(
            pd.DataFrame(
                {"Wavelength": lambda_int, "Flux": interpol_spectrum * interp_sun.Flux}
            )
        )

        # Compute color of the reflectance*Sun spectrum
        return interp_spectrum.compute_color(
            filter_1, filter_2, phot_sys=phot_sys, vega=vega
        )

    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    # Plot spectrum
    def plot(self, filters=None, figure=None, black=False):
        """Create a plot of the spectrum.

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
        ax.plot(self.wave, self.flux, label="Spectrum")

        # Add filters
        if filters is not None:
            if isinstance(filters, ska.Filter):
                filters = [filters]

            for f in filters:

                if isinstance(f, ska.Filter):
                    filt = f
                else:
                    filt = ska.Filter(f)
                    ax.plot(filt.wave, filt.trans, label=filt.id)

        # Add labels
        ax.set_xlabel("Wavelength (micron)")
        if self.is_refl:
            ax.set_ylabel("Reflectance")
        else:
            ax.set_ylabel("Flux")
        # ax.legend(loc="lower right")
        fig.tight_layout()

        # Save to file
        if figure is not None:
            fig.savefig(figure, dpi=180)

        return fig, ax

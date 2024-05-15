import os
import sys
import pandas as pd

import rich


class Spectrum:
    # --------------------------------------------------------------------------------
    def __init__(self, input=None):
        """
        """

        # Store attributes
        self.Wavelength = None
        self.Flux = None
        self.Reflectance = False

        if 'input' in locals():
            
            # Initialize from a file
            if isinstance(input, str):
                self.from_csv(input)

            # Initialize from a pandas.DataFrame
            if isinstance(input, pd.DataFrame):
                self.from_dataframe(input)


    # --------------------------------------------------------------------------------
    def from_csv(self, file):
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
    def from_dataframe(self, df):

        # Test Wavelength column
        check_wave = True
        if not 'Wavelength' in df.columns:
            check_wave = False
            rich.print(f"[red]Column 'Wavelength' missing from input.[/red]")
        
        # Test Flux or Reflectance column
        check_flux = True
        check_refl = True
        if not 'Flux' in df.columns:
            check_flux = False
        if not 'Reflectance' in df.columns:
            check_refl = False

        if not (check_flux | check_refl):
            rich.print(f"[red]Column 'Flux' or 'Reflectance' missing from input.[/red]")
            sys.exit(1)

        if not (check_wave & (check_flux | check_refl)):
            sys.exit(1)


        self.Wavelength = df.Wavelength.values
        if check_flux:
            self.Flux = df.Flux.values
        if check_refl:
            self.Flux = df.Reflectance.values
            self.Reflectance = True


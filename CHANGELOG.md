# 2.3 - 2026-08-03
- Allow the wavelength and flux (or reflectance) as distinct inputs for `Spectrum`
- Allow the `reflectance` keyword to `Spectrum` to instantiate either flux or reflectance from lists or numpy arrays
- Patched documentation for `solar_color` which is a method of `Filter`

# 2.2 - 2026-06-01
- Adapt to new data structure at SVO Filter Service

# 2.1 - 2026-02-12
- Loosen requirements on packages version
- Change deprecated `numpy.trapz`

# 1.2 - 2024-06-04
- Changed method "plot" into "plot-filter" in the CLI
- Added method "plot-spectrum" to Spectrum object 
- Added "docs" command to the CLI


# 1.1.1 - 2024-05-27
- Fix python requirement

# 1.1 - 2024-05-27
- Cache handles Sun and Vega
- Cache templates of asteroid taxonomy ([Mahlke+2022](https://ui.adsabs.harvard.edu/abs/2022A&A...665A..26M/abstract))
- Spectrum object from templates
  - Classes from [Mahlke+2022](https://ui.adsabs.harvard.edu/abs/2022A&A...665A..26M/abstract)
  - Blackbody from temperature

# 1.0 - 2024-05-23
- Initial release on PyPI

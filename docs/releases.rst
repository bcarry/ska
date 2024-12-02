.. _releases:

####################
``Release notes``
####################

.. raw:: html

    <style> .gray {color:#979eab} </style>

.. role:: gray


.. |br| raw:: html

     <br>

.. highlight:: python



|br|

Release 2.0 -- *2024-12-02*
============================================

- Major change in the Spectrum class. Attributes *Wavelength*, *Flux* are now **wave**, **refl** and *Reflectance* is **is_refl**. Shorter and lower-case attributes, as per `PEP8 <https://peps.python.org/pep-0008/#method-names-and-instance-variables>`_ recommendations. Thanks to `Max Mahlke <https://github.com/maxmahlke/>`_ for pointing this out.

- Methods to compute flux and colors from Spectrum now accept both ska.Filter and filter names (str) as input.

- API is now exposed in the documentation

Release 1.3 -- *2024-11-30*
============================================

The reference spectra for the Sun and Vega have changed. SKA now uses

- Sun:  The `2000 ASTM Standard Extraterrestrial Spectrum Reference E-490-00 <https://www.nrel.gov/grid/solar-resource/spectra-astm-e490.html>`_
- Vega: The `STSCi CALSPEC <https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec>`_ spectrum

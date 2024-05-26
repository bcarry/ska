.. _spectra:

#########
``Handling spectra``
#########

.. raw:: html

    <style> .gray {color:#979eab} </style>

.. role:: gray


.. |br| raw:: html

     <br>

.. highlight:: python


``ska`` relies ``Spectrum`` objects for all computations.
These objects can be easily created from a variety of sources, 
or from templates.

|br|

.. _spectra_local:

:octicon:`file;1em` Spectrum from local data
============================================

You can instantiate a ``Spectrum`` object from your own
spectrum (or reflectance spectrum). ``ska`` offers various
input to the ``Spectrum`` objects. 
In all cases, the ``Wavelength`` must be provided in :math:`\mu m`).



.. tab-set::

  .. tab-item:: CSV

    Create a ``Spectrum`` object directly from a local ``CSV`` file.
    The names of the columns defining the spectrum must be
    ``Wavelength`` and ``Flux`` (or ``Reflectance``).

      .. code-block:: python

        >>> from ska import Spectrum         # Class for spectra
        >>> my_spect = Spectrum("sun.csv")   # Read and create Spectrum object

  .. tab-item:: numpy array

    Create a ``Spectrum`` object from a simple 2d
    `numpy <https://numpy.org/>`_ array:
    the first column contains the wavelength and
    the second the flux (or the reflectance).

     .. code-block:: python

       >>> from ska import Spectrum         # Class for spectra
       >>> import numpy as np               # Import numpy
       >>> my_array = np.genfromtxt( 'sun.csv', delimiter=',', skip_header=1 )
       >>> my_array
       array([[1.19500000e-01, 8.86150000e-03],
       [1.20500000e-01, 6.94500000e-02],
       [1.21500000e-01, 6.08100000e-01],
       ...,
       [2.99870918e+02, 2.94500000e-08],
       [2.99901507e+02, 2.94230000e-08],
       [2.99932098e+02, 2.93950000e-08]])

       >>> my_spect = Spectrum( my_array )

  .. tab-item:: pandas DataFrame

    Create a ``Spectrum`` object from a `pandas <https://pandas.pydata.org/>`_ ``DataFrame``.
    ``ska`` will use the columns named
    ``Wavelength`` and ``Flux`` (or ``Reflectance``).

     .. code-block:: python

       >>> from ska import Spectrum         # Class for spectra
       >>> import pandas as pd              # Import pandas
       >>> df = pd.read_csv( 'sun.csv')     # Store a spectrum in a DataFrame
       >>> df.head(5)
          Wavelength   Flux
        0 0.119500     8.861500e-03
        1 0.120500     6.945000e-02
        2 0.121500     6.081000e-01
        3 0.122500     1.437000e-01
        4 0.123500     6.269500e-03

       >>> my_spect = Spectrum( df )



|br|



:octicon:`database;1em` Spectrum from templates
============================================

``ska`` offers the possibility to instantiate a ``Spectrum`` object
from a library of templates.

.. tab-set::

  .. tab-item:: Mahlke+2022 Taxonomy

    Create a ``Spectrum`` object from any of the taxonomic classes
    of `Mahlke et al. (2022) <https://ui.adsabs.harvard.edu/abs/2022A&A...665A..26M/abstract>`_.


      .. code-block:: python

        >>> from ska import Spectrum         # Class for spectra
        >>> A_type = Spectrum("A")           # Simply provide the class name
        >>> S_type = Spectrum("S")           # Simply provide the class name

  .. tab-item:: Blackbody

    Create a ``Spectrum`` object from a blackbody at the requested temperature (in K). 

      .. code-block:: python

        >>> from ska import Spectrum         # Class for spectra
        >>> my_BB = Spectrum(5778)           # Simply provide the temperature

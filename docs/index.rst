#########
``ska: a Spectral Kit for Asteroids``
#########

.. raw:: html

    <style> .gray {color:#979eab} </style>

.. role:: gray

A ``python`` client to explore the filters in 
`SVO Filter Service
<http://svo2.cab.inta-csic.es/theory/fps/>`_ and compute colors 
from spectra.


.. |br| raw:: html

     <br>

.. highlight:: python

|br|

:octicon:`archive;1em` **Easy handling of filters with SVO**


.. tab-set::

  .. tab-item:: Command Line

      .. code-block:: bash

          $ ska filter Paranal/VISTA.Ks
          
          Filter ID : Paranal/VISTA.Ks
          Facility  : Paranal
          Instrument: VIRCAM
          Band      : Ks
          Central λ : 2.148 (micron)
          FWHM      : 0.306 (micron)


  .. tab-item :: python

     .. code-block:: python

       >>> from ska import Filter                # class handling filters
       >>> VISTA_Ks = Filter("Paranal/VISTA.Ks") # retrieve VISTA Ks filter
       >>> VISTA_Ks.facility                     # get the parameter values via the dot notation
       'Paranal'
       >>> VISTA_Ks.instrument
       'VIRCAM'
       >>> VISTA_Ks.central_wavelength
       1.6458237
       >>> VISTA_Ks.FWHM
       0.289423

|br|

:octicon:`sun;1em` **Simple access to the colors of the Sun**

.. tab-set::

  .. tab-item:: Command Line

      .. code-block:: bash

          $ ska solarcolor Generic/Johnson.V Paranal/VISTA.Ks
          1.53

          $ ska solarcolor Generic/Johnson.V Paranal/VISTA.Ks --phot_sys AB
          -0.31

  .. tab-item :: python

     .. code-block:: python

       >>> from ska import Filter                # class handling filters
       >>> filt_V = Filter("Generic/Johnson.V")  # retrieve Johnson V filter
       >>> filt_Ks = Filter("Paranal/VISTA.Ks")  # retrieve VISTA Ks filter

       >>> filt_V.solar_color(filt_Ks)
       1.53020564
       
|br|

:octicon:`graph;1em` **Plotting utilities**

|br|


:octicon:`git-branch;1em` **Handle both flux and reflectance**



.. toctree::
   :maxdepth: 2
   :caption: Contents
   :hidden:

   Home<self>
   Getting Started<getting_started>
   Available Data<ssodnet>
   Basic Usage<cli>
   credit
   appendix
   glossary


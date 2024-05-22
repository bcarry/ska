.. _colors:

#########
``Computing colors``
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

:: _color_sun:
  
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
      
      >>> filt_V.solar_color(filt_Ks, phot_sys='AB')
      -0.3111391
       
|br|


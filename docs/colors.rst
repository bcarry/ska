.. _colors:

#########
``Computing colors``
#########

.. raw:: html

    <style> .gray {color:#979eab} </style>

.. role:: gray

.. |br| raw:: html

     <br>

.. highlight:: python


``ska`` offers simple methods to compute the color of a spectrum or
a reflectance spectrum between two filters, in the three photometric
systems (Vega, AB, ST).


|br|

.. _color_sun: 

:octicon:`sun;1em` Computing the colors of the Sun
==================================================

``ska`` provides a simple way to access to the colors of the Sun, directly from the
solar flux computed by the `SVO Filter Service <http://svo2.cab.inta-csic.es/theory/fps/>`_.
As ``ska`` also includes a spectrum of the Sun from CalSpec [#f1]_, you can also compute 
its colors from the spectrum itself (located at ``ska.PATH_SUN``).


.. tab-set::

  .. tab-item:: Command Line

    The ``$ ska solarcolor [filter1] [filter2]`` command will compute the color of the Sun
    between ``filter1`` and ``filter2``. The default
    :term:`photometric system<Photometric system>` is
    :term:`Vega<Vega>`.

    .. code-block:: bash

      $ ska solarcolor Generic/Johnson.V Paranal/VISTA.Ks
      1.53
         
  .. tab-item :: python

    The method ``solar_color`` computes the color of the Sun between the current
    filter and another, specified by its name or by a ``Filter`` object.

    .. code-block:: python

      >>> from ska import Filter                 # Class for filters
      >>> V = Filter("Generic/Johnson.V")        # Retrieve Johnson V
      >>> Ks = Filter("2MASS/2MASS.Ks")          # Retrieve 2MASS Ks
      >>> V.solar_color(Ks)
      1.54

      # or
      >>> V.solar_color("2MASS/2MASS.Ks")
      1.54      

|br|

.. _color_flux: 

:octicon:`telescope;1em` Computing colors from spectra
======================================================


.. _color_refl: 

:octicon:`rss;1em` Computing colors from reflectance
====================================================


.. _color_phot_sys: 

:octicon:`repo-forked;1em` Switching between photometric systems
================================================================



.. [#f1] `https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec <https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec>`_
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
systems (Vega, AB, ST). See :ref:`how_it_works` for more details.


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

``ska`` can compute the color of any spectrum between two filters.

.. tab-set::

  .. tab-item:: Command Line

    The ``$ ska color [file] [filter1] [filter2]`` command will compute the color of
    the provided spectrum (in ``file``)
    between ``filter1`` and ``filter2``.
    The spectrum must be provided as a CSV file with two columns: ``Wavelength`` and ``Flux``.
    The default
    :term:`photometric system<Photometric system>` is
    :term:`Vega<Vega>`.
    
    .. code-block:: bash

      $ ska color data/hst_sun.csv Generic/Johnson.V 2MASS/2MASS.J
      1.15
         
  .. tab-item :: python

    The method ``compute_color`` computes the color of the ``Spectrum`` object
    between two filters, specified by their names or provided as ``Filter`` objects.

    .. code-block:: python

      >>> from ska import Spectrum             # Class for spectra
      >>> sun = Spectrum("sun.csv")            # Load a spectrum
      >>> sun.compute_color("Generic/Johnson.V", "2MASS/2MASS.J")
      1.15

      # or
      >>> from ska import Filter               # Class for filters
      >>> V = Filter("Generic/Johnson.V")      # Retrieve Johnson V filter
      >>> J = Filter("2MASS/2MASS.J")          # Retrieve 2MASS J filter
      >>> sun.solar_color(V, J)
      1.15

|br|

.. _color_refl: 

:octicon:`rss;1em` Computing colors from reflectance
====================================================

``ska`` can compute the color of any reflectance spectrum between two filters, 
as for spectra, but will automatically convert the reflectance
into flux using the spectrum of the Sun.

**NB** To compute the color between two filters, in the reflectance space,
simply use the color computation above.

.. tab-set::

  .. tab-item:: Command Line

    The ``$ ska color [file] [filter1] [filter2] --reflectance``
    command will compute the color of
    the provided reflectance spectrum (in ``file``)
    between ``filter1`` and ``filter2``.
    The spectrum must be provided as a CSV file with two columns:
    ``Wavelength`` and ``Reflectance``.
    The default
    :term:`photometric system<Photometric system>` is
    :term:`Vega<Vega>`.
    
    .. code-block:: bash

      $ ska color vesta.csv Generic/Johnson.V Paranal/VISTA.Ks --reflectance
      1.59
         
  .. tab-item :: python

    The method ``reflectance_to_color`` computes the color of the ``Spectrum`` object
    between two filters, specified by their names or provided as ``Filter`` objects.

    .. code-block:: python

      >>> from ska import Spectrum             # Class for spectra
      >>> vesta = Spectrum("vesta.csv")        # Load a reference spectrum
      >>> vesta.reflectance_to_color("Generic/Johnson.V", "2MASS/2MASS.J")
      1.15

      # or
      >>> from ska import Filter               # Class for filters
      >>> V = Filter("Generic/Johnson.V")      # Retrieve Johnson V filter
      >>> J = Filter("2MASS/2MASS.J")          # Retrieve 2MASS J filter
      >>> vesta.reflectance_to_color(V, J)
      1.15

|br|

.. _color_phot_sys: 

:octicon:`repo-forked;1em` Switching between photometric systems
================================================================

Colors are intrinscally linked to a photometric system, that defines
the reference spectral energy distribution
(see :ref:`how_it_works`)
``ska`` offers an easy possibility to switch between the three photometric systems:
Vega, AB and ST.

.. tab-set::

  .. tab-item:: Command Line

    Simple uses the ``--phot_sys [Vega|AB|ST]`` option to switch photometric
    system when computing colors.
    
    .. code-block:: bash

      $ ska color sun.csv Generic/Johnson.V 2MASS/2MASS.J --phot_sys Vega
      1.15    # This is the default. No need to specify Vega

      $ ska color sun.csv Generic/Johnson.V 2MASS/2MASS.J --phot_sys AB
      0.24

      $ ska color sun.csv Generic/Johnson.V 2MASS/2MASS.J --phot_sys ST
      -1.51
         
  .. tab-item :: python

    The methods ``compute_color`` and ``reflectance_to_color`` accept
    a ``phot_sys`` keyword. Simply set it to ``Vega`` (default), 
    ``AB`` or ``ST``.

    .. code-block:: python

      >>> from ska import Spectrum             # Class for spectra
      >>> sun = Spectrum("sun.csv")            # Load a spectrum
      
      >>> sun.compute_color("Generic/Johnson.V", "2MASS/2MASS.J", phot_sys="Vega")
      1.15       # This is the default behavior

      >>> sun.compute_color("Generic/Johnson.V", "2MASS/2MASS.J", phot_sys="AB")
      0.24

      >>> sun.compute_color("Generic/Johnson.V", "2MASS/2MASS.J", phot_sys="ST")
      -1.51

|br|


.. [#f1] `https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec <https://www.stsci.edu/hst/instrumentation/reference-data-for-calibration-and-tools/astronomical-catalogs/calspec>`_
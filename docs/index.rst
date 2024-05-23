#####################################
``ska: a Spectral Kit for Asteroids``
#####################################

.. raw:: html

    <style> .gray {color:#979eab} </style>

.. role:: gray

A ``python`` client to explore the filters in 
`SVO Filter Service <http://svo2.cab.inta-csic.es/theory/fps/>`_ 
(`Rodrigo & Solano, 2020 <https://ui.adsabs.harvard.edu/abs/2020sea..confE.182R/abstract>`_) and compute colors 
from spectra.


.. |br| raw:: html

     <br>

.. highlight:: python

|br|

:octicon:`archive;1em` **Easy handling of filters**


.. grid:: 3

    .. grid-item-card::
      :link: filter_info
      :link-type: ref

      What is the wavelength of ``VISTA.Ks`` filter?
      What is its FWHM?


    .. grid-item-card::
      :link: filter_plot
      :link-type: ref

      Show me the transmission curve of ``Gaia/RP``

    .. grid-item-card::
      :link: filter_search
      :link-type: ref

      How do I find the identifier of a filter?


:octicon:`sun;1em` **Easy computation of colors**

.. grid:: 3

    .. grid-item-card::
      :link: color_sun
      :link-type: ref

      What is the color of the Sun?

    .. grid-item-card::
      :link: color_flux
      :link-type: ref

      What is the V-J of my spectrum?

    .. grid-item-card::
      :link: color_phot_sys
      :link-type: ref

      How to specify the photometric system: AB, Vega, ST?


|br|



.. toctree::
  :maxdepth: 2
  :caption: Contents

  Home<self>
  Getting Started<getting_started>
  Dealing with filters<filters>
  Computing colors<colors>
  How does it work?<how_it_works>
  glossary

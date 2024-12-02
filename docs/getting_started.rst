
###################
``Getting started``
###################

.. raw:: html

    <style> .gray {color:#979eab} </style>

.. role:: gray


.. |br| raw:: html

     <br>

.. highlight:: python

:octicon:`rocket;1em` Install ``ska``
=====================================


``ska`` is available on the `python package index <https://pypi.org>`_ as *space-ska*:

.. code-block:: bash

   $ pip install space-ska

The minimum version requirement for ``python`` is ``3.8``. After
installation, you have the ``ska`` executable available system-wide.
In addition, you can now import the ``ska`` ``python`` package.


.. tab-set::

  .. tab-item:: Command Line

      .. code-block:: bash

          $ ska

          Usage: ska [OPTIONS] COMMAND [ARGS]...

            CLI for Spectral-Kit for Asteroids.

          Options:
            --version  Show the version and exit.
            --help     Show this message and exit.

          Commands:
            color       Compute the color between two filters
            docs        Open the ska documentation in browser.
            filter      Display the basic properties of the filter
            id          Fuzzy-search SVO filter index.
            plot-filter    Display a simple figure of the transmission of the filter
            plot-spectrum  Display a simple figure of the spectrum
            solarcolor  Compute the color of the Sun between two filters
            status      Echo the status of the cached filters.


  .. tab-item :: python


     .. code-block:: python

         >>> import ska

`ska` is still in its early days, and `new versions
<https://github.com/bcarry/ska/blob/main/CHANGELOG.md>`_ come out
frequently. 


:octicon:`server;1em` Manage ``ska`` cache
==========================================

``ska`` relies extensively on the 
`SVO Filter Profile Service <http://svo2.cab.inta-csic.es/svo/theory/fps3/index.php>`_
for all the aspects related to filters (both the list and their properties).
``ska`` also needs a reference spectrum of Vega
(for :term:`Vega<Vega>` :term:`photometric system<Photometric system>`, see :ref:`how_it_works`), 
and of the Sun (for solar colors), as well as templates
for asteroids taxonomic classes.

To speed up ``ska`` those files are cached locally. It is recommended to
update the cache regularly, by running the following command:

.. code-block:: bash

    $ ska status

    Contents of /home/bcarry/.cache/ska:

            10 filters
            2 spectra
            1 spectral template files

    Update or clear the cached filters and filter list?
    [0] No [1] Clear cache [2] Update data  (0): 



.. raw:: html

    <style> .blue {color:blue;} </style>

.. role:: blue

.. raw:: html

    <style> .coral {color:LightCoral;} </style>

.. role:: coral



.. |br| raw:: html

     <br>

###############
Getting started
###############

Install ``ska``
=================


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
             color   Compute the color between two filters
             filter  Fuzzy-search SVO filter index.

  .. tab-item :: python


     .. code-block:: python

         >>> import ska

`ska` is still in its early days, and `new versions
<https://github.com/maxmahlke/rocks/blob/master/CHANGELOG.md>`_ come out
frequently. 

.. _install_fzf:

Optional: Interactive Search
============================

``ska`` provides an interactive search dialogue using the `fzf
<https://github.com/junegunn/fzf/>`_  fuzzy-finder which is triggered if
commands that expect an `filter identifier` as argument are
called without argument.

The ``fzf`` tool needs to be installed separately from ``ska``. On most
systems (Linux + MacOS), this requires a single command on the terminal, as
explained in the `fzf documentation
<https://github.com/junegunn/fzf/#installation>`_

.. raw:: html

    <style> .blue {color:blue;} </style>

.. role:: blue

.. raw:: html

    <style> .coral {color:LightCoral;} </style>

.. role:: coral


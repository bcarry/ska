.. _how_it_works:

####################
``How does it work``
####################

.. raw:: html

    <style> .gray {color:#979eab} </style>

.. role:: gray


.. |br| raw:: html

     <br>

.. highlight:: python



|br|

.. _work_principle: 

:octicon:`light-bulb;1em` Quantity of energy
============================================

The total number of photons N,
per unit time per unit area, received through a filter F
(of transmission :math:`T_\lambda`)
from a source of a flux density :math:`S_\lambda` is:

.. math ::
    N &=& \int_\lambda\,\frac{S_\lambda}{E_\nu}\,T_\lambda\,d\lambda\\
    &=& \frac{1}{hc} \int_\lambda\,S_\lambda\,T_\lambda\,\lambda\,d\lambda


Hence, if one consider :math:`T_\lambda\,\lambda` as a distribution, the
mean flux density :math:`\overline{f_\lambda}` received through the filter F is:

.. math ::
    \overline{f_\lambda} = \frac{\int_\lambda\,S_\lambda\,T_\lambda\,\lambda\,d\lambda}
                        {\int_\lambda\,T_\lambda\,\lambda\,d\lambda}

and the magnitude (with the Pogson definition) is computed as:

.. math ::
    m(F) = -2.5\log\left(\overline{f_\lambda}\right) + \textrm{ZP}\left(\overline{f_\lambda}\right)

where :term:`ZP<ZP>` is an offset, called the zero point of the :term:`photometric system<Photometric system>`. 
There are several photometric systems, differing by their definition of the zero point.

.. _work_Vega: 

:octicon:`north-star;1em` The Vega system
======================================

The historical system, most spread, is defined such as the
:math:`\alpha` Lyr star (Vega, which gives its name to the photometric
system) has a magnitude 0 in all filters.
In other words:

.. math ::
    \textrm{ZP}\left(\overline{f_\lambda}\right) = -2.5\log\left(\overline{f_\lambda(Vega)}\right)

which can be directly written

.. math ::
    m_{\textrm{Vega}}(F) = -2.5\log\left(\frac{\overline{f_\lambda}}{\overline{f_\lambda(\textrm{Vega})}}\right)

Vega was chosen because of its visibility from the northern
hemisphere, its high flux, and the low amount of spectral lines in
its visible spectrum..
This photometric systems does however not correspond to any
remarkable spectral energy distribution. This led to the definition
of two other systems: ST et AB.

.. _work_ST: 

:octicon:`horizontal-rule;1em` The ST system
====================================

The ST system was defined such as a source with a constant
flux
:math:`f_\lambda (\textrm{erg}\cdot\textrm{cm}^{2}\cdot\textrm{s}^{-1}\cdot\overset{\lower.5em\circ}{\mathrm{A}}^{-1})`
against wavelength :math:`\lambda` has a constant magnitude regardless of
the filter. The zero point is chosen to provide a magnitude in V
close to the magnitude in the Vega system (i.e., close to 0):

.. math ::
    m_{\textrm{ST}}(F) = -2.5\log\left(\overline{f_\lambda}\right) - 21.1


.. _work_AB: 

:octicon:`pulse;1em` The AB system
====================================

The AB system was defined such as a source with constant flux
:math:`f_\nu (\textrm{erg}\cdot\textrm{cm}^{2}\cdot\textrm{s}^{-1}\cdot\textrm{Hz}^{-1})`
against frequency :math:`\nu` has a constant magnitude
regardless of the filter. Here again, the ZP is chosen to provide a
magnitude in V close to that of Vega system:

.. math ::
    m_{\textrm{AB}}(F) = -2.5\log\left(\overline{f_\nu}\right) - 48.6

where :math:`\overline{f_\nu}` is defined 
`Koornneef et al. (1986) <https://ui.adsabs.harvard.edu/abs/1986HiA.....7..833K/abstract>`_ as


.. math ::
    \overline{f_\nu} =  \frac{\int_\nu\,S_\nu\,T_\nu\,d\nu\,/\,\nu}
                          {\int_\nu\,T_\nu\,d\nu\,/\,\nu}

It is often useful to consider the :term:`pivot wavelength<Pivot wavelength>`
:math:`\lambda_p` to easily convert :math:`\overline{f_\nu}` into
:math:`\overline{f_\lambda}` (knowing :math:`\lambda\nu = c` the speed of light):

.. math ::
    \lambda_p^2 &=& \frac{\int_\lambda T_\lambda\,\lambda\,d\lambda}
                         {\int_\lambda T_\lambda\,d\lambda /\lambda}  \\
    \overline{f_\nu} &=& \frac{\lambda_p^2}{c} \overline{f_\lambda}

Hence, the magnitude in the AB system can also be written as:

.. math ::
    m_{\textrm{AB}}(F) = -2.5\log\left(\overline{f_\lambda}\right) -2.5\log\left(\frac{\lambda_p^2}{c}\right) - 48.6


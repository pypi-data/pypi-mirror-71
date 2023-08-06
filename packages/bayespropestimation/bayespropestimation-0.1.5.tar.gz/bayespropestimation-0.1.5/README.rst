==================================
Bayesian estimation of proportions
==================================

.. image:: https://img.shields.io/pypi/v/bayespropestimation.svg
        :target: https://pypi.python.org/pypi/bayespropestimation


Simple class and methods for the Bayesian estimation and comparison of proportions.

* Free software: MIT license

Features
--------

* Estimates the posterior distribution of the mean parameter for two binomial samples, A and B.
* Estimates of the posterior distribution of difference in mean parameters for two binomial samples, A and B.
* Provides summary statistics and visualisations for the estimated parameters.
* The prior distribution, sample count, random seed, credible intervals and field names can all be customised.


============
Installation
============

Stable release
--------------

To install Bayesian estimation of proportions, run this command in your terminal:

.. code-block:: console

    $ pip install bayespropestimation

This is the preferred method to install the module, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

From sources
------------

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/oli-chipperfield/bayespropestimation

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/oli-chipperfield/bayespropestimation/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install

.. _Github repo: https://github.com/oli-chipperfield/bayespropestimation
.. _tarball: https://github.com/oli-chipperfield/bayespropestimation/tarball/master

===========
Methodology
===========

watch this space

=====
Usage
=====

To use Bayesian estimation of proportions in a project

.. code-block:: python

    import bayespropestimation

Simple example
--------------

To carry out a simple estimation of the posterior density of two samples and an estimate of the difference, using an uninformative prior.  Import the `BayesProportionsEstimation` class.

.. code-block:: python

    from bayespropestimation.bayespropestimation import BayesProportionsEstimation

Define data from samples A and B as two lists of format `[successes, trials]` and initialise the `BayesProportionsEstimation` class.

.. code-block:: python

    a = [10, 50]
    b = [20, 50]
    ExampleBayes = BayesProportionsEstimation(a, b)

Posterior densities are estimated when the class is intialised. There are three methods for accessing the draws from simulations of the posterior densities.

.. code-block:: python

    ExampleBayes.get_posteriors()
    # Returns tuple of samples from the posterior distributions for parameters

.. code-block:: python

    ExampleBayes.quantile_summary()
    # Returns dataframe of quantiles and mean of the posterior densities of samples for parameters

.. image:: https://github.com/oli-chipperfield/bayespropestimation/blob/improve-readme/images/example_quantile.png

.. code-block:: python

    ExampleBayes.kde_plot()
    # Returns KDE plot of samples from the posterior densities of the parameters
    # Shading denote the 95% (default) credible intervals

.. image:: https://github.com/oli-chipperfield/bayespropestimation/blob/improve-readme/images/example_kde.png

To see how to use non-default parameters, refer to the doc-strings in the `source <https://github.com/oli-chipperfield/bayespropestimation/blob/improve-readme/bayespropestimation/bayespropestimation.py>`_.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

.. highlight:: shell

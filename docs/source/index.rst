.. _amplapi:



AMPL Python API
===============

``amplpy`` is an interface that allows developers to access the features of `AMPL <https://ampl.com>`_ from within Python.
For a quick introduction to AMPL see `Quick Introduction to AMPL <https://dev.ampl.com/ampl/introduction.html>`_.

In the same way that AMPL's syntax matches naturally the mathematical description of the model,
the input and output data matches naturally Python lists, sets, dictionaries, ``pandas`` and ``numpy`` objects.

All model generation and solver interaction is handled directly by AMPL, which leads to
great stability and speed; the library just acts as an intermediary, and the added overhead (in terms of memory and
CPU usage) depends mostly on how much data is sent and read back from AMPL, the size of the expanded model as such is irrelevant.
With ``amplpy`` you can model and solve large scale optimization problems in Python with the performance of heavily optimized C code
without losing model readability.

.. grid:: 1 1 2 2
    :gutter: 0
    :margin: 0
    :padding: 0

    .. grid-item-card::
        :margin: 0
        :padding: 0

        Quick Start using Pandas dataframes
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        Data can be loaded in various forms, one of which is ``pandas.DataFrame`` objects.

        .. image:: https://colab.research.google.com/assets/colab-badge.svg
            :target: https://colab.research.google.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/pandasdiet.ipynb
            :alt: Open In Colab

        .. image:: https://kaggle.com/static/images/open-in-kaggle.svg
            :target: https://kaggle.com/kernels/welcome?src=https://github.com/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/pandasdiet.ipynb
            :alt: Kaggle

        .. image:: https://assets.paperspace.io/img/gradient-badge.svg
            :target: https://console.paperspace.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/pandasdiet.ipynb
            :alt: Gradient

        .. image:: https://studiolab.sagemaker.aws/studiolab.svg
            :target: https://studiolab.sagemaker.aws/import/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/pandasdiet.ipynb
            :alt: Open In SageMaker Studio Lab

    .. grid-item-card::
        :margin: 0
        :padding: 0

        Quick Start using lists and dictionaries
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        Data can be loaded in various forms, including Python lists and dictionaries.

        .. image:: https://colab.research.google.com/assets/colab-badge.svg
            :target: https://colab.research.google.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/nativediet.ipynb
            :alt: Open In Colab

        .. image:: https://kaggle.com/static/images/open-in-kaggle.svg
            :target: https://kaggle.com/kernels/welcome?src=https://github.com/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/nativediet.ipynb
            :alt: Kaggle

        .. image:: https://assets.paperspace.io/img/gradient-badge.svg
            :target: https://console.paperspace.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/nativediet.ipynb
            :alt: Gradient

        .. image:: https://studiolab.sagemaker.aws/studiolab.svg
            :target: https://studiolab.sagemaker.aws/import/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/nativediet.ipynb
            :alt: Open In SageMaker Studio Lab

More notebooks with examples available on the `AMPL Model Colaboratory <https://colab.ampl.com/>`_.


Contents
--------

.. toctree::
   :maxdepth: 2

   intro
   getting-started
   quick-start
   class-structure
   reference
   examples

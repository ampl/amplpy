.. lblGettingStarted:

Getting started
===============

Installation
------------

The AMPL API can function as an add-on to any existing AMPL installation.
If you do not yet have an AMPL installation on the computer where you will
be working with the API, see our
`demo page <http://ampl.com/try-ampl/download-a-free-demo/>`_ or
`trial page <http://ampl.com/try-ampl/request-a-full-trial/>`_ to download a
working version that can be installed quickly.

In order to install the Python API you just need to run

.. code-block:: bash

    pip install amplpy

Or alternatively:

.. code-block:: bash

    python -m pip install amplpy

Note: For Windows, Linux, and macOS, the ``amplpy`` package comes with 26 binary
wheels for Python 2.7, 3.3, 3.4, 3.5, and 3.6. Please make sure that you are
using the latest version of ``pip`` before installing ``amplpy`` (upgrade using
``pip install pip --upgrade`` or ``python -m pip install pip --upgrade``).
If a binary wheel for your platform is not available,
a C++ compiler and python development libraries will be required.

Initial test
------------

To begin, open a command/terminal window and clone our `GitHub repository <https://github.com/ampl/amplpy>`_:

.. code-block:: bash

    git clone git@github.com:ampl/amplpy.git

To complete an initial test, run ``firstexample`` with

.. code-block:: bash

   python amplpy/examples/firstexample.py <solver>

where optionally ``<solver>`` is the name of a solver that has been installed with AMPL.
(If a solver is not specified, AMPL's default choice will be used.) This will solve
several small diet problems and then display the optimal amounts of the foods
from the last solution. Alternatively, you can download the examples directly from
`<https://github.com/ampl/amplpy/tree/master/examples>`_.

Development
-----------

Import the ``amplpy`` modude with

.. code-block:: python

   import amplpy

Together with your existing AMPL implementation, this will provide the full
object library and access to all AMPL functions.

Deployment
----------

To deploy AMPL API applications to users who do not have their own AMPL installations,
include with your application the AMPL executable (``ampl`` or ``ampl.exe``), and the ``amplpy`` package.

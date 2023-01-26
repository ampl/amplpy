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

    python -m pip install amplpy

Note: For Windows, Linux, and macOS, the ``amplpy`` package comes with binary
wheels. Please make sure that you are
using the latest version of ``pip`` before installing ``amplpy`` (upgrade using
``pip install pip --upgrade`` or ``python -m pip install pip --upgrade``).
If a binary wheel for your platform is not available,
a C++ compiler and python development libraries will be required.

amplpy.modules
--------------
.. _amplpyModules:

`AMPL and all solvers are now available as python packages <https://dev.ampl.com/ampl/python/modules.html>`_ for Windows, Linux, and macOS. For instance, to install AMPL with HiGHS and Gurobi,
you just need the following:

.. code-block:: bash

   $ python -m pip install amplpy --upgrade
   $ python -m amplpy.modules install highs gurobi # install HiGHS and Gurobi
   $ python -m amplpy.modules run amplkey activate --uuid <license-uuid> # activate your license
   $ python -m amplpy.modules run ampl -vvq # confirm that the license is active
   $ python
   >>> from amplpy import AMPL, modules
   >>> modules.load() # load all modules
   >>> ampl = AMPL()

For Apple M1/M2, please make sure your have Rosetta 2 installed since not all modules are available for M1. You can install it with: ``softwareupdate --install-rosetta``.

Full documentation for ``amplpy.modules``: https://dev.ampl.com/ampl/python/modules.html

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

Otherwise, the error message "AMPL could not be started" will be shown.
If the AMPL installation directory is not in the system search path,
you can add it using :func:`~amplpy.add_to_path` as follows:

.. code-block:: python

    from amplpy import AMPL, add_to_path
    add_to_path(r"full path to the AMPL installation directory")
    ampl = AMPL()

Or, if you are using :ref:`amplpy.modules <amplpyModules>`, do the following:

.. code-block:: python

    from amplpy import AMPL, modules
    modules.load()
    ampl = AMPL()

You can also specify an :class:`amplpy.Environment`

.. code-block:: python

   from amplpy import AMPL, Environment
   ampl = AMPL(Environment(r"full path to the AMPL installation directory"))

Note that you may need to use raw strings (e.g., `r'C:\\ampl\\ampl.mswin64'`) or escape the slashes (e.g., `'C:\\\\ampl\\\\ampl.mswin64'`) if the path includes backslashes.

Development
-----------

Import the ``amplpy`` module with

.. code-block:: python

   import amplpy

Together with your existing AMPL implementation, this will provide the full
object library and access to all AMPL functions. Please make sure that the
folder containing the AMPL executable is in the system search path.

Deployment
----------

To deploy AMPL API applications we recommend the use of :ref:`amplpy.modules <amplpyModules>`.
Alternatively, make sure that AMPL is installed and that its directly is in the environment variable PATH.

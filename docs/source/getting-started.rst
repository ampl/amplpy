.. lblGettingStarted:

Initial Setup
=============

Installation
------------

The AMPL API can function as an add-on to any existing AMPL installation.
If you do not yet have an AMPL installation on the computer where you will
be working with the API, see our
`AMPL Community Edition page <https://ampl.com/ce/>`_ to download a
working version that can be installed quickly. Alternatively,
you can use :ref:`amplpy.modules <amplpyModules>` if you only intend to access AMPL from the Python environment.

In order to install the Python API you just need to run

.. code-block:: bash

    python -m pip install amplpy

Note: For Windows, Linux, and macOS, the ``amplpy`` package comes with binary
wheels. Please make sure that you are
using the latest version of ``pip`` before installing ``amplpy`` (upgrade using
``pip install pip --upgrade`` or ``python -m pip install pip --upgrade``).
If a binary wheel for your platform is not available,
a C++ compiler and python development libraries will be required.

.. _amplpyModules:

amplpy.modules
--------------

`AMPL and all solvers are now available as python packages <https://dev.ampl.com/ampl/python/modules.html>`_ for Windows, Linux, and macOS. For instance, to install AMPL with HiGHS and Gurobi,
you just need the following:

.. code-block:: bash

   # Install Python API for AMPL
   $ python -m pip install amplpy --upgrade

   # Install HiGHS and Gurobi (AMPL is installed automatically with any solver)
   $ python -m amplpy.modules install highs gurobi

   # Activate your license (e.g., free https://ampl.com/ce license)
   $ python -m amplpy.modules activate <license-uuid>

   # Confirm that the license is active
   $ python -m amplpy.modules run ampl -vvq

   # Import in Python
   $ python
   >>> from amplpy import AMPL
   >>> ampl = AMPL() # instantiate AMPL object

For Apple M1/M2, please make sure your have Rosetta 2 installed since not all modules are available for M1/M2. You can install it with: ``softwareupdate --install-rosetta``.

Complete documentation for ``amplpy.modules``: `AMPL Modules for Python <https://dev.ampl.com/ampl/python/modules.html>`_

Google Colab
------------

On Google Colab there is a default `AMPL Community
Edition license <https://ampl.com/ce/>`_ that gives you unlimited access to AMPL
with open-source solvers (e.g., HiGHS, CBC, Couenne, Ipopt, Bonmin)
or with commercial solvers from the `NEOS Server <https://www.neos-server.org/>`_ as described in `Kestrel documentation <https://dev.ampl.com/solvers/kestrel.html>`_.

In the list ``modules`` you need to include 
``"gokestrel"`` to use the `kestrel <https://dev.ampl.com/solvers/kestrel.html>`_ driver; 
``"highs"`` for the `HiGHS <https://highs.dev/>`_ solver; 
``"coin"`` for the `COIN-OR <https://www.coin-or.org/>`_ solvers.
To use other commercial solvers, your license needs to include the commercial solver (e.g., an AMPL CE commercial solver trial).

In order to be use AMPL on Google Colab you just need to following two code blocks
at the beginning of your notebook:

.. code-block:: bash

   # Install dependencies
   %pip install -q amplpy


.. code-block:: python

    # Google Colab & Kaggle integration
    from amplpy import AMPL, ampl_notebook
    ampl = ampl_notebook(
        modules=["coin", "highs", "gokestrel", "gurobi"], # modules to install
        license_uuid="default", # license to use
    ) # instantiate AMPL object and register magics

.. note::

    In these notebooks there are ``%%ampl_eval`` cells that allow you to run AMPL code directly from the notebook. 
    They are equivalent to ``ampl.eval("""cell content""")``.

Many notebooks with examples are available on the `AMPL Model Colaboratory <https://colab.ampl.com/>`_
and the new book `Hands-On Optimization with AMPL in Python 🐍 <https://ampl.com/mo-book/>`_.

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

    from amplpy import AMPL
    ampl = AMPL()

Note that you may need to use raw strings (e.g., `r'C:\\ampl\\ampl.mswin64'`) or escape the slashes (e.g., `'C:\\\\ampl\\\\ampl.mswin64'`) if the path includes backslashes.

Development
-----------

If you have an existing AMPL installation in the system search path:

.. code-block:: python

   from amplpy import AMPL
   ampl = AMPL()
   ampl.eval("option version;")

If you have an existing AMPL installation, but not in the system search path:

.. code-block:: python

    from amplpy import AMPL, add_to_path
    add_to_path(r"full path to the AMPL installation directory")
    ampl.eval("option version;")

If you are using :ref:`amplpy.modules <amplpyModules>`:

.. code-block:: python

    from amplpy import AMPL
    ampl = AMPL()
    ampl.eval("option version;")

Deployment
----------

To deploy AMPL API applications we recommend the use of :ref:`amplpy.modules <amplpyModules>`.
Alternatively, make sure that AMPL is installed and that its directory is in the environment variable PATH.

For a list of common deployment options available for Python see `AMPL integration with Python <https://dev.ampl.com/ampl/python/index.html>`_.

Docker deployment
^^^^^^^^^^^^^^^^^

`Docker containers <https://www.docker.com/>`_ are very popular for cloud deployments.
Since AMPL and all Solvers are now available as  :ref:`Python Packages <amplpyModules>`,
it is really simple to deploy with Docker:

.. code-block:: Dockerfile

    # Use any image as base image
    FROM python:3.9-slim-bullseye
    RUN python -m pip install amplpy # Install amplpy
    RUN python -m amplpy.modules install highs gurobi  # Install modules


You can build and run the container as follows:

.. code-block:: bash

    $ docker build . --tag ampl-container
    $ docker run --rm -it ampl-container bash
    root@c240a014dd67:/# python
    Python 3.9.16 (main, Jan 23 2023, 23:42:27)
    [GCC 10.2.1 20210110] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from amplpy import AMPL
    >>> ampl = AMPL()
    >>>

Other cloud deployment options such as cloud functions (e.g. `AWS Lambda <https://aws.amazon.com/lambda/>`_ and `Azure Functions <https://azure.microsoft.com/en-us/products/functions/>`_) are just as easy.
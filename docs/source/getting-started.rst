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

Follow the instructions on our `AMPL API <http://ampl.com/products/api/>`_
page to download the API package appropriate to your platform, and to add
the downloaded folder (directory) ``amplapi`` to your AMPL installation.

Initial test
------------

AMPL API includes a CMake script that can be used to build C++ examples on a
wide range of platforms. To begin, `download <http://www.cmake.org/download/>`_
and install the free CMake utility. Open a command/terminal window, make
``amplapi/examples/cpp`` the current folder (directory), and invoke

.. code-block:: none

   cmake .

to generate native makefiles or project files that can be used in the compiler
environment of your choice.

* Under Linux or any Unix-like environment, you will see a Makefile in the
  current directory; you can then build examples by running make.

* Under Windows with Visual Studio installed, the ``EXAMPLES.sln`` file and
  several project files will be created. You can then build examples using
  Visual Studio or MSBuild. Note that to compile the examples in 64 bits with 
  Visual Studio, the command line above must be amended to something like 
  the following:

  .. code-block:: none
   
    cmake -G "Visual Studio 14 2015 Win64" .

  where the version and year number can differ depending on the target version
  of Visual Studio. See `cmake --help` for a list of valid generators.

* Under Mac OS X with Xcode installed, an ``.xcodeproj`` file will be generated
  and can be used to build the examples.

To complete an initial test, build ``firstexample`` using these generated
files, and then invoke it with

.. code-block:: none

   ./firstexample <solver>

where optionally ``<solver>`` is the name of a solver that has been installed with AMPL.
(If a solver is not specified, AMPL's default choice will be used.) This will solve
several small diet problems and then display the optimal amounts of the foods
from the last solution.

Development
-----------

Include the ``ampl/ampl.h`` header from the ``amplapi/include`` folder (directory)
in your C++ code and link binaries with the AMPL library (|ampl_lib|) from
``amplapi/lib`` to use the AMPL API. Together with your existing AMPL
implementation, this will provide the full object library and access to all
AMPL functions.

The ``amplapi`` folder (directory) can be moved to a different location in
your computer’s filesystem, provided that the location of your AMPL executable
has been placed in the system search path.

Deployment
----------

To deploy AMPL API applications to users who do not have their own AMPL installations, 
include with your C++ application the AMPL
executable (``ampl`` or ``ampl.exe``); the shared library (|ampl_so|)
which contains the full implementation of the C++ object library; binaries
needed to run any solvers that are used; and an appropriate license
file for AMPL and solvers.

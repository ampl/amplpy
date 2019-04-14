Introduction
============

What is AMPL API?
-----------------

AMPL API is an interface that allows developers to access the features of the AMPL interpreter from within a
programming language. All model generation and solver interaction is handled directly by AMPL, which leads to
great stability and speed; the library just acts as an intermediary, and the added overhead (in terms of memory and
CPU usage) depends mostly on how much data is read back from AMPL, the size of the model as such is irrelevant.
Functions for directly assigning data to AMPL parameters and sets are provided, which can be used instead of the
normal AMPL data reading procedures. AMPL API has been written with usability in mind, and it is easy to access
its functionalities from  C++, Java,  MATLAB, C# and Python.

Who can use AMPL API
--------------------

The intended user of the library is the developer who needs to connect an application to optimization models and solvers,
or the analyst with some experience in programming who wants to build a quick proof-of-concept application.
:ref:`figArchitecture`  below shows a possible architecture and a sequence of interaction between a decision support system relying on
an existing IT framework and AMPL API.

.. _figArchitecture:

.. figure:: ../common/images/ArchitectureSchema.*
   :align: center
   :width: 621 px
   :height: 402 px
   :alt: Architecture Schema
   :figClass: align-center

   Architecture schema of AMPLAPI

System requirements
-------------------

As AMPL API uses AMPL for model generation, the AMPL executable is needed and is generally provided. The solution is then obtained through external solvers.
In general, a valid AMPL setup and Python 2.7 or 3.x are necessary and sufficient conditions for the correct execution of AMPL API.

The officially supported platforms are all Windows flavours, various Linux 32/64 bits and OSX.
Ports to any other platform supported by AMPL can be easily obtained.

For Windows only, please make sure that the Microsoft Visual C++ 2010 Redistributable Package (32 or 64 bits, depending on the architecture of 
the AMPL API you downloaded) is installed. It often comes preinstalled or as part of other software; it can also be downloaded from Microsoft
download center. Click `here <https://www.microsoft.com/en-us/download/details.aspx?id=5555>`_ for the 32 bits or 
`here <https://www.microsoft.com/en-us/download/details.aspx?id=14632>`_ for the 64 bits version.


About this manual
-----------------

This document intends to guide a developer in the process of implementing an “AMPL API based” application in Python.
The section :ref:`secClassStructure` presents the main logic of the API, which does not change depending on which programming environment is chosen.
Further sections walk the reader through the implementation of the most common applications, finally the sections
:ref:`secReferencePython` and :ref:`secExamplesPython` contain respectively the API reference documentation and a collection of examples.

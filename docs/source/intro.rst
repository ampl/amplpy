Introduction
============

What are AMPL APIs?
-------------------

`AMPL APIs <https://ampl.com/apis/>`_ are interfaces that allows developers to access the features of the AMPL interpreter from within a
programming language. All model generation and solver interaction is handled directly by AMPL, which leads to
great stability and speed; the library just acts as an intermediary, and the added overhead (in terms of memory and
CPU usage) depends mostly on how much data is read back from AMPL, the size of the model as such is irrelevant.
Functions for directly assigning data to AMPL parameters and sets are provided, which can be used instead of the
normal AMPL data reading procedures. AMPL API has been written with usability in mind, and it is easy to access
its functionalities from
`Python <https://ampl.com/api/latest/python>`_,
`R <https://ampl.com/api/latest/R>`_,
`C++ <https://ampl.com/api/latest/cpp>`_,
`C#/.NET <https://ampl.com/api/latest/dotnet>`_,
`Java <https://ampl.com/api/latest/java>`_, and
`MATLAB <https://ampl.com/api/latest/matlab>`_.

Who can use AMPL APIs
---------------------

The intended user of the library is the developer who needs to connect an application to optimization models and solvers,
or the analyst with some experience in programming who wants to build a quick proof-of-concept application.

System requirements
-------------------

In general, :ref:`amplpy.modules <amplpyModules>` or a valid AMPL setup, and Python 3 are necessary and sufficient conditions for the correct execution of AMPL API.

The officially supported platforms are Windows, Linux, and macOS.
Ports to any other platform supported by AMPL can be easily obtained.

For Windows only, please make sure that the Microsoft Visual C++ Redistributable Package is installed. It often comes preinstalled or as part of other software; it can also be downloaded from Microsoft
download center. Click `here <https://aka.ms/vs/16/release/vc_redist.x64.exe>`_ to download.


About this manual
-----------------

This document intends to guide a developer in the process of implementing an “AMPL API based” application in Python.
The section :ref:`secClassStructure` presents the main logic of the API, which does not change depending on which programming environment is chosen.
Further sections walk the reader through the implementation of the most common applications, finally the sections
:ref:`secReferencePython` and :ref:`secExamplesPython` contain respectively the API reference documentation and a collection of examples.

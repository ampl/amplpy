.. _secExamplesPython:

Examples
========

This section lists a few examples in Python.
These are the same files that can be found in the *examples* directory of the
distribution, and show the basic usage of the Python API.


Example 1: First steps
----------------------

:download:`firstexample.py <../../examples/firstexample.py>`

This example shows how to

* read an AMPL model
* reassign values to parameters
* solve the model
* display the objective function value


Example 2: Get and set AMPL options
-----------------------------------

:download:`optionsexample.py <../../examples/optionsexample.py>`

This example shows how to:

* get and set AMPL options


Example 3: Assign all data to a model and solve it
--------------------------------------------------

:download:`dietmodel.py <../../examples/dietmodel.py>`

This example shows how to:

* Assign all the data necessary to generate a model instance programmatically

Example 4: Build an efficient frontier
--------------------------------------

:download:`efficientfrontier.py <../../examples/efficientfrontier.py>`

This example shows how to:

* build an efficient frontier by repeteatly solve a portfolio problem in AMPL


Example 5: Simple heuristic
---------------------------

:download:`trackingmodel.py <../../examples/trackingmodel.py>`

This example shows how to:

* Do a simple heuristics for solving a QMIP problem, using the relaxed solution as a hint

.. _secExamplesPython:

Python API examples
===================

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


Example 3: Use AMPL asynchronously
----------------------------------

:download:`asyncexample.py <../../examples/asyncexample.py>`

This example shows how to:

* set a callback for AMPL async operation (implementing :class:`amplpy.Runnable`)
* start and interrupt async operations


Example 4: Get and set data through DataFrames
----------------------------------------------

:download:`dataframeexample.py <../../examples/dataframeexample.py>`

This example shows how to:

* Use :class:`amplpy.DataFrame` objects to assign values to sets and parameters
* Use an :class:`amplpy.DataFrame` object to fetch and decouple values from a variable


Example 5: Operate with multidimensional data
---------------------------------------------

:download:`multidimensionalexample.py <../../examples/multidimensionalexample.py>`

This example shows how to:

* Use a :class:`amplpy.DataFrame` to assign values to multidimensional parameters


Example 6: Assign all data to a model and solve it
--------------------------------------------------

:download:`dietmodel.py <../../examples/dietmodel.py>`

This example shows how to:

* Assign all the data necessary to generate a model instance programmatically


Example 7: Build an efficient frontier
--------------------------------------

:download:`efficientfrontier.py <../../examples/efficientfrontier.py>`

This example shows how to:

* build an efficient frontier by repeteatly solve a portfolio problem in AMPL


Example 8: Simple heuristic
---------------------------

:download:`trackingmodel.py <../../examples/trackingmodel.py>`

This example shows how to:

* Do a simple heuristics for solving a QMIP problem, using the relaxed solution as a hint

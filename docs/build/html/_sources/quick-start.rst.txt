.. _secPythonQuickStart:

Python quick start
==================

This section will show a simple example to illustrate various functionalities of the AMPL Python interface.
The full example prints the version of the AMPL interpreter used, loads a model from file and the corresponding
data file, solves it, gets some of the AMPL entities in Python and uses them to get the results and to assign data
programmatically. This section assumes that you are already familiar with the Python language.
Full class reference is given in :ref:`secReferencePython`.


Complete listing
----------------

This is the complete listing of the example. Please note that, for clarity of presentation,
all the code in the examples below does not include exception handling.

.. code-block:: python

  from amplpy import AMPL
  ampl = AMPL()

  # Interpret the two files
  ampl.read('models/diet/diet.mod')
  ampl.readData('models/diet/diet.dat')

  # Solve
  ampl.solve()

  # Get objective entity by AMPL name
  totalcost = ampl.getObjective('total_cost')
  # Print it
  print("Objective is:", totalcost.value())

  # Reassign data - specific instances
  cost = ampl.getParameter('cost')
  cost.setValues({'BEEF': 5.01, 'HAM': 4.55})
  print("Increased costs of beef and ham.")

  # Resolve and display objective
  ampl.solve()
  print("New objective value:", totalcost.value())

  # Reassign data - all instances
  cost.setValues([3, 5, 5, 6, 1, 2, 5.01, 4.55])

  print("Updated all costs.")

  # Resolve and display objective
  ampl.solve()
  print("New objective value:", totalcost.value())

  # Get the values of the variable Buy in a dataframe object
  buy = ampl.getVariable('Buy')
  df = buy.getValues()
  # Print them
  print(df)

  # Get the values of an expression into a DataFrame object
  df2 = ampl.getData('{j in FOOD} 100*Buy[j]/Buy[j].ub')
  # Print them
  print(df2)

Needed modules and AMPL environment creation
--------------------------------------------

For a simple hello world program, first import the needed classes from the `amplpy` package.

.. code-block:: python

  from amplpy import AMPL, DataFrame

Then copy the following statements to have a hello world application which gets the value
of the option `version` as defined in the underlying AMPL executable and prints the result
on the console.

.. code-block:: python

   ampl = AMPL()
   print(ampl.getOption('version'))


The first line creates a new AMPL object with all default settings, incapsulated in a smart pointer to ensure resource deletion.
The second, which is the preferred way to access AMPL options, gets the value of the option
`version` from AMPL as a string and prints the result on the active console.


If the AMPL installation directory is not in the system search path, you should create
the AMPL object as follows instead:

.. code-block:: python

   from amplpy import AMPL, Environment
   ampl = AMPL(Environment('full path to the AMPL installation directory'))

Note that you may need to use raw strings (e.g., `r'C:\\ampl\\ampl.mswin64'`) or escape the slashes (e.g., `'C:\\\\\\ampl\\\\\\ampl.mswin64'`) if the path includes backslashes.


Load a model from file
----------------------

The following lines use the method :func:`amplpy.AMPL.read` to load a model and data stored in external (AMPL) files.
If the files are not found, an IOError is thrown.

.. code-block:: python

   ampl.read('models/diet/diet.mod')
   ampl.readData('models/diet/diet.dat')

Once these commands are executed, the AMPL interpreter will have interpreted the content of the two files.
No further communication is made between the AMPL interpreter and the Python object, as every entity is created lazily (as needed).

Solve a problem
---------------

To solve the currently loaded problem instance, it is sufficient to issue the command:

.. code-block:: python

   ampl.solve()


Get an AMPL entity in the programming environment (get objective value)
-----------------------------------------------------------------------

AMPL API provides Python representations of the AMPL entities. Usually, not all the entities are
of interest for the programmer. The generic procedure is:

1. Identify the entities that need interaction (either data read or modification)
2. For each of these entities, get the entity through the AMPL API using one of the
   following functions: :func:`amplpy.AMPL.getVariable()`,
   :func:`amplpy.AMPL.getConstraint()`, :func:`amplpy.AMPL.getObjective()`,
   :func:`amplpy.AMPL.getParameter()` and :func:`amplpy.AMPL.getSet()`.


.. code-block:: python

    totalcost = ampl.getObjective('total_cost')
    print("Objective is:", totalcost.get().value())

It can be noted that we access an Objective to interrogate AMPL API about the objective function.
It is a collections of objectives. To access the single instance, the function get() should be used in
case of the objective, which gets the only instance of the objective.
Since objectives are often single instance, the value() function has been implemented in the class  :class:`amplpy.Objective`.
So, equivalently to the call above, the following call would return the same value, as it gives direct access
to the objective function value:

.. code-block:: python

   totalcost.value()

The output of the snippet above is::

   Objective is: 118.05940323955669

The same is true for all other entities.

Modify model data (assign values to parameters)
-----------------------------------------------

The input data of an optimization model is stored in its parameters; these can be scalar or vectorial entities.
Two ways are provided to change the value of vectorial parameter: change specific values or change all values at
once. The example shows an example of both ways, reassigning the values of the parameter costs firstly specifically,
then altogether. Each time, it then solves the model and get the objective function. The function used to change the
values is overloaded, and is in both cases :func:`amplpy.Parameter.setValues()`.

.. code-block:: python

   cost = ampl.getParameter('cost')
   cost.setValues({'BEEF': 5.01, 'HAM': 4.55})
   print("Increased costs of beef and ham.")
   ampl.solve();
   print("New objective value:", totalcost.value())

The code above assigns the values 5.01 and 4.55 to the parameter cost for the objects beef and ham respectively.
If the order of the indexing of an entity is known (i.e. for multiple reassignment), it is not necessary to specify
both the index and the value. A collection of values is assigned to each of the parameter values, in the order they are represented in AMPL.

.. code-block:: python

   cost.setValues([3, 5, 5, 6, 1, 2, 5.01, 4.55])
   print("Updated all costs.")
   ampl.solve()
   print("New objective value:", totalcost.value())

The statements above produce the following output::

   Objective is: 118.05940323955669
   Increased costs of beef and ham.
   New objective value: 144.41572037510653
   Updated all costs
   New objective value: 164.54375000000002

Get numeric values from variables
---------------------------------

To access all the numeric values contained in a Variable or any other entity, use a :class:`amplpy.DataFrame` object. Doing so, the data is detached from
the entity, and there is a considerable performance gain. To do so, we first get the Variable object from AMPL, then we get its data with the function :func:`amplpy.Entity.getValues()`.

.. code-block:: python

   # Get the values of the variable Buy in a dataframe object
   buy = ampl.getVariable('Buy')
   df = buy.getValues()
   # Print them
   print(df)


Get arbitrary values via ampl expressions
-----------------------------------------

Often we are interested in very specific values coming out of the optimization session. To make use of the power of AMPL expressions and avoiding
cluttering up the environment by creating entities, fetching data through arbitrary AMPL expressions is possible. For this model, we are interested
in knowing how close each decision variable is to its upper bound, in percentage.
We can obtain this data into a dataframe using the function :func:`amplpy.AMPL.getData()` with the code :

.. code-block:: python

  # Get the values of an expression into a DataFrame object
  df2 = ampl.getData("{j in FOOD} 100*Buy[j]/Buy[j].ub")
  # Print them
  print(df2)


Delete the AMPL object to free the resources
-----------------------------------------------------

It is good practice to make sure that the AMPL object is closed and all its resources released when it is not needed any more.
All the internal resources are automatically deallocated by the destructor of the AMPL object, so it is suggested to keep it stored
by value.

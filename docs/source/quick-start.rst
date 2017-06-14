.. _secPythonQuickStart:

Python quick start
==================

This section will show a simple example to illustrate various functionalities of the AMPL C++ interface.
The full example prints the version of the AMPL interpreter used, loads a model from file and the corresponding
data file, solves it, gets some of the AMPL entities in C++ and uses them to get the results and to assign data
programmatically. This section assumes that you are already familiar with the C++ language.
Full class reference is given in :ref:`secReferencePython`.


Complete listing
----------------

This is the complete listing of the example. Please note that, for clarity of presentation,
all the code in the examples below does not include exceptions handling.

.. code-block:: cpp

	#include "ampl/ampl.h"

	int main(int argc, char **argv) {

		ampl::AMPL ampl;

		std::string modelDirectory;
		if (argc == 2)
		  modelDirectory = argv[1];
		else
		  modelDirectory = "./models";

		// Interpret the two files
		ampl.read(modelDirectory + "/diet/diet.mod");
		ampl.readData(modelDirectory + "/diet/diet.dat");

		// Solve
		ampl.solve();

		// Get objective entity by AMPL name
		ampl::Objective totalcost = ampl.getObjective("total_cost");
		// Print it
		std::cout << "Objective is: " << totalcost.value() << std::endl;

		// Reassign data - specific instances
		ampl::Parameter cost = ampl.getParameter("cost");
		cost.setValues(new Tuple[2]{ ampl::Arg("BEEF"),  ampl::Arg("HAM")}, new Arg[2]{ 5.01, 4.55 },
					   2);
		std::cout << "Increased costs of beef and ham." << std::endl;

		// Resolve and display objective
		ampl.solve();
		std::cout << "New objective value: " << totalcost.value() << std::endl;

		// Reassign data - all instances
		ampl::Arg elements[8]{ 3, 5, 5, 6, 1, 2, 5.01, 4.55 };
		cost.setValues(elements);

		std::cout << "Updated all costs." << std::endl;

		// Resolve and display objective
		ampl.solve();
		std::cout << "New objective value: " << totalcost.value() << std::endl;

		// Get the values of the variable Buy in a dataframe object
		Variable buy = ampl.getVariable("Buy");
		ampl::DataFrame df;
		df = buy.getValues();
		// Print them
		df.print();
		ampl::DataFrame df2;
		// Get the values of an expression into a DataFrame object
		df2 = ampl.getData("{j in FOOD} 100*Buy[j]/Buy[j].ub");
		// Print them
		df2.print();

	}


Needed headers and AMPL environment creation
--------------------------------------------

For a simple hello world program, first include the needed headers. All the headers in the AMPL API distribution reside in the directory */ampl*.
The most important header is ``ampl.h``, which defines the main :class:`ampl::AMPL` class.

Please note that all classes part of the AMPL API are declared in the ``ampl`` namespace;
for clarity the namespace will be omitted but in the first code snippet below.


.. code-block:: cpp

  #include "ampl/ampl.h"

Then copy the following statements to have a hello world application which gets the value
of the option `version` as defined in the underlying AMPL executable and prints the result
on the console.

.. code-block:: cpp

   ampl::AMPL ampl;
   std::cout << ampl.getOption("version") << std::endl;


The first line creates a new AMPL object with all default settings, incapsulated in a smart pointer to ensure resource deletion.
The second, which is the preferred way to access AMPL options, gets the value of the option
`version` from AMPL as a string and prints the result on the active console.

Load a model from file
----------------------

The following lines use the method :func:`ampl::AMPL::read()` to load a model and data stored in external (AMPL) files.
If the files are not found, a runtime_error is thrown.

.. code-block:: cpp

   ampl.read(modelDirectory + "/diet/diet.mod");
   ampl.readData(modelDirectory + "/diet/diet.dat");

Once these commands are executed, the AMPL interpreter will have interpreted the content of the two files.
No further communication is made between the AMPL interpreter and the C++ object, as every entity is created lazily (as needed).

Solve a problem
---------------

To solve the currently loaded problem instance, it is sufficient to issue the command:

.. code-block:: cpp

   ampl.solve();


Get an AMPL entity in the programming environment (get objective value)
-----------------------------------------------------------------------

AMPL API provides C++ representations of the AMPL entities. Usually, not all the entities are
of interest for the programmer. The generic procedure is:

1. Identify the entities that need interaction (either data read or modification)
2. For each of these entities, create an object of the appropriate class in C++
3. Get the entity through the AMPL API using one of the following functions: :func:`ampl::AMPL::getVariable()`,
   :func:`ampl::AMPL::getConstraint()`, :func:`ampl::AMPL::getObjective()`,
   :func:`ampl::AMPL::getParameter()` and :func:`ampl::AMPL::getSet ()`.


.. code-block:: cpp

    ampl::Objective totalcost = ampl.getObjective("total_cost");
    std::cout << "Objective is: " << totalcost.get().value() << std::endl;

It can be noted that we access an Objective to interrogate AMPL API about the objective function.
It is a collections of objectives. To access the single instance, the function get() should be used in
case of the objective, which gets the only instance of the objective.
Since objectives are often single instance, the value() function has been implemented in the class  :cpp:class:`AMPL::Objective`.
So, equivalently to the call above, the following call would return the same value, as it gives direct access
to the objective function value:

.. code-block:: cpp

   totalcost.value();

The output of the snippet above is::

   Objective is: 118.05940323955669

The same is true for all other entities.

Modify model data (assign values to parameters)
-----------------------------------------------

The input data of an optimisation model is stored in its parameters; these can be scalar or vectorial entities.
Two ways are provided to change the value of vectorial parameter: change specific values or change all values at
once. The example shows an example of both ways, reassigning the values of the parameter costs firstly specifically,
then altogether. Each time, it then solves the model and get the objective function. The function used to change the
values is overloaded, and is in both cases :func:`ampl::Parameter::setValues()`.

.. code-block:: cpp

   ampl::Parameter cost = ampl.getParameter("cost");
   ampl::Tuple indices[] = { ampl::Tuple("BEEF"), ampl::Tuple("HAM") };
   double values[] = { 5.01, 4.55 };
   cost.setValues(indices, values, 2);
   std::cout << "Increased costs of beef and ham." << std::endl;
   ampl.solve();
   std::cout << "New objective value: " << totalcost.value() << std::endl;

The code above assigns the values 5.01 and 4.55 to the parameter cost for the objects beef and ham respectively.
If the order of the indexing of an entity is known (i.e. for multiple reassignment), it is not necessary to specify
both the index and the value. A collection of values is assigned to each of the parameter values, in the order they are represented in AMPL.

.. code-block:: cpp

   double elements[8] = { 3, 5, 5, 6, 1, 2, 5.01, 4.55 };
   cost.setValues(elements, 8);
   std::cout << "Updated all costs." << std::endl;
   ampl.solve();
   std::cout << "New objective value: " << totalcost.value() << std::endl;

The statements above produce the following output::

   Objective is: 118.05940323955669
   Increased costs of beef and ham.
   New objective value: 144.41572037510653
   Updated all costs
   New objective value: 164.54375000000002

Get numeric values from variables
---------------------------------

To access all the numeric values contained in a Variable or any other entity, use a :cpp:class:`ampl::DataFrame` object. Doing so, the data is detached from
the entity, and there is a considerable performance gain. To do so, we first get the Variable object from AMPL, then we get its data with the function :func:`ampl::Entity::getValues()`.

.. code-block:: cpp

   // Get the values of the variable Buy in a dataframe object
   ampl::Variable buy = ampl.getVariable("Buy");
   ampl::DataFrame df = buy.getValues();
   // Print them
   std::cout << df.toString() << std::endl;


Get arbitrary values via ampl expressions
-----------------------------------------

Often we are interested in very specific values coming out of the optimization session. To make use of the power of AMPL expressions and avoiding
cluttering up the environment by creating entities, fetching data through arbitrary AMPL expressions is possible. For this model, we are interested
in knowing how close each decision variable is to its upper bound, in percentage.
We can obtain this data into a dataframe using the function :func:`ampl::AMPL::getData()` with the code :

.. code-block:: cpp

  // Get the values of an expression into a DataFrame object
  ampl::DataFrame df2 = ampl.getData("{j in FOOD} 100*Buy[j]/Buy[j].ub");
  // Print them
  std::cout << df2.toString() << std::endl;


Delete the AMPL object to free the resources
-----------------------------------------------------

It is good practice to make sure that the AMPL object is closed and all its resources released when it is not needed any more.
All the internal resources are automatically deallocated by the destructor of the AMPL object, so it is suggested to keep it stored
by value.

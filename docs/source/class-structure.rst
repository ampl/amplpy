.. _secClassStructure:

Class structure
===============

AMPL API library consists of a collection of classes to interact with the underlying AMPL interpreter and to access
its inputs and outputs. It uses generic collections to represent the various entities which comprise a mathematical
model. The structure of these entities is explained in this section.

Please note that all classes and functions of the AMPL API are declared in the `ampl` namespace; for clarity the namespace will be omitted.

The main class used to interact with AMPL, instantiate and interrogate the models is :class:`ampl::AMPL`.
One object of this class represents an execution of an AMPL translator, and is the first class that has to be instantiated when
developing a solution based on AMPL API. It allows the interaction with the underlying AMPL translator, issuing commands,
getting diagnostics and controlling the process.

The model entities are represented by a set of classes, schematized in figure :ref:`figCDModelEntities`. These classes
represent the optimisation model being created and allow some manipulation and data assignments operations on such entities
and will be presented more in detail in the section :ref:`secModellingClasses`.


.. _figCDModelEntities:

.. figure:: images/ClassDiagramModelEntitiesNew.*
   :align: center
   :width: 836 px
   :height: 480 px
   :alt: Model entities class diagram
   :figClass: align-center

   Model entities classes overview


.. _secAMPLClass:

AMPL class
----------

For all calculations, AMPL API uses an underlying AMPL execution engine, which is wrapped by the class :class:`ampl::AMPL`.
Thus, one instance of this class is the first object to be created when writing a program which uses the AMPL API
library. The object is quite resource-heavy, therefore it should be explicitly closed as soon as it is not needed anymore,
with a call to :func:`ampl::AMPL::close()`
.

All the model creation and structural alteration operations are to be expressed in AMPL language through the
AMPL main object; moreover, the class provides access to the current state represented via the classes derived
from :class:`ampl::Entity`, as shown in section :ref:`secPythonAlgebraicEntitiesReference` and provides several other functionalities
(see :ref:`secReferencePython`).

The functions can be split in three groups: direct AMPL interaction, model interrogation and commands.

Direct interaction with AMPL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The methods available to input AMPL commands are :func:`ampl::AMPL::eval()`, :func:`ampl::AMPL::read()` and :func:`ampl::AMPL::readData()`;
they send the strings specified (or the specified files) to the AMPL engine for interpretation.
Their async versions: :func:`ampl::AMPL::evalAsync()`, :func:`ampl::AMPL::readAsync()` and :func:`ampl::AMPL::readDataAsync()`,
permit the calling program to continue the execution while the underlying AMPL process is busy in some time consuming operation,
and to define a callback to be executed when the operation is over.


Model interrogation
~~~~~~~~~~~~~~~~~~~

Evaluating AMPL files or statements creates various kind of entities in the underlying AMPL process.
To get the Java (or, in general, programmatic) representation of such entities, the programmer can follow two main courses.

* Get an :class:`ampl::EntityMap` of all available entities, to iterate through them. The methods to obtain such lists are:

  * :func:`ampl::AMPL::getVariables()` gets the map of all the defined variables
  * :func:`ampl::AMPL::getConstraints()` gets the map of all the defined constraints
  * :func:`ampl::AMPL::getObjectives()` gets the map of all the defined objectives
  * :func:`ampl::AMPL::getSets()` gets the map of all the defined sets
  * :func:`ampl::AMPL::getParameters()` gets the map of all the defined parameters

* Knowing the AMPL name of an entity, use commands to get the specific entity directly:

  * :func:`ampl::AMPL::getVariable()` returns the :class:`ampl::Variable` representing the AMPL variable with the specified name, if it exists
  * :func:`ampl::AMPL::getConstraint()` returns the :class:`ampl::Constraint` representing the AMPL constraint with the specified name, if it exists
  * :func:`ampl::AMPL::getObjective()` returns the :class:`ampl::Objective` representing the AMPL objective with the specified name, if it exists
  * :func:`ampl::AMPL::getParameter()` returns the :class:`ampl::Parameter` representing the AMPL parameter with the specified name, if it exists
  * :func:`ampl::AMPL::getSet()` returns the :class:`ampl::Set` representing the AMPL set with the specified name, if it exists


Once the desired entities have been created, it is possible to use their properties and methods to manipulate the model
and to extract or assign data. Updating the state of the programmatic entities is implemented lazily and uses proper
dependency handling. Communication with the underlying engine is therefore executed only when an entity's properties
are being accessed and only when necessary.
An entity is invalidated (needs refreshing) if one of the entities it depends from has been manipulated or if a generic
AMPL statement evaluation is performed (through :func:`ampl::AMPL::eval()` or similar routines). This is one of the reasons
why it is generally better to use the embedded functionalities (e.g. fixing a variable through the corresponding API
function call) than using AMPL statements: in the latter case, the API invalidates all entities, as the effects of
such generic statements cannot be predicted.
Refreshing is transparent to the user, but must be taken into account when implementing functions
which access data or modify entities frequently.


Commands and options
~~~~~~~~~~~~~~~~~~~~

Some AMPL commands are encapsulated by functions in the :class:`ampl::AMPL` class for ease of access.
These comprise :func:`ampl::AMPL::solve()` and others.
To access and set options in AMPL, the functions :func:`ampl::AMPL::getOption()` and :func:`ampl::AMPL::setOption()` are provided.
Together with their type-safe alternatives (e.g. :func:`ampl::AMPL::getBoolOption()` and :func:`ampl::AMPL::setBoolOption()`), these functions
provide an easier programmatic access to the AMPL options.
In general, when an encapsulation is available for an AMPL command, the programmatic access to it is to be preferred to calling the same command using
:func:`ampl::AMPL::eval()`.


Output and errors handling
~~~~~~~~~~~~~~~~~~~~~~~~~~

The output from the AMPL translator is handled implementing the interface :class:`ampl::OutputHandler`.
The method :func:`ampl::OutputHandler::output()` is called at each block of output from the translator. The current output handler
can be accessed and set via :func:`ampl::AMPL::getOutputHandler()` and :func:`ampl::AMPL::setOutputHandler()`;
the default output handler prints each block to the standard console output.

Error handling is two-faced:

* Errors coming from the underlying AMPL translator (e.g. syntax errors and warnings obtained calling the :func:`ampl::AMPL::eval()` method)
  are handled by the :class:`ampl::ErrorHandler` which can be set and get via :func:`ampl::AMPL::getErrorHandler()`
  and :func:`ampl::AMPL::setErrorHandler()`.
* Generic errors coming from the API, which are detected outside the translator are thrown as exceptions.

The default implementation of the error handler throws exceptions on errors and prints the warnings to stdout.



.. _secModellingClasses:

Modelling entities classes
--------------------------

This group of classes represents the basic entities of an AMPL optimisation
model: variables, constraints, objectives, parameters and sets.
They are used to access the current state of the AMPL translator
(e.g. to find the values of a variable), and to some extent they can be
used for data input (e.g. assign values to a parameter, fix a variable).

Objects of these classes cannot be created programmatically by the user: the model creation and structural
modification is handled in AMPL (see section :ref:`secAMPLClass`), through the methods :func:`ampl::AMPL::eval()`
and :func:`ampl::AMPL::read()`. The two base classes are :class:`ampl::Entity` and :class:`ampl::Instance`.

The classes derived from :class:`ampl::Entity` represent algebraic entites
(e.g. a variable indexed over a set in AMPL), and are implemented as a map
from an object (number, string or tuple) to an :class:`ampl::Instance` which allow access
to its instances (methods :func:`ampl::BasicEntity::operator[]()` and
:func:`ampl::BasicEntity::get()` ).
The case of scalar entities (like the AMPL entity defined by ``var x;``) is handled at Entity level, and will be
illustrated in the paragraph regarding instances below.
The derived classes are: :class:`ampl::Variable`, :class:`ampl::Constraint`, :class:`ampl::Parameter`,
:class:`ampl::Objective` and :class:`ampl::Set`.

Any object of a class derived from :class:`ampl::Instance` represents a single instance of an algebraic entity
(e.g.  the value of a variable for a specific value of its indexing set).
The derived classes are: :class:`ampl::VariableInstance`, :class:`ampl::ConstraintInstance`,
:class:`ampl::ObjectiveInstance` and :class:`ampl::SetInstance`.
The composition of these classes can be described as shown below:

.. _figEntityInstance:

.. figure:: ../common/images/EntityMapItem.*
   :align: center
   :width: 560 px
   :height: 137 px
   :alt: Relationship between Entity and Instance
   :figClass: align-center

   Relationship between Entity and Instance


The UML diagram in figure :ref:`figEntityInstance` illustrates that each :class:`ampl::Entity` (algebraic entity in AMPL)
can contain various :class:`ampl::Instance` objects (instances in AMPL), while each ``Instance`` has to be part of exactly one
``Entity``.
The exact methods and properties of the entity depend on the particular kind of entity under consideration
(i.e. variable, constraint, parameter).

As an example, the class :class:`ampl::Variable` has functionalities like :func:`ampl::Variable::fix()` and :func:`ampl::Variable::unfix()`,
which would fix or unfix all instances which are part of the algebraic entity, and its corresponding instance
class :class:`ampl::VariableInstance` has properties like :func:`ampl::VariableInstance::value()`
and :func:`ampl::VariableInstance::dual()` (together with instance level fix and unfix methods).

The class :class:`ampl::Constraint` has functionalities like :func:`ampl::Constraint::drop()` and
:func:`ampl::Constraint::restore()`,
and its instance level class :class:`ampl::ConstraintInstance` properties like :func:`ampl::ConstraintInstance::body()` and
:func:`ampl::ConstraintInstance::dual()`
(and methods like drop and restore for the single instance).

Note that the class :class:`ampl::Parameter`, which represent an algebraic parameter, does not have
an instance level class; its instances are represented by objects instead (typically double numbers or strings).


.. _secAccessInstancesAndValues:

Access to instances and values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The instances can be accessed from the parent Entity through functions like :func:`ampl::BasicEntity::get()`, available for
all entity classes or via the indexing operator.
All data corresponding to the entity can be accessed through the instances, but the computational overhead of such kind of
access is quite considerable. To avoid this, the user can gain bulk data access through a :class:`ampl::DataFrame` object;
reference to these object can be obtained using :func:`ampl::Entity::getValues` methods.
In case of scalar entities (e.g. the entity declared in AMPL with the statement ``var x;``), all the instance specific methods are
replicated at Entity level, to allow the code fragment ``value = x.value();`` instead of the more explicit ``value = x.get().value()``.
See example below:


.. code-block:: cpp

   double value;
   ampl::AMPL ampl;

   ampl.eval("var x;");
   ampl::Variable x = ampl.getVariable("x");
   value = x.value();       // Compact access to scalar entities
   value = x.get().value(); // Access through explicit reference to the instance


Indexed entities are central in modelling via AMPL. This is why the :func:`ampl::BasicEntity::get()` method
and the indexing operator have various overloads and can be used in multiple ways, to adapt to specific use cases.
These will be presented below, by mean of some examples.



**Scalar Entities** In general, as seen above, access to an instance of a scalar entity is not needed, as all functionalities of the instance are replicated at entity level in this case. Anyway,
to gain explicit access to an instance, the function :func:`ampl::BasicEntity::get()` can be used without parameters, as shown below.

.. code-block:: cpp

   ampl.eval("var x;");
   VariableInstance x = ampl.getVariable("x").get();

**Indexed Entities** To gain access to instances in indexed entities,
this set of functions can be used, depending on the context. For specialised conversion of indices, see the function :func:`ampl::Tuple::join`.


See the examples below:

* *Each item is a index value* : Each item passed to the function is interpreted as the value of one of its indices (up to 4 indices)
* *The (only) item is an array containing all the indices*
* *The (only) item is a* :class:`ampl::Tuple` *representing all the indices*
* *Indices values are available in a few tuples*

.. code-block:: cpp

   ampl::AMPL ampl;
   ampl.eval("var x{1..2, 4..5, 7..8};");
   ampl::Variable x = ampl.getVariable("x");

   // Each item an index
   ampl::VariableInstance instance = x.get(1, 4, 7); // or

   // The item is an array
   ampl::Variant values[] = { 1, 4, 7 };
   instance = x.get(ampl::Tuple(values, 3)); // or
   instance = x[ampl::Tuple(values, 3)];

   // The item is a tuple
   ampl::Tuple t(1, 4, 7);
   instance = x.get(t); // or
   instance = x[t];

   // The index is the joining of some tuples
   ampl::Tuple t1(1);
   ampl::Tuple t2(4, 7);
   t = ampl::Tuple::join(t1, t2);
   instance = x.get(t); // or
   instance = x[t];


For a more idiomatic style, AMPL API allows access to the instances through iterators. See the examples below which use
the same declarations of the example above to illustrate how to:

* Find if an instance exists or not
* Enumerate all the instances (C++11 and C++98 syntax)

.. code-block:: cpp

  // Find using iterator
  ampl::Variable::iterator it = x.find(t);
  if (it == x.end())
    std::cout << "Instance not found\n";
  else
    instance = it->second;

  // Access all instances using iterator (C++11)
  for (auto i : x)
    std::cout << i.second.name() << std::endl;

  // Access all instances using iterator (C++98)
  ampl::Variable::iterator end = x.end();
  for (it = x.begin(); it != end; ++it)
    std::cout << it->second.name() << std::endl;


The currently defined entities are obtained from the various get methods of the :class:`ampl::AMPL` object
(see section :ref:`secAMPLClass`). Once a reference to an entity is created, the entity is automatically kept up-to-date
with the corresponding entity in the AMPL interpreter. That is, if a reference to a newly created AMPL variable
is obtained by means of :func:`ampl::AMPL::getVariable()`, and the model the variable is part of is then solved
by means of :func:`ampl::AMPL::solve()`, the values of the instances of the variable will automatically be updated.
The following code snippet should demonstrate the concept.

.. code-block:: cpp

   ampl.eval("var x;");
   ampl.eval("maximize z: x;");
   ampl.eval("subject to c: x<=10;");
   ampl::Variable x = ampl.getVariable("x");

   // At this point x.value() evaluates to 0
   std::cout << x.value(); // prints 0

   ampl.solve();

   // At this point x.value() evaluates to 10
   std::cout << x.value(); // prints 10


Relation between entities and data
----------------------------------

The entities and instances in AMPL store data (numbers or strings) and can be indexed, hence the instances available depend
on the values in the indexing set(s).  The order in which these indexing sets is handled in the AMPL entities is
not always consistent with the ordering in which the data for such sets is defined, so it is often desirable, even when interested
in only data (decoupled from the AMPL entities) to keep track of the indexing values which corresponds to each value.

Moreover, when dealing with AMPL entities (like :class:`ampl::Variable`), consistency is guaranteed for every instance.
This means that, if a reference to an instance is kept and in the underlying AMPL interpreter the value of the instance
is changed, the value read from the instance object will be always consistent with the AMPL value and, if an instance is
deleted in AMPL, an exception will be thrown when accessing it. This has the obvious benefit of allowing the user to rely
on the values of the instances, but has a price in terms of computational overhead. For example, accessing in this way the value
of 1000 instances:

.. code-block:: cpp

  ampl::AMPL ampl;
  ampl.eval("set A := 1..1000; param c{i in A} default 0; var x{i in 1..1000} := c[i];");

  // Enumerate through all the instances of c and set their values
  ampl::Parameter c = ampl.getParameter("c");
  for (std::size_t i = 1; i <= c.numInstances(); i++)
    c.set(i, i * 1.1);
  // Enumerate through all the instances and print their values
  ampl::Variable x = ampl.getVariable("x");
  for (auto xi : x)
    std::cout << xi.second.value() << std::endl;


will check at each access if the referenced instance is valid or not, resulting in a computational overhead. Moreover,
in a multi-threaded environment (like when using :func:`ampl::AMPL::evalAsync()`), the value of the underlying collection of instances
could be be changed by the interpreter while the main program is iterating through them, leading to undetermined results.

To ease data communication and handling, the class :class:`ampl::DataFrame` is provided. Its usage is two-fold:

* It allows definition of data for multiple parameters in one single call to the underlying interpterer
* It decouples data and entities, reducing the computational overhead and risks related to concurrency

`ampl::DataFrame` objects should therefore be used in these circumnstances, together with the methods
:func:`ampl::AMPL::setData()` and :func:`ampl::Entity::getValues()`.

.. code-block:: cpp

   // Create a new dataframe with one indexing column (A) and another column (c)
   ampl::DataFrame df(1, ampl::StringArgs("A", "c"));
   for (int i = 1; i <= 1000; i++)
    df.addRow(i, i * 1.1);

   {
    ampl::AMPL ampl;
    ampl.eval("set A; param c{i in A} default 0; var x{i in A} := c[i];");
    // Assign data to the set A and the parameter c in one line
    ampl.setData(df, "A");

    ampl::Variable x = ampl.getVariable("x");
    // From the following line onwards, df is uncoupled from the
    // modelling system,
    df = x.getValues();
   } // ampl object goes out of scope

   // Prints all the values
   for (auto row : df)
    std::cout << row[0].dbl() << " " << row[1].dbl() << "\n";

   // Prints all the values using DataFrame's routine
   std::cout << df.toString();

The underlying AMPL interpreter does not need to be open when using the dataframe object, but it maintains all
the correspondence between indexing set and actual value of the instances.


.. _secAccessToScalars:

Access to scalar values
~~~~~~~~~~~~~~~~~~~~~~~

Simplified access to scalar values, like the value of a scalar variable or parameter or, in general, any
AMPL expression that can be evaluated to a single string or number, is possible using the convenience method :func:`ampl::AMPL::getValue()`.
This method will fail if called on an AMPL expression which does not evaluate to a single value. See below for an example:


.. code-block:: cpp

   ampl::AMPL ampl;
   ampl.eval("var x{i in 1..3} := i;");
   ampl.eval("param p symbolic := 'test';");
   ampl.eval("param pp := 4;");
   // x2 will have the value 2
   std::cout << ampl.getValue("x[2]").dbl() << std::endl;
   // p will have the value "test"
   std::cout << ampl.getValue("p").c_str() << std::endl;
   // pp will have the value 4
   std::cout << ampl.getValue("pp").dbl() << std::endl;


.. _secVariableSuffixesNotes:

Note on variables suffixes
--------------------------

For AMPL versions prior to 20150516, there was a glitch with
v.lb, v.ub, v.lslack, v.uslack, and v.slack where v is a variable
instantiated without need of presolve and after one or more
other variables have been instantiated.  Example:

.. code-block:: ampl

    var x <= 0;
    var y <= 0;
    display y.lb;
    display x.ub;
    # x.ub was wrong (with separate display commands)
    # but all went well with "display y.lb, x.ub;"

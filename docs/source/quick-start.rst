.. _secPythonQuickStart:

Quick start
===========

This section will show a simple example to illustrate various functionalities of the AMPL Python interface.
The full example prints the version of the AMPL interpreter used, loads a model from file and the corresponding
data from ``pandas.DataFrame`` objects, solves it, gets some of the AMPL entities in Python and uses them to get the results and to assign data
programmatically.

This section assumes that you are already familiar with the Python language and
the `Pandas library <https://pandas.pydata.org/>`_. Note that data can be loaded from various sources such as table handlers, data files, and other Python native data structures such as ``list`` and ``dict``. 
Full class reference is given in :ref:`secReferencePython`.

.. grid:: 1 1 2 2
    :gutter: 0
    :margin: 0
    :padding: 0

    .. grid-item-card::
        :margin: 0
        :padding: 0

        Quick Start using Pandas dataframes
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        Data can be loaded in various forms, one of which is ``pandas.DataFrame`` objects.

        .. image:: https://colab.research.google.com/assets/colab-badge.svg
            :target: https://colab.research.google.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/pandasdiet.ipynb
            :alt: Open In Colab

        .. image:: https://kaggle.com/static/images/open-in-kaggle.svg
            :target: https://kaggle.com/kernels/welcome?src=https://github.com/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/pandasdiet.ipynb
            :alt: Kaggle

        .. image:: https://assets.paperspace.io/img/gradient-badge.svg
            :target: https://console.paperspace.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/pandasdiet.ipynb
            :alt: Gradient

        .. image:: https://studiolab.sagemaker.aws/studiolab.svg
            :target: https://studiolab.sagemaker.aws/import/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/pandasdiet.ipynb
            :alt: Open In SageMaker Studio Lab

    .. grid-item-card::
        :margin: 0
        :padding: 0

        Quick Start using lists and dictionaries
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        Data can be loaded in various forms, including Python lists and dictionaries.

        .. image:: https://colab.research.google.com/assets/colab-badge.svg
            :target: https://colab.research.google.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/nativediet.ipynb
            :alt: Open In Colab

        .. image:: https://kaggle.com/static/images/open-in-kaggle.svg
            :target: https://kaggle.com/kernels/welcome?src=https://github.com/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/nativediet.ipynb
            :alt: Kaggle

        .. image:: https://assets.paperspace.io/img/gradient-badge.svg
            :target: https://console.paperspace.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/nativediet.ipynb
            :alt: Gradient

        .. image:: https://studiolab.sagemaker.aws/studiolab.svg
            :target: https://studiolab.sagemaker.aws/import/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/nativediet.ipynb
            :alt: Open In SageMaker Studio Lab

.. note::
    Many Jupyter notebooks with examples are available on the `AMPL Model Colaboratory <https://colab.ampl.com/>`_
    and the new book `Hands-On Mathematical Optimization with AMPL in Python 🐍 <https://ampl.com/mo-book/>`_.

    You should also check out our collection of interactive `Streamlit Apps <https://ampl.com/streamlit>`_ and
    learn how easy you can build your own apps.

Complete listing
----------------

This is the complete listing of the example. You can download it from: :download:`diet_model.py <../../examples/diet_model.py>`. A simplified version using a data file instead of Pandas can be download from: :download:`first_example.py <../../examples/first_example.py>`. Please note that, for clarity of presentation,
all the code in the examples below does not include exception handling.

.. code-block:: python

    from amplpy import AMPL
    import pandas as pd # for pandas.DataFrame objects (https://pandas.pydata.org/)
    import numpy as np # for numpy.matrix objects (https://numpy.org/)

    # Create an AMPL instance
    ampl = AMPL()

    """
    # If you are not using amplpy.modules, and the AMPL installation directory
    # is not in the system search path, add it as follows:
    from amplpy import add_to_path
    add_to_path(r"full path to the AMPL installation directory")
    """

    # Load the model (alternatively, you can use ampl.eval("""...""") to define the model)
    ampl.read("diet.mod")

    # Load the data from pandas.DataFrame objects:
    food_df, nutr_df, amt_df = prepare_data()
    # 1. Send the data from "amt_df" to AMPL and initialize the indexing set "FOOD"
    ampl.set_data(food_df, "FOOD")
    # 2. Send the data from "nutr_df" to AMPL and initialize the indexing set "NUTR"
    ampl.set_data(nutr_df, "NUTR")
    # 3. Set the values for the parameter "amt" using "amt_df"
    ampl.get_parameter("amt").set_values(amt_df)

    # Specify the solver to use (e.g., HiGHS)
    ampl.option["solver"] = "highs"
    # Solve
    ampl.solve()
    # Stop if the model was not solved
    assert ampl.solve_result == "solved"

    # Get objective entity by AMPL name
    totalcost = ampl.get_objective("Total_Cost")
    # Print it
    print("Objective is:", totalcost.value())

    # Reassign data - specific instances
    cost = ampl.get_parameter("cost")
    cost.set_values({"BEEF": 5.01, "HAM": 4.55})
    print("Increased costs of beef and ham.")

    # Resolve and display objective
    ampl.solve()
    # Stop if the model was not solved
    assert ampl.solve_result == "solved"
    print("New objective value:", totalcost.value())

    # Reassign data - all instances
    cost.set_values(
        {
            "BEEF": 3,
            "CHK": 5,
            "FISH": 5,
            "HAM": 6,
            "MCH": 1,
            "MTL": 2,
            "SPG": 5.01,
            "TUR": 4.55,
        }
    )

    print("Updated all costs.")

    # Resolve and display objective
    ampl.solve()
    # Stop if the model was not solved
    assert ampl.solve_result == "solved"
    print("New objective value:", totalcost.value())

    # Get the values of the variable Buy in a pandas.DataFrame object
    df = ampl.get_variable("Buy").get_values().to_pandas()
    # Print them
    print(df)

    # Get the values of an expression into a pandas.DataFrame object
    df2 = ampl.get_data("{j in FOOD} 100*Buy[j]/Buy[j].ub").to_pandas()
    # Print them
    print(df2)

Where ``prepare_data`` is the following function that returns three ``pandas.DataFrame`` objects:

.. code-block:: python

    def prepare_data():
        food_df = pd.DataFrame(
            [
                ("BEEF", 3.59, 2, 10),
                ("CHK", 2.59, 2, 10),
                ("FISH", 2.29, 2, 10),
                ("HAM", 2.89, 2, 10),
                ("MCH", 1.89, 2, 10),
                ("MTL", 1.99, 2, 10),
                ("SPG", 1.99, 2, 10),
                ("TUR", 2.49, 2, 10),
            ],
            columns=["FOOD", "cost", "f_min", "f_max"],
        ).set_index("FOOD")

        # Create a pandas.DataFrame with data for n_min, n_max
        nutr_df = pd.DataFrame(
            [
                ("A", 700, 20000),
                ("C", 700, 20000),
                ("B1", 700, 20000),
                ("B2", 700, 20000),
                ("NA", 0, 50000),
                ("CAL", 16000, 24000),
            ],
            columns=["NUTR", "n_min", "n_max"],
        ).set_index("NUTR")

        amt_df = pd.DataFrame(
            np.array(
                [
                    [60, 8, 8, 40, 15, 70, 25, 60],
                    [20, 0, 10, 40, 35, 30, 50, 20],
                    [10, 20, 15, 35, 15, 15, 25, 15],
                    [15, 20, 10, 10, 15, 15, 15, 10],
                    [928, 2180, 945, 278, 1182, 896, 1329, 1397],
                    [295, 770, 440, 430, 315, 400, 379, 450],
                ]
            ),
            columns=food_df.index.to_list(),
            index=nutr_df.index.to_list(),
        )
        return food_df, nutr_df, amt_df

.. note::

    ``amplpy`` should be able to load ``pandas.DataFrame`` objects with millions of rows
    in a couple of seconds, but if you are dealing with such large amounts of data (e.g., over 10 millions of rows), you may
    consider using a table handler to transfer the data directly into AMPL from its source without
    having to pass it though Python, as Python may sometimes be the performance bottleneck. We have table handlers such as
    `amplcsv <https://plugins.ampl.com/amplcsv.html>`_ (CSV files),
    `amplxl <https://plugins.ampl.com/amplxl.html>`_ (XLSX files), and
    `eodbc <https://plugins.ampl.com/eodbc.html>`_ (Databases such as MySQL and PostgreSQL via ODBC).
    You can still use the API to update the data and retrieve solutions, but you may gain substantial performance by
    passing the initial values directly into AMPL.

Needed modules and AMPL environment creation
--------------------------------------------

For a simple hello world program, first import the needed classes from the ``amplpy`` package.

.. code-block:: python

  from amplpy import AMPL

Then copy the following statements to have a hello world application which gets the value
of the option `version` as defined in the underlying AMPL executable and prints the result
on the console.

.. code-block:: python

   ampl = AMPL()
   print(ampl.get_option("version"))


The first line creates a new AMPL object with all default settings.
The second, which is the preferred way to access AMPL options, gets the value of the option
`version` from AMPL as a string and prints the result on the active console.


If you are not using :ref:`amplpy.modules <amplpyModules>`, and your AMPL installation directory is not in the system search path, add it as follows:

.. code-block:: python

   from amplpy import AMPL, add_to_path
   add_to_path(r"full path to the AMPL installation directory")
   ampl = AMPL()

Note that you may need to use raw strings (e.g., `r"C:\\ampl\\ampl.mswin64"`) or escape the slashes (e.g., `"C:\\\\\\ampl\\\\\\ampl.mswin64"`) if the path includes backslashes.

Load model and data from files
------------------------------

If you have AMPL model and data files, you can use
the method :func:`amplpy.AMPL.read` to load model files and :func:`amplpy.AMPL.read_data` to load data files.
If the files are not found, an IOError is raised.

.. code-block:: python

   ampl.read("models/diet.mod")
   ampl.read_data("models/diet.dat")

Once these commands are executed, the AMPL interpreter will have interpreted the content of the two files.
No further communication is made between the AMPL interpreter and the Python object, as every entity is created lazily (as needed).

Load model using eval
---------------------

An alternative to :func:`amplpy.AMPL.read` for loading models, is the method
:func:`amplpy.AMPL.eval` to load a model directly from a string as follows:

.. code-block:: python

    ampl.eval(r"""
        set NUTR;
        set FOOD;

        param cost {FOOD} > 0;
        param f_min {FOOD} >= 0;
        param f_max {j in FOOD} >= f_min[j];

        param n_min {NUTR} >= 0;
        param n_max {i in NUTR} >= n_min[i];

        param amt {NUTR,FOOD} >= 0;

        var Buy {j in FOOD} >= f_min[j], <= f_max[j];

        minimize Total_Cost:  sum {j in FOOD} cost[j] * Buy[j];

        subject to Diet {i in NUTR}:
        n_min[i] <= sum {j in FOOD} amt[i,j] * Buy[j] <= n_max[i];
    """)

Using :func:`amplpy.AMPL.eval` or :func:`amplpy.AMPL.read` to load a model is a matter of preference.

Load the data using Pandas objects
----------------------------------

Data can be loaded in various ways, one of them is ``pandas.DataFrame`` objects.
In the snippet below, :func:`amplpy.AMPL.set_data` is used to load data from
the ``pandas.DataFrame`` objects ``food_df`` and ``nutr_df``,
and :func:`amplpy.Parameter.set_values` is used to load data in ``amt_df`` into the AMPL parameter ``amt``.

.. code-block:: python

    # the function prepare_data returns three pandas.DataFrame objects
    food_df, nutr_df, amt_df = prepare_data()
    # 1. Send the data from "amt_df" to AMPL and initialize the indexing set "FOOD"
    ampl.set_data(food_df, "FOOD")
    # 2. Send the data from "nutr_df" to AMPL and initialize the indexing set "NUTR"
    ampl.set_data(nutr_df, "NUTR")
    # 3. Set the values for the parameter "amt" using "amt_df"
    ampl.get_parameter("amt").set_values(amt_df)


Load the data using lists and dictionaries
------------------------------------------

AMPL parameters are very similar to Python dictionaries and AMPL sets are very similar to Python lists and sets.
For the same model, all data could also have been loaded using native Python lists and dictionaries.

.. code-block:: python

    # foods[food] = (cost, f_min, f_max)
    foods = {
        "BEEF": (3.59, 2, 10),
        "CHK": (2.59, 2, 10),
        "FISH": (2.29, 2, 10),
        "HAM": (2.89, 2, 10),
        "MCH": (1.89, 2, 10),
        "MTL": (1.99, 2, 10),
        "SPG": (1.99, 2, 10),
        "TUR": (2.49, 2, 10),
    }
    # nutrients[nutr] = (n_min, n_max)
    nutrients = {
        "A": (700, 20000),
        "C": (700, 20000),
        "B1": (700, 20000),
        "B2": (700, 20000),
        "NA": (0, 50000),
        "CAL": (16000, 24000),
    }
    ampl.set["FOOD"] = list(foods.keys())
    ampl.param["cost"] = {food: cost for food, (cost, _, _) in foods.items()}
    ampl.param["f_min"] = {food: f_min for food, (_, f_min, _) in foods.items()}
    ampl.param["f_max"] = {food: f_max for food, (_, _, f_max) in foods.items()}
    ampl.set["NUTR"] = list(nutrients.keys())
    ampl.param["n_min"] = {nutr: n_min for nutr, (n_min, _) in nutrients.items()}
    ampl.param["n_max"] = {nutr: n_max for nutr, (_, n_max) in nutrients.items()}
    amounts = [
        [60, 8, 8, 40, 15, 70, 25, 60],
        [20, 0, 10, 40, 35, 30, 50, 20],
        [10, 20, 15, 35, 15, 15, 25, 15],
        [15, 20, 10, 10, 15, 15, 15, 10],
        [928, 2180, 945, 278, 1182, 896, 1329, 1397],
        [295, 770, 440, 430, 315, 400, 379, 450],
    ]
    ampl.param["amt"] = {
        (nutrient, food): amounts[i][j]
        for i, nutrient in enumerate(nutrients)
        for j, food in enumerate(foods)
    }

In this example we used the :ref:`secAlternativeMethodToAccessEntities` as it is more compact.
To use ``pandas.DataFrame`` objects or native ``list`` and ``dict`` objects are a matter of preference.


Solve a problem
---------------

To solve the currently loaded problem instance, it is sufficient to issue the following commands:

.. code-block:: python

   # Specify the solver to use (e.g., HiGHS)
   ampl.option["solver"] = "highs"
   
   # Solve the problem
   ampl.solve()

   # Stop if the model was not solved
   assert ampl.solve_result == "solved"

Get an AMPL entity in the programming environment (get objective value)
-----------------------------------------------------------------------

AMPL API provides Python representations of the AMPL entities. Usually, not all the entities are
of interest for the programmer. The generic procedure is:

1. Identify the entities that need interaction (either data read or modification)
2. For each of these entities, get the entity through the AMPL API using one of the
   following functions: :func:`amplpy.AMPL.get_variable()`,
   :func:`amplpy.AMPL.get_constraint()`,
   :func:`amplpy.AMPL.get_objective()`,
   :func:`amplpy.AMPL.get_parameter()`
   and :func:`amplpy.AMPL.get_set()`.


.. code-block:: python

    totalcost = ampl.get_objective("Total_Cost")
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
values is overloaded, and is in both cases :func:`amplpy.Parameter.set_values()`.

.. code-block:: python

   cost = ampl.get_parameter("cost")
   cost.set_values({"BEEF": 5.01, "HAM": 4.55})
   print("Increased costs of beef and ham.")
   ampl.solve()
   print("New objective value:", totalcost.value())

The code above assigns the values 5.01 and 4.55 to the parameter cost for the objects beef and ham respectively.
If the order of the indexing of an entity is known (i.e. for multiple reassignment), it is not necessary to specify
both the index and the value. A collection of values is assigned to each of the parameter values, in the order they are represented in AMPL.

.. code-block:: python

   cost.set_values([3, 5, 5, 6, 1, 2, 5.01, 4.55])
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

To access all the numeric values contained in a Variable or any other entity, use a :class:`amplpy.DataFrame` object, which can be converted into other objects such as ``pandas.DataFrame`` using :func:`amplpy.DataFrame.to_pandas()`. Doing so, the data is detached from
the entity, and there is a considerable performance gain. To do so, we first get the Variable object from AMPL, then we get its data with the function :func:`amplpy.Entity.get_values()`.

.. code-block:: python

   # Get the values of the variable Buy in a pandas.DataFrame object
   buy = ampl.get_variable("Buy")
   df = buy.get_values().to_pandas()
   print(df)


Get arbitrary values via ampl expressions
-----------------------------------------

Often we are interested in very specific values coming out of the optimization session. To make use of the power of AMPL expressions and avoiding
cluttering up the environment by creating entities, fetching data through arbitrary AMPL expressions is possible. For this model, we are interested
in knowing how close each decision variable is to its upper bound, in percentage.
We can obtain this data into a dataframe using the function :func:`amplpy.AMPL.get_data()` with the code :

.. code-block:: python

  # Get the values of an expression into a pandas.DataFrame object
  df2 = ampl.get_data("{j in FOOD} 100*Buy[j]/Buy[j].ub").to_pandas()
  print(df2)

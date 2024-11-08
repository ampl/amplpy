.. _secExamplesPython:

Examples
========


Many Jupyter notebooks with examples are available on the `AMPL Model Colaboratory <https://colab.ampl.com/>`_
and the new book `Hands-On Mathematical Optimization with AMPL in Python 🐍 <https://ampl.com/mo-book/>`_.

You should also check out our collection of interactive `Streamlit Apps <https://ampl.com/streamlit>`_ and
learn how easy you can build your own apps.


.. grid:: 1 1 2 2
    :gutter: 1

    .. grid-item::

        .. grid:: 1 1 1 1
            :gutter: 1

            .. grid-item-card::

                `AMPL Model Colaboratory <https://ampl.com/colab/>`_ is a collection of AMPL models in Jupyter Notebooks that run on platforms such as Google Colab, Kaggle, Gradient, and AWS SageMaker.

                Available at: `ampl.com/colab <https://ampl.com/colab/>`_.

            .. grid-item-card::

                You can use the **Christmas notebook** written by `ChatGPT <https://chat.openai.com/>`_ to get started:

                .. image:: https://colab.research.google.com/assets/colab-badge.svg
                    :target: https://colab.research.google.com/github/ampl/colab.ampl.com/blob/master/authors/fdabrandao/chatgpt/christmas.ipynb
                    :alt: Open In Colab

                .. image:: https://kaggle.com/static/images/open-in-kaggle.svg
                    :target: https://kaggle.com/kernels/welcome?src=https://github.com/ampl/colab.ampl.com/blob/master/authors/fdabrandao/chatgpt/christmas.ipynb
                    :alt: Kaggle

                .. image:: https://assets.paperspace.io/img/gradient-badge.svg
                    :target: https://console.paperspace.com/github/ampl/colab.ampl.com/blob/master/authors/fdabrandao/chatgpt/christmas.ipynb
                    :alt: Gradient

                .. image:: https://studiolab.sagemaker.aws/studiolab.svg
                    :target: https://studiolab.sagemaker.aws/import/github/ampl/colab.ampl.com/blob/master/authors/fdabrandao/chatgpt/christmas.ipynb
                    :alt: Open In SageMaker Studio Lab

                | BTW: you can even ask `ChatGPT <https://chat.openai.com/>`_ to write models for you! If it makes mistakes you can ask for help in our new `Discourse Forum <https://discuss.ampl.com>`_!

    .. grid-item::

        .. grid:: 1 1 1 1
            :gutter: 1

            .. grid-item-card::

                The repository of notebooks `MO-BOOK: Hands-On Mathematical Optimization with AMPL in Python 🐍 <https://ampl.com/mo-book/>`_
                introduces the concepts and tools of mathematical optimization with examples from a range of disciplines.
                
                Available at: `ampl.com/mo-book <https://ampl.com/mo-book/>`_.

            .. grid-item-card::

                Build and share data apps quickly with Streamlit - no front-end experience necessary.

                Available at: `ampl.com/streamlit <https://ampl.com/streamlit/>`_.

                .. figure:: https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png
                    :alt: AMPL Optimization Apps on Streamlit Cloud
                    :target: https://ampl.com/streamlit/
 
Example files
=============

This section lists a few examples in Python.
These are the same files that can be found in the `amplpy Github repository <https://github.com/ampl/amplpy/tree/master/examples>`_, and show the basic usage of the Python API.

Example 1: First steps
----------------------

:download:`first_example.py <../../examples/first_example.py>`

This example shows how to

* read an AMPL model
* reassign values to parameters
* solve the model
* display the objective function value


Example 2: Get and set AMPL options
-----------------------------------

:download:`options_example.py <../../examples/options_example.py>`

This example shows how to:

* get and set AMPL options


Example 3: Assign all data to a model and solve it
--------------------------------------------------

:download:`diet_model.py <../../examples/diet_model.py>`

This example shows how to:

* Assign all the data necessary to generate a model instance programmatically

Example 4: Build an efficient frontier
--------------------------------------

:download:`efficient_frontier.py <../../examples/efficient_frontier.py>`

This example shows how to:

* build an efficient frontier by repeteatly solve a portfolio problem in AMPL


Example 5: Simple heuristic
---------------------------

:download:`tracking_model.py <../../examples/tracking_model.py>`

This example shows how to:

* Do a simple heuristics for solving a QMIP problem, using the relaxed solution as a hint

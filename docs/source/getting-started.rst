###############
Getting Started
###############

************
Requirements
************

Python 3.8.+

Optional Packages::

   pandas

* ``pandas`` is needed if you want to convert a QVD data table to a pandas DataFrame and vice versa. It is not a required dependency. See `pandas <https://pandas.pydata.org/>`_ for more information.

It is generally recommended to use
`python virtual environment <https://docs.python.org/3/tutorial/venv.html>`_ or
`conda virtual environment <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_.

************
Installation
************

PyQvd is a Python library available through `pypi <https://pypi.org/>`_. The recommended way to
install and maintain PyQvd as a dependency is through the package installer (PIP). Before
installing this library, download and install Python.

To use PyQvd, first install it using pip:

.. code-block:: console

   (.venv) $ pip install PyQvd

*****
Usage
*****

To use PyQvd in a project, import the module and create a ``QvdTable`` object. The ``QvdTable``
class is the primary interface for working with QVD files in PyQvd. It represents the parsed data
table from a QVD file and provides methods and properties to work with the data. A ``QvdTable`` can
be constructed in different ways, depending on the source of the data. The most common way is to
load a QVD file from disk:

.. code-block:: python

   from pyqvd import QvdTable

   tbl = QvdTable.from_qvd("path/to/file.qvd")
   print(tbl.head())

The above example loads the PyQvd library and parses an example QVD file. A QVD file is
typically loaded using the ``QvdTable.from_qvd`` function of the ``QvdTable`` class.
For more ways to load/construct ``QvdTable``'s see :doc:`api`. After loading the file's content,
numerous methods and properties are available to work with the parsed data.

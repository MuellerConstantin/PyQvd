############
Introduction
############

This user guide is intended to provide a comprehensive guide to the use of the
PyQvd library. The PyQvd library is a Python library that provides a simple
interface to the QVD file format. The QVD file format is a simple file format
that is used to store data in a columnar format. The QVD file format is used by
QlikView and later Qlik Sense, a popular business intelligence tool, to store data.

The PyQvd library provides a simple interface to read and write QVD files. The
library is designed to be easy to use and to provide a simple and intuitive
interface to the QVD file format.

*******
Reading
*******

The most common use case for the PyQvd library is to read data from a QVD file on
disk. To read data from a QVD file, you can use the static :func:`pyqvd.qvd.QvdTable.from_qvd`
method of the :class:`pyqvd.qvd.QvdTable` class. This method takes the path to the
QVD file as an argument and returns a :class:`pyqvd.qvd.QvdTable` object that
represents the data in the QVD file.

For example, to read data from a QVD file called `sample.qvd`, you can use the
following code:

.. code-block:: python

    from pyqvd import QvdTable

    tbl = QvdTable.from_qvd("data.qvd")

Next to reading a QVD file from disk, you can also read a QVD file from any file-like object
such as a binary stream. This can be done by using the :func:`pyqvd.qvd.QvdTable.from_stream`
method of the :class:`pyqvd.qvd.QvdTable` class. This method takes the file-like object
(``BinaryIO``) as an argument and returns a :class:`pyqvd.qvd.QvdTable` object that represents
the data in the QVD file.

For example, to read data from a QVD file stored in a S3 Object Storage, you could use the
following code:

.. code-block:: python

    import boto3
    from pyqvd import QvdTable

    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket="my-bucket", Key="sample.qvd")
    tbl = QvdTable.from_stream(obj["Body"])

Sometimes your QVD files may be very large and you may not want to load the entire file into
memory at once or at least you want to track the progress of the reading process. In this case,
you can use the :func:`pyqvd.qvd.QvdTable.from_qvd` or :func:`pyqvd.qvd.QvdTable.from_stream`
method with the optional argument ``chunk_size``. This argument specifies the number of rows that
are read from the QVD file at once. The default value is ``None`` which means that the entire file
is read at once.

When you specify a chunk size, the result of the :func:`pyqvd.qvd.QvdTable.from_qvd` or
:func:`pyqvd.qvd.QvdTable.from_stream` method is a iterator that yields :class:`pyqvd.qvd.QvdTable`
objects. Each :class:`pyqvd.qvd.QvdTable` object represents a chunk of the data in the QVD file.

.. code-block:: python

    import tqdm
    from pyqvd import QvdTable

    itr = QvdTable.from_qvd("data.qvd", chunk_size=1000)

    with tqdm.tqdm(total=len(itr)) as pbar:
        for tbl in itr:
            # Process the chunk
            pbar.update(1)

.. important::

    Especially for arbitrary ``BinaryIO`` objects, it is important to note that not every stream
    implementation is seekable. The iteration process requires the ability to seek to any position
    in the stream. If the stream is not seekable, the iteration process will fail.

*****************
Data Manipulation
*****************

After reading/constructing a QVD table, you can perform various operations on the data. The
:class:`pyqvd.qvd.QvdTable` class provides a number of methods to help you analyze and
manipulate the data in the QVD table. The following examples can only give you a brief
overview of the possibilities. For a complete overview of the available methods, please refer
to the :ref:`api` documentation.

Retrevieve and Edit
===================

First of all, you can retrieve and edit the existing data in the QVD table. For example,
you can retrieve single values or slices of the data using the :func:`pyqvd.qvd.QvdTable.get`
method. Instead of using the :func:`pyqvd.qvd.QvdTable.get` method, you can also use the
shorthand notation, the square brackets, to retrieve single values or slices of the data.

.. code-block:: python

    # Retrieve the value at row 0 and column 'A'
    value = tbl.get((0, "A"))

    # Retrieve the value at row 0 and column 'A' using the shorthand notation
    value = tbl[0, "A"]

    # Retrieve the second row
    row = tbl.get(1)

    # Retrieve the second row using the shorthand notation
    row = tbl[1]

For editing the data, you can use the :func:`pyqvd.qvd.QvdTable.set` method. This method allows
you to modify individual cells, rows, or columns in the QVD table. The :func:`pyqvd.qvd.QvdTable.set`
has also a shorthand notation available like the :func:`pyqvd.qvd.QvdTable.get` method.

.. note:: You can use symbols (``QvdValue`` objects) as well as native Python values to update the data.
    Native values will be converted to ``QvdValue`` objects automatically. Unsupported native types
    are automatically converted to strings (``StringValue``).

.. code-block:: python

    # Update the value at row 0 and column 'A'
    tbl.set((0, "A"), 42)

    # Update the value at row 0 and column 'A' using a symbol
    tbl.set((0, "A"), IntegerValue(42))

    # Update the value at row 0 and column 'A' using the shorthand notation
    tbl[0, "A"] = 42

    # Replace the second row
    tbl.set(1, [1, 2, 3, 4, 5])

    # Replace the second row using the shorthand notation
    tbl[1] = [1, 2, 3, 4, 5]

Add and Remove
==============

In addition you can also add new rows or columns to the QVD table or remove existing rows
or columns if needed. For example, to add a new row to the QVD table, you can use the
:func:`pyqvd.qvd.QvdTable.append` or :func:`pyqvd.qvd.QvdTable.insert` method. The
:func:`pyqvd.qvd.QvdTable.drop` method can be used to remove rows or columns from the
QVD table again.

.. note:: You can use symbols (``QvdValue`` objects) as well as native Python values to add new data.
    Native values will be converted to ``QvdValue`` objects automatically. Unsupported native types
    are automatically converted to strings (``StringValue``).

.. code-block:: python

    # Add a new row to the QVD table
    tbl.append([1, 2, 3, 4, 5])

    # Add a new row to the QVD table using symbols
    tbl.append([IntegerValue(1), IntegerValue(2), IntegerValue(3), IntegerValue(4), IntegerValue(5)])

    # Insert a new row at index 0
    tbl.insert(0, [1, 2, 3, 4, 5])

    # Remove the second row from the QVD table
    tbl.drop(1)

    # Remove the column 'A' from the QVD table
    tbl.drop("A", axis="columns")

Filtering and Sorting
=====================

The :class:`pyqvd.qvd.QvdTable` class also supports basic filtering and sorting operations.
Therefor, the class provides the :func:`pyqvd.qvd.QvdTable.filter_by` and
:func:`pyqvd.qvd.QvdTable.sort_by` methods to filter and sort the data based on the values
of individual columns.

.. code-block:: python

    # Filter the data based on the values in the column 'A'
    new_tbl = tbl.filter_by("A", lambda value: value.calculation_value > 0)

    # Sort the data based on the values in the column 'A'
    new_tbl = tbl.sort_by("A", ascending=False)

    # Sorting is also possible by using a custom comparator
    new_tbl = tbl.sort_by("A", comparator=lambda x, y: 1 if x.calculation_value > y.calculation_value else -1 if x.calculation_value < y.calculation_value else 0)

Concatenate and Join
====================

The :class:`pyqvd.qvd.QvdTable` class also supports concatenation and joining of multiple
QVD tables. The :func:`pyqvd.qvd.QvdTable.concat` method can be used to concatenate multiple
QVD tables along the rows. The :func:`pyqvd.qvd.QvdTable.join` method can be used to join
multiple QVD tables along the columns.

The join method supports four different types of joins: inner, left, right, and outer. The
default join type is the outer join. The join method also supports the specification of the
join columns and the suffixes for the columns that are present in both tables.

.. code-block:: python

    # Concatenate two QVD tables
    new_tbl = tbl.concat(tbl2)

    # Join two QVD tables
    new_tbl = tbl.join(tbl2, on="A", how="inner", lsuffix="_left", rsuffix="_right")

    # Join two QVD tables using multiple columns
    new_tbl = tbl.join(tbl2, on=["A", "B"], how="left", lsuffix="_left", rsuffix="_right")

Import and Export
=================

Instead of reading the data from a QVD file, you can also import data from other in-memory sources
such as a dictionary or a pandas DataFrame. This can be done by using the respective methods like
:func:`pyqvd.qvd.QvdTable.from_dict` or :func:`pyqvd.qvd.QvdTable.from_pandas`. For more information,
please refer to the :ref:`api` documentation.

.. note:: Native Python types are automatically converted to symbols (``QvdValue`` objects) and
    vice versa. Unsupported native types are automatically converted to strings (``StringValue``).

For example, to import a pandas DataFrame into a QVD table, you can use the following code:

.. code-block:: python

    import pandas as pd
    from pyqvd import QvdTable

    df = pd.read_csv("data.csv")
    tbl = QvdTable.from_pandas(df)

Of course, you can also export the data in the QVD table to other in-memory data structures such.
This can be done by using the respective methods like :func:`pyqvd.qvd.QvdTable.to_dict` or
:func:`pyqvd.qvd.QvdTable.to_pandas`.

For example, to export the data in the QVD table to a pandas DataFrame, you can use the following code:

.. code-block:: python

    df = tbl.to_pandas()

*******
Writing
*******

After analyzing and manipulating the data in the QVD table, you can write the data back to a QVD
file on disk. To write the data to a QVD file, you can use the :func:`pyqvd.qvd.QvdTable.to_qvd`
method of the :class:`pyqvd.qvd.QvdTable` class. This method takes the path to the QVD file as an
argument and writes the data in the QVD table to the specified file.

For example, to write the data in the QVD table to a QVD file called `output.qvd`, you can use the
following code:

.. code-block:: python

    tbl.to_qvd("output.qvd")

As with reading, the QVD table or the resulting QVD file can also be written to any binary
stream instead of to the hard drive. This can be done by using the :func:`pyqvd.qvd.QvdTable.to_stream`
method of the :class:`pyqvd.qvd.QvdTable` class. This method takes the file-like object
(``BinaryIO``) as an argument and writes the data in the QVD table to the specified stream.

For example, to write the data in the QVD table to a binary buffer and then upload the buffer to a
S3 Object Storage, you could use the following code:

.. code-block:: python

    import boto3
    from pyqvd import QvdTable

    ...

    buffer = io.BytesIO()
    tbl.to_stream(buffer)

    s3 = boto3.client("s3")
    obj = s3.put_object(Bucket="my-bucket", Key="output.qvd", Body=buffer.getvalue())

By default, opinionated settings are used when writing the QVD file. However, you can also specify
custom settings when writing the QVD file. For example, you can specify the table's name or the
format that is used to write the data to the QVD file. Therefore you can use the writer's options
class :class:`pyqvd.io.QvdFileWriterOptions` to specify the custom settings and so called formatters
to format the data.

.. code-block:: python

    from pyqvd.io import QvdFileWriterOptions, DateValueFormatter

    date_formatter = DateValueFormatter("DD.MM.YYYY")
    options = QvdFileWriterOptions(table_name="my-table", date_formatter=date_formatter)

    tbl.to_qvd("output.qvd", options)

For a complete list of available options and formatters, as well as information about the supported
format strings, please refer to the :ref:`api` documentation.

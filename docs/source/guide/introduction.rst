Introduction
============

This user guide is intended to provide a comprehensive guide to the use of the
PyQvd library. The PyQvd library is a Python library that provides a simple
interface to the QVD file format. The QVD file format is a simple file format
that is used to store data in a columnar format. The QVD file format is used by
QlikView and later Qlik Sense, a popular business intelligence tool, to store data.

The PyQvd library provides a simple interface to read and write QVD files. The
library is designed to be easy to use and to provide a simple and intuitive
interface to the QVD file format.

Reading
-------

The most common use case for the PyQvd library is to read data from a QVD file on
disk. To read data from a QVD file, you can use the static :func:`pyqvd.qvd.QvdTable.from_qvd`
method of the :class:`pyqvd.qvd.QvdTable` class. This method takes the path to the
QVD file as an argument and returns a :class:`pyqvd.qvd.QvdTable` object that
represents the data in the QVD file.

For example, to read data from a QVD file called `sample.qvd`, you can use the
following code:

.. code-block:: python

    from pyqvd import QvdTable

    tbl = QvdTable.from_qvd('data.qvd')

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

    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket='my-bucket', Key='sample.qvd')
    tbl = QvdTable.from_stream(obj['Body'])

In addition to reading data from a QVD file, you can also create a new QVD table from scratch using
an in-memory data source such as a dictionary or a pandas DataFrame. This can be done by using the
:func:`pyqvd.qvd.QvdTable.from_dict` for example. For more information, please refer to the
:ref:`api` documentation.

Analysis
--------

After reading/constructing a QVD table, you can perform various operations on the data. The
:class:`pyqvd.qvd.QvdTable` class provides a number of methods to help you analyze and
manipulate the data in the QVD table. The following examples can only give you a brief
overview of the possibilities. For a complete overview of the available methods, please refer
to the :ref:`api` documentation.

For example, you can retrieve single values or slices of the data using the :func:`pyqvd.qvd.QvdTable.get`
method. Instead of using the :func:`pyqvd.qvd.QvdTable.get` method, you can also use the shorthand
notation, the square brackets, to retrieve single values or slices of the data.

.. code-block:: python

    # Retrieve the value at row 0 and column 'A'
    value = tbl.get((0, 'A'))

    # Retrieve the value at row 0 and column 'A' using the shorthand notation
    value = tbl[0, 'A']

    # Retrieve the second row
    row = tbl.get(1)

    # Retrieve the second row using the shorthand notation
    row = tbl[1]

Of course, it is also possible to modify the data in the QVD table. For example, you can add
new rows to the QVD table or update existing rows and cells using the :func:`pyqvd.qvd.QvdTable.set`
method. There is also a shorthand notation available to update a single cell in the QVD table.

.. code-block:: python

    # Update the value at row 0 and column 'A'
    tbl.set((0, 'A'), 42)

    # Update the value at row 0 and column 'A' using the shorthand notation
    tbl[0, 'A'] = 42

    # Replace the second row
    tbl.set(1, [1, 2, 3, 4, 5])

    # Replace the second row using the shorthand notation
    tbl[1] = [1, 2, 3, 4, 5]

Writing
-------

After analyzing and manipulating the data in the QVD table, you can write the data back to a QVD
file on disk. To write the data to a QVD file, you can use the :func:`pyqvd.qvd.QvdTable.to_qvd`
method of the :class:`pyqvd.qvd.QvdTable` class. This method takes the path to the QVD file as an
argument and writes the data in the QVD table to the specified file.

For example, to write the data in the QVD table to a QVD file called `output.qvd`, you can use the
following code:

.. code-block:: python

    tbl.to_qvd('output.qvd')

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

    s3 = boto3.client('s3')
    obj = s3.put_object(Bucket='my-bucket', Key='output.qvd', Body=buffer.getvalue())

Instead of persisting the data to a QVD file, you can also convert the QVD table to another
in-memory data structure such as a dictionary or a pandas DataFrame. This can be done by using the
:func:`pyqvd.qvd.QvdTable.to_dict` or :func:`pyqvd.qvd.QvdTable.to_pandas` method respectively.

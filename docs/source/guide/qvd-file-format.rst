QVD File Format
===============

The *Qlik View Data (QVD)* file format is a binary file format that is used by QlikView, and
later Qlik Sense, to store data. The format is proprietary and contains one data table per file.
However, the format is well structured and can be parsed without the need of a QlikView/Qlik Sense
installation using this library. In fact, a QVD file consists of three parts: a XML header, and two
binary parts, the symbol and the index table. The XML header contains meta information about the
data table stored in the QVD file, such as the number of data records and the names of the fields.
The symbol table contains the actual distinct values for each field and the index table contains the
actual data records, consisting of references to the symbol table.

XML Header
----------

The XML header contains meta information about the data table stored in the QVD file. The header is
always located at the beginning of the file and is in human readable text format, XML. The header
contains information about the number of data records, the names of the fields, and the data types
of the fields. In addition, the header parsing instructions for the symbol and index table, like
the offset and length. The complete header is written in UTF-8 encoded XML and is separated from the
binary part of the file by a carriage return and line feed (CRLF) sequence followed by a null byte.

Symbol Table
------------

The symbol table contains the actual distinct values for each field. The symbol table is a binary
table that is stored in the QVD file after the XML header. The symbol table is stored in a column-major
format, meaning that the values of each field are stored in a contiguous block of memory.

In general, QlikView/Qlik Sense can handle multiple data types, such as text strings, numbers, dates,
times, timestamps, and currencies. But on memory level, a QVD file knows only the following five
different data types. The data types stored in the QVD file are interpreted by the QlikView/Qlik Sense
application when loading the data with the help of additional meta information stored in the XML header.
This allows to store a date for example as a plain number in the QVD file, but to interpret it as a date
when loading the data into QlikView/Qlik Sense.

+--------------+------+-----------------------------------------------------------------------------------------------+
| Type         | Code | Description                                                                                   |
+==============+======+===============================================================================================+
| Integer      | 0x01 | signed 4-byte integer (little endian)                                                         |
+--------------+------+-----------------------------------------------------------------------------------------------+
| Double       | 0x02 | signed 8-byte IEEE floating point number (little endian)                                      |
+--------------+------+-----------------------------------------------------------------------------------------------+
| String       | 0x04 | null terminated string                                                                        |
+--------------+------+-----------------------------------------------------------------------------------------------+
| Dual Integer | 0x05 | signed 4-byte integer (little endian) followed by a null terminated string                    |
+--------------+------+-----------------------------------------------------------------------------------------------+
| Dual Double  | 0x06 | signed 8-byte IEEE floating point number (little endian) followed by a null terminated string |
+--------------+------+-----------------------------------------------------------------------------------------------+

Basically, the symbol table is a memory block that contains the distinct values of each field. The order
of the fields in the symbol table is the same as in the XML header. Each single value is prefixed with
a type byte that indicates the data type of the value itself.

Index Table
-----------

The index table contains the actual data records, consisting of references to the symbol table. This means
that the index table does not contain the actual cell values, but a reference to the cell's value in the
symbol table. The index table is a binary table that is stored in the QVD file after the symbol table.
It is stored in a row-major format, meaning that the values of each record are stored in a contiguous block
of memory. To save memory, the indices of a record are stored with a bit mask instead of whole bytes per index.
Meta information about the bit mask is stored in the XML header.

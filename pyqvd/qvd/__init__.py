"""
Module contains the core classes and functions for dealing with QVD files. The main class is the
:class:`QvdTable` class, which represents a the internal data table of a QVD file.
"""

from pyqvd.qvd.header import NumberFormat, QvdFieldHeader, LineageInfo, QvdTableHeader
from pyqvd.qvd.values import (QvdValue, IntegerValue, DoubleValue, StringValue, DualIntegerValue,
                              DualDoubleValue)
from pyqvd.qvd.logical import TimeValue, DateValue, TimestampValue, IntervalValue, MoneyValue
from pyqvd.qvd.table import QvdTable

# The classes are split across submodules for readability only. Their module stays pyqvd.qvd, so
# that pickled objects remain loadable by earlier versions and the documented type paths are stable.
for _cls in (NumberFormat, QvdFieldHeader, LineageInfo, QvdTableHeader, QvdValue, IntegerValue,
             DoubleValue, StringValue, DualIntegerValue, DualDoubleValue, TimeValue, DateValue,
             TimestampValue, IntervalValue, MoneyValue, QvdTable):
    _cls.__module__ = __name__
del _cls

"""
This module contains the classes and functions for reading and writing QVD files. QVD files can be read
and written to/from any arbitrary stream-like target using the :class:`pyqvd.io.QvdFileReader` and
:class:`pyqvd.io.QvdFileWriter` classes respectively.
"""

from .reader import QvdFileReader
from .writer import QvdFileWriter

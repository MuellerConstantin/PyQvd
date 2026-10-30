"""
Module contains the data classes describing the XML header of a QVD file.
"""

from typing import List
from dataclasses import dataclass

@dataclass
class NumberFormat:
    """
    Represents the number format of a field in a QVD file.
    """
    type: str = "UNKNOWN"
    n_dec: int = 0
    use_thou: int = 0
    fmt: str = None
    dec: str = None
    thou: str = None

@dataclass
class QvdFieldHeader:
    """
    Metadata description of a field in a QVD file.
    """
    field_name: str = ""
    bit_offset: int = 0
    bit_width: int = 0
    bias: int = 0
    number_format: NumberFormat = None
    no_of_symbols: int = 0
    offset: int = 0
    length: int = 0
    comment: str = ""
    tags: List[str] = None

@dataclass
class LineageInfo:
    """
    Represents lineage information in a QVD file.
    """
    discriminator: str = ""
    statement: str = ""

@dataclass
class QvdTableHeader:
    """
    Structure of the header of a QVD file.
    """
    qv_build_no: int = 0
    creator_doc: str = ""
    create_utc_time: str = ""
    source_create_utc_time: str = ""
    source_file_utc_time: str = ""
    stale_utc_time: str = ""
    table_name: str = ""
    source_file_size: int = 0
    fields: List[QvdFieldHeader] = None
    compression: str = ""
    record_byte_size: int = 0
    no_of_records: int = 0
    no_of_fields: int = 0
    offset: int = 0
    length: int = 0
    comment: str = ""
    lineage: List[LineageInfo] = None

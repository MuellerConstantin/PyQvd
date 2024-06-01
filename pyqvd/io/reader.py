"""
Module for reading QVD files into memory. Contains the required logic to parse the binary data of a QVD file.
"""

import struct
import io
from typing import Union, List, BinaryIO
import xml.etree.ElementTree as ET
from pyqvd.qvd import (QvdTable, QvdValue, IntegerValue, DoubleValue, StringValue,
                       DualIntegerValue, DualDoubleValue, QvdTableHeader, QvdFieldHeader,
                       NumberFormat, LineageInfo, TimeValue, DateValue, TimestampValue,
                       IntervalValue)

class QvdFileReader:
    """
    Class for reading QVD files into memory. Parses the binary data of a QVD file and converts it into a
    :class:`.QvdTable` object.
    """
    def __init__(self, source: Union[str, BinaryIO]):
        """
        Constructs a new QVD file parser. The source can be either a file path or a BinaryIO object.

        :param source: The source to the QVD file.
        """
        self._source: Union[str, BinaryIO] = source
        self._buffer: bytes = None
        self._header: QvdTableHeader = None
        self._symbol_table: List[List[QvdValue]] = None
        self._index_table: List[List[int]] = None
        self._header_offset: int = None
        self._symbol_table_offset: int = None
        self._index_table_offset: int = None

    def _read_data(self):
        """
        Reads the data of the QVD file into memory.
        """
        if isinstance(self._source, str):
            with open(self._source, "rb") as file:
                self._buffer = file.read()
        elif isinstance(self._source, (io.RawIOBase, io.BufferedIOBase)):
            self._buffer = self._source.read()
        else:
            raise ValueError("Unsupported source type. Please provide either a file path or a BinaryIO object.")

    def _parse_header(self):
        """
        Parses the header of the QVD file.
        """
        # pylint: disable-next=invalid-name
        HEADER_DELIMITER = "\r\n\0"

        header_begin_index: int = 0
        header_delimiter_index: int = self._buffer.find(str.encode(HEADER_DELIMITER), header_begin_index)

        if header_delimiter_index == -1:
            raise ValueError("The XML header section does not exist or is not properly delimited from the binary data.")

        header_end_index: int = header_delimiter_index + len(HEADER_DELIMITER)
        header_buffer: bytes = self._buffer[header_begin_index:header_end_index].decode()

        header_xml: str = ET.fromstring(header_buffer[:-1])

        self._header = QvdTableHeader()
        self._header.qv_build_no = int(header_xml.find("QvBuildNo").text, 10)
        self._header.creator_doc = header_xml.find("CreatorDoc").text
        self._header.create_utc_time = header_xml.find("CreateUtcTime").text
        self._header.source_create_utc_time = header_xml.find("SourceCreateUtcTime").text
        self._header.source_file_utc_time = header_xml.find("SourceFileUtcTime").text
        self._header.stale_utc_time = header_xml.find("StaleUtcTime").text
        self._header.table_name = header_xml.find("TableName").text
        self._header.source_file_size = int(header_xml.find("SourceFileSize").text, 10)

        self._header.fields = []

        for field_xml in header_xml.find("Fields"):
            field = QvdFieldHeader()
            field.field_name = field_xml.find("FieldName").text
            field.bit_offset = int(field_xml.find("BitOffset").text, 10)
            field.bit_width = int(field_xml.find("BitWidth").text, 10)
            field.bias = int(field_xml.find("Bias").text, 10)

            number_format_xml = field_xml.find("NumberFormat")
            field.number_format = NumberFormat()
            field.number_format.type = number_format_xml.find("Type").text
            field.number_format.n_dec = int(number_format_xml.find("nDec").text, 10)
            field.number_format.use_thou = int(number_format_xml.find("UseThou").text, 10)
            field.number_format.fmt = number_format_xml.find("Fmt").text
            field.number_format.dec = number_format_xml.find("Dec").text
            field.number_format.thou = number_format_xml.find("Thou").text

            field.no_of_symbols = int(field_xml.find("NoOfSymbols").text, 10)
            field.offset = int(field_xml.find("Offset").text, 10)
            field.length = int(field_xml.find("Length").text, 10)
            field.comment = field_xml.find("Comment").text
            field.tags = [tag.text for tag in field_xml.find("Tags")]

            self._header.fields.append(field)

        self._header.compression = header_xml.find("Compression").text
        self._header.record_byte_size = int(header_xml.find("RecordByteSize").text, 10)
        self._header.no_of_records = int(header_xml.find("NoOfRecords").text, 10)
        self._header.offset = int(header_xml.find("Offset").text, 10)
        self._header.length = int(header_xml.find("Length").text, 10)
        self._header.comment = header_xml.find("Comment").text

        self._header.lineage = []

        for lineage_xml in header_xml.find("Lineage"):
            lineage = LineageInfo()
            lineage.discriminator = lineage_xml.find("Discriminator").text
            lineage.statement = lineage_xml.find("Statement").text

            self._header.lineage.append(lineage)

        self._header_offset = header_begin_index
        self._symbol_table_offset = header_end_index
        self._index_table_offset = self._symbol_table_offset + self._header.offset

    def _parse_symbol_table(self):
        """
        Parses the symbol table of the QVD file.
        """
        self._symbol_table = [None] * len(self._header.fields)
        symbol_buffer: bytes = self._buffer[self._symbol_table_offset:self._index_table_offset]

        for field_index, field in enumerate(self._header.fields):
            symbols: List[QvdValue] = []
            pointer = field.offset

            while pointer < field.offset + field.length:
                symbol_type = symbol_buffer[pointer]
                pointer += 1

                if symbol_type == 1:
                    byte_data = symbol_buffer[pointer:pointer + 4]
                    value = int.from_bytes(byte_data, byteorder="little", signed=True)
                    pointer += 4
                    symbols.append(IntegerValue(value))
                elif symbol_type == 2:
                    byte_data = symbol_buffer[pointer:pointer + 8]
                    value = struct.unpack("<d", byte_data)[0]
                    pointer += 8
                    symbols.append(DoubleValue(value))
                elif symbol_type == 4:
                    byte_data = bytearray()

                    while symbol_buffer[pointer] != 0:
                        byte_data.append(symbol_buffer[pointer])
                        pointer += 1

                    value = byte_data.decode(encoding="utf-8")
                    pointer += 1
                    symbols.append(StringValue(value))
                elif symbol_type == 5:
                    int_byte_data = symbol_buffer[pointer:pointer + 4]
                    int_value = int.from_bytes(int_byte_data, byteorder="little", signed=True)
                    pointer += 4

                    string_byte_data = bytearray()
                    while symbol_buffer[pointer] != 0:
                        string_byte_data.append(symbol_buffer[pointer])
                        pointer += 1

                    string_value = string_byte_data.decode(encoding="utf-8")
                    pointer += 1

                    if field.number_format.type == "DATE":
                        symbols.append(DateValue(int_value, string_value))
                    else:
                        symbols.append(DualIntegerValue(int_value, string_value))
                elif symbol_type == 6:
                    double_byte_data = symbol_buffer[pointer:pointer + 8]
                    double_value = struct.unpack("<d", double_byte_data)[0]
                    pointer += 8

                    string_byte_data = bytearray()
                    while symbol_buffer[pointer] != 0:
                        string_byte_data.append(symbol_buffer[pointer])
                        pointer += 1

                    string_value = string_byte_data.decode(encoding="utf-8")
                    pointer += 1

                    if field.number_format.type == "TIMESTAMP":
                        symbols.append(TimestampValue(double_value, string_value))
                    elif field.number_format.type == "TIME":
                        symbols.append(TimeValue(double_value, string_value))
                    elif field.number_format.type == "INTERVAL":
                        symbols.append(IntervalValue(double_value, string_value))
                    else:
                        symbols.append(DualDoubleValue(double_value, string_value))
                else:
                    raise ValueError("The symbol type byte is not recognized. Unknown data type: " + hex(symbol_type))

            self._symbol_table[field_index] = symbols

    def _parse_index_table(self):
        """
        Parses the index table of the QVD file.
        """
        self._index_table = []
        index_buffer: bytes = self._buffer[self._index_table_offset:self._index_table_offset + self._header.length + 1]

        pointer = 0

        while pointer < len(index_buffer):
            record_buffer = index_buffer[pointer:pointer + self._header.record_byte_size]
            record_buffer = record_buffer[::-1]
            record_buffer = struct.unpack("<" + "B" * len(record_buffer), record_buffer)

            mask = "".join(format(byte, "08b") for byte in record_buffer)
            mask = mask[::-1]
            mask = [int(bit) for bit in mask]

            record_indices = []

            for field in self._header.fields:
                if field.bit_width == 0:
                    symbol_index = 0
                else:
                    symbol_index = QvdFileReader._convert_bits_to_int32(
                        mask[field.bit_offset:field.bit_offset + field.bit_width])

                symbol_index += field.bias
                record_indices.append(symbol_index)

            self._index_table.append(record_indices)
            pointer += self._header.record_byte_size

    def read(self) -> QvdTable:
        """
        Reads the QVD file and returns its data as a :class:`.QvdTable` object.

        :return: The data table.
        """
        self._read_data()
        self._parse_header()
        self._parse_symbol_table()
        self._parse_index_table()

        def _get_record(index: int) -> List[QvdValue]:
            if index < 0 or index >= len(self._index_table):
                raise IndexError("Index out of range.")

            record = [None] * len(self._index_table[index])

            for field_index, symbol_index in enumerate(self._index_table[index]):
                if symbol_index < 0:
                    record[field_index] = None
                else:
                    record[field_index] = self._symbol_table[field_index][symbol_index]

            return record

        data = [_get_record(index) for index in range(len(self._index_table))]
        columns = [field.field_name for field in self._header.fields]

        return QvdTable(data, columns)

    @staticmethod
    def _convert_bits_to_int32(bits: List[int]) -> int:
        """
        Converts a list of bits to an integer.

        :param bits: The list of bits.
        :return: The integer value.
        """
        if len(bits) == 0:
            return 0

        return sum(bit * (2 ** index) for index, bit in enumerate(bits))

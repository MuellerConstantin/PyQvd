"""
Module for reading QVD files into memory. Contains the required logic to parse the binary data of a QVD file.
"""

import math
import struct
import io
from collections.abc import Iterator
from typing import Union, List, BinaryIO
import xml.etree.ElementTree as ET
from pyqvd.qvd import (QvdTable, QvdValue, IntegerValue, DoubleValue, StringValue,
                       DualIntegerValue, DualDoubleValue, QvdTableHeader, QvdFieldHeader,
                       NumberFormat, LineageInfo, TimeValue, DateValue, TimestampValue,
                       IntervalValue, MoneyValue)

class QvdFileReaderIterator(Iterator):
    """
    Iterator class for reading QVD files into memory. Parses the binary data of a QVD file and
    converts it into a :class:`.QvdTable` object.
    """
    def __init__(self, reader: "QvdFileReader", chunk_size: int):
        """
        Constructs a new QVD file parser iterator.

        :param reader: The QVD file reader.
        :param chunk_size: The size of the chunks to read as number of records.
        """
        self._reader = reader
        self._chunk_size = chunk_size
        self._current_chunk = 0

    def __next__(self):
        # pylint: disable-next=protected-access
        if self._current_chunk * self._chunk_size >= self._reader._header.no_of_records:
            # pylint: disable-next=protected-access
            self._reader._stream.close()
            raise StopIteration

        # pylint: disable-next=protected-access
        chunk = self._reader._parse_index_table_chunk(self._current_chunk * self._chunk_size, self._chunk_size)
        self._current_chunk += 1

        # pylint: disable-next=protected-access
        data = [self._reader._decode_record(record) for record in chunk]
        # pylint: disable-next=protected-access
        columns = [field.field_name for field in self._reader._header.fields]

        return QvdTable(data, columns)

    def __len__(self):
        return math.ceil(self._reader._header.no_of_records / self._chunk_size)

class QvdFileReader:
    """
    Class for reading QVD files into memory. Parses the binary data of a QVD file and converts it into a
    :class:`.QvdTable` object.

    :param source: The source to the QVD file. Either a file path or a BinaryIO object.
    :param chunk_size: Optional chunk size if the data should be read in chunks. The chunk size is
        given as number of records.
    """
    def __init__(self, source: Union[str, BinaryIO], chunk_size: int = None):
        """
        Constructs a new QVD file parser. The source can be either a file path or a BinaryIO object.

        :param source: The source to the QVD file.
        """
        self._source: Union[str, BinaryIO] = source
        self._stream: BinaryIO = None
        self._chunk_size: int = chunk_size
        self._symbol_table_offset: int = None
        self._index_table_offset: int = None

        self._header_buffer: bytes = None
        self._header: QvdTableHeader = None
        self._symbol_table_buffer: bytes = None
        self._symbol_table: List[List[QvdValue]] = None
        self._index_table_buffer: bytes = None
        self._index_table: List[List[int]] = None

    def _read_header_data(self):
        """
        Reads the header data of the QVD file into memory.
        """
        # pylint: disable-next=invalid-name
        HEADER_DELIMITER = "\r\n\0"

        buffer = b""

        self._stream.seek(0)

        while True:
            block = self._stream.read(512)

            if not block:
                break

            buffer += block

            pos = buffer.find(str.encode(HEADER_DELIMITER))

            if pos != -1:
                buffer = buffer[:pos + len(HEADER_DELIMITER)]
                break

        if not buffer or buffer.find(str.encode(HEADER_DELIMITER)) == -1:
            raise ValueError("The XML header section does not exist or is not properly delimited from the binary data.")

        self._header_buffer = buffer
        self._symbol_table_offset = len(buffer)

    def _parse_header(self):
        """
        Parses the header of the QVD file.
        """
        self._read_header_data()

        header_xml: str = ET.fromstring(self._header_buffer.decode()[:-1])

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

        self._index_table_offset = self._symbol_table_offset + self._header.offset

    def _read_symbol_table_data(self):
        """
        Reads the symbol table data of the QVD file into memory.
        """
        self._stream.seek(self._symbol_table_offset)
        self._symbol_table_buffer = self._stream.read(self._header.offset)

    def _parse_symbol_table(self):
        """
        Parses the symbol table of the QVD file.
        """
        self._read_symbol_table_data()

        self._symbol_table = [None] * len(self._header.fields)

        for field_index, field in enumerate(self._header.fields):
            symbols: List[QvdValue] = []
            pointer = field.offset

            while pointer < field.offset + field.length:
                symbol_type = self._symbol_table_buffer[pointer]
                pointer += 1

                if symbol_type == 1:
                    byte_data = self._symbol_table_buffer[pointer:pointer + 4]
                    value = int.from_bytes(byte_data, byteorder="little", signed=True)
                    pointer += 4
                    symbols.append(IntegerValue(value))
                elif symbol_type == 2:
                    byte_data = self._symbol_table_buffer[pointer:pointer + 8]
                    value = struct.unpack("<d", byte_data)[0]
                    pointer += 8
                    symbols.append(DoubleValue(value))
                elif symbol_type == 4:
                    byte_data = bytearray()

                    while self._symbol_table_buffer[pointer] != 0:
                        byte_data.append(self._symbol_table_buffer[pointer])
                        pointer += 1

                    value = byte_data.decode(encoding="utf-8")
                    pointer += 1
                    symbols.append(StringValue(value))
                elif symbol_type == 5:
                    int_byte_data = self._symbol_table_buffer[pointer:pointer + 4]
                    int_value = int.from_bytes(int_byte_data, byteorder="little", signed=True)
                    pointer += 4

                    string_byte_data = bytearray()
                    while self._symbol_table_buffer[pointer] != 0:
                        string_byte_data.append(self._symbol_table_buffer[pointer])
                        pointer += 1

                    string_value = string_byte_data.decode(encoding="utf-8")
                    pointer += 1

                    if field.number_format.type == "DATE":
                        symbols.append(DateValue(int_value, string_value))
                    elif field.number_format.type == "MONEY":
                        symbols.append(MoneyValue(int_value, string_value))
                    else:
                        symbols.append(DualIntegerValue(int_value, string_value))
                elif symbol_type == 6:
                    double_byte_data = self._symbol_table_buffer[pointer:pointer + 8]
                    double_value = struct.unpack("<d", double_byte_data)[0]
                    pointer += 8

                    string_byte_data = bytearray()
                    while self._symbol_table_buffer[pointer] != 0:
                        string_byte_data.append(self._symbol_table_buffer[pointer])
                        pointer += 1

                    string_value = string_byte_data.decode(encoding="utf-8")
                    pointer += 1

                    if field.number_format.type == "TIMESTAMP":
                        symbols.append(TimestampValue(double_value, string_value))
                    elif field.number_format.type == "TIME":
                        symbols.append(TimeValue(double_value, string_value))
                    elif field.number_format.type == "INTERVAL":
                        symbols.append(IntervalValue(double_value, string_value))
                    elif field.number_format.type == "MONEY":
                        symbols.append(MoneyValue(double_value, string_value))
                    else:
                        symbols.append(DualDoubleValue(double_value, string_value))
                else:
                    raise ValueError("The symbol type byte is not recognized. Unknown data type: " + hex(symbol_type))

            self._symbol_table[field_index] = symbols

    def _read_index_table_data(self):
        """
        Reads the index table data of the QVD file into memory.
        """
        self._stream.seek(self._index_table_offset)
        self._index_table_buffer = self._stream.read(self._header.length + 1)

    def _parse_index_table(self):
        """
        Parses the index table of the QVD file.
        """
        self._read_index_table_data()

        self._index_table = []

        pointer = 0

        while pointer < len(self._index_table_buffer):
            record_buffer = self._index_table_buffer[pointer:pointer + self._header.record_byte_size]
            record_buffer = record_buffer[::-1]
            record_buffer = struct.unpack("<" + "B" * len(record_buffer), record_buffer)

            mask = "".join(format(byte, "08b") for byte in record_buffer)
            mask = mask[::-1]

            record_indices = []

            for field in self._header.fields:
                if field.bit_width == 0:
                    symbol_index = 0
                else:
                    symbol_index = int(mask[field.bit_offset:field.bit_offset + field.bit_width][::-1], 2)

                symbol_index += field.bias
                record_indices.append(symbol_index)

            self._index_table.append(record_indices)
            pointer += self._header.record_byte_size

    def _read_index_table_chunk_data(self, chunk_offset: int, chunk_size: int) -> bytes:
        """
        Reads a chunk of the index table data of the QVD file into memory.

        :param chunk_offset: The offset of the chunk as number of records.
        :param chunk_size: The size of the chunk as number of records.
        :return: The chunk of the index table.
        """
        if chunk_offset < 0 or chunk_offset >= self._header.no_of_records or chunk_size < 0:
            raise ValueError("The chunk is out of range.")

        chunk_byte_offset = self._index_table_offset + chunk_offset * self._header.record_byte_size
        chunk_byte_size = chunk_size * self._header.record_byte_size

        self._stream.seek(chunk_byte_offset)

        return self._stream.read(chunk_byte_size)

    def _parse_index_table_chunk(self, chunk_offset: int, chunk_size: int) -> List[List[int]]:
        """
        Parses a chunk of the index table of the QVD file.

        :param chunk_offset: The offset of the chunk as number of records.
        :param chunk_size: The size of the chunk as number of records.
        :return: The chunk of the index table.
        """
        if chunk_offset < 0 or chunk_offset >= self._header.no_of_records or chunk_size < 0:
            raise ValueError("The chunk is out of range.")

        chunk: List[List[int]] = []
        chunk_buffer = self._read_index_table_chunk_data(chunk_offset, chunk_size)

        pointer = 0

        while pointer < len(chunk_buffer):
            record_buffer = chunk_buffer[pointer:pointer + self._header.record_byte_size]
            record_buffer = record_buffer[::-1]
            record_buffer = struct.unpack("<" + "B" * len(record_buffer), record_buffer)

            mask = "".join(format(byte, "08b") for byte in record_buffer)
            mask = mask[::-1]

            record_indices = []

            for field in self._header.fields:
                if field.bit_width == 0:
                    symbol_index = 0
                else:
                    symbol_index = int(mask[field.bit_offset:field.bit_offset + field.bit_width][::-1], 2)

                symbol_index += field.bias
                record_indices.append(symbol_index)

            chunk.append(record_indices)
            pointer += self._header.record_byte_size

        return chunk

    def _decode_record(self, record: List[int]) -> List[QvdValue]:
        """
        Decodes a record from the index table.
        """
        decoded_record = [None] * len(record)

        for field_index, symbol_index in enumerate(record):
            if symbol_index < 0:
                decoded_record[field_index] = None
            else:
                decoded_record[field_index] = self._symbol_table[field_index][symbol_index]

        return decoded_record

    def read(self) -> Union[QvdTable, Iterator[QvdTable]]:
        """
        Reads the QVD file and returns its data as a :class:`.QvdTable` object.

        :return: The data table of the QVD file or an iterator for reading the data in chunks.
        """
        if isinstance(self._source, str):
            self._stream = open(self._source, "rb")
        elif isinstance(self._source, (io.RawIOBase, io.BufferedIOBase)):
            self._stream = self._source
        else:
            raise ValueError("Unsupported source type. Please provide either a file path or a BinaryIO object.")

        self._parse_header()
        self._parse_symbol_table()

        if self._chunk_size is None:
            self._parse_index_table()

            self._stream.close()

            data = [self._decode_record(record) for record in self._index_table]
            columns = [field.field_name for field in self._header.fields]

            return QvdTable(data, columns)
        else:
            return QvdFileReaderIterator(self, self._chunk_size)

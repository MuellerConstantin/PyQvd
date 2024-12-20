"""
Module for writing QVD files to disk. Contains the required classes and functions to persist QVD files.
"""

import uuid
import time
import struct
import io
from typing import Union, List, Dict, BinaryIO
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pyqvd.qvd import (QvdTable, QvdValue, QvdFieldHeader, QvdTableHeader, NumberFormat,
                       IntegerValue, DoubleValue, StringValue, DualIntegerValue, DualDoubleValue,
                       TimeValue, DateValue, TimestampValue, IntervalValue, MoneyValue)
from pyqvd.io.format import (TimeValueFormatter, DateValueFormatter, IntervalValueFormatter,
                             TimestampValueFormatter, MoneyValueFormatter)

@dataclass
class QvdFileWriterOptions:
    """
    Class for storing options for the QVD file writer.
    """
    table_name: str = "UNKNOWN"
    time_formatter: TimeValueFormatter = TimeValueFormatter("hh:mm:ss")
    date_formatter: DateValueFormatter = DateValueFormatter("YYYY-MM-DD")
    timestamp_formatter: TimestampValueFormatter = TimestampValueFormatter("YYYY-MM-DD hh:mm:ss[.fff]")
    interval_formatter: IntervalValueFormatter = IntervalValueFormatter("D hh:mm:ss")
    money_formatter: MoneyValueFormatter = MoneyValueFormatter(thousand_separator=",", decimal_separator=".",
                                                                currency_symbol="$", decimal_precision=2)

class QvdFileWriter:
    """
    Class allows to write a :class:`QvdTable` as a QVD file to disk.
    """
    def __init__(self, target: Union[str, BinaryIO], table: QvdTable,
                 options: QvdFileWriterOptions = QvdFileWriterOptions()):
        """
        Constructs a new QVD file writer. The target can be either a file path or a BinaryIO object.

        :param target: The destination to which the Qvd file should be written.
        :param table: The data to persist.
        :param options: The options for the QVD file writer.
        """
        self._target = target
        self._table = table
        self._options = options if options is not None else QvdFileWriterOptions()

        self._header: QvdTableHeader = None
        self._symbol_table: List[Dict[QvdValue, int]] = None
        self._index_table: List[List[int]] = None
        self._header_buffer: bytes = None
        self._symbol_table_buffer: bytes = None
        self._index_table_buffer: bytes = None
        # Stores for each field whether it contains null values
        self._symbol_table_nullability: List[bool] = None

        # Initialize the header
        self._header = QvdTableHeader()
        self._header.qv_build_no = 50668
        self._header.creator_doc = str(uuid.uuid4())
        self._header.create_utc_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        self._header.source_create_utc_time = ""
        self._header.source_file_utc_time = ""
        self._header.stale_utc_time = ""
        self._header.table_name = self._options.table_name
        self._header.source_file_size = -1
        self._header.fields = []
        self._header.compression = ""
        self._header.comment = ""
        self._header.lineage = []
        self._header.no_of_records = len(self._table._data)
        self._header.no_of_fields = len(self._table._columns)

    def _build_symbol_table(self):
        """
        Builds the symbol table of the QVD file.
        """
        self._symbol_table = [None] * self._header.no_of_fields
        self._symbol_table_buffer = b""
        self._symbol_table_nullability = [False] * self._header.no_of_fields

        for column_index, _ in enumerate(self._table._columns):
            # Uses a dictionary over a set to preserve the order of the values and over a loop for performance reasons
            unique_values = list(dict.fromkeys([row[column_index] for row in self._table._data]).keys())

            symbols: Dict[QvdValue, int] = {}
            contains_none = False

            for value in unique_values:
                # Skip None values, they are represented by bias shifted negative indices
                if value is None:
                    contains_none = True
                    continue

                symbols[value] = len(symbols)

            # Extend the symbol table with the new symbols
            current_symbols_buffer = b"".join([self._get_symbol_byte_representation(symbol)
                                               for symbol in symbols])
            self._symbol_table_buffer += current_symbols_buffer
            self._symbol_table[column_index] = symbols
            self._symbol_table_nullability[column_index] = contains_none

            # Update the field header with the new symbol table information
            field_header = QvdFieldHeader()
            field_header.field_name = self._table._columns[column_index]
            field_header.no_of_symbols = len(symbols)
            field_header.offset = len(self._symbol_table_buffer) - len(current_symbols_buffer)
            field_header.length = len(current_symbols_buffer)
            field_header.comment = ""
            field_header.tags = []

            field_header.number_format = NumberFormat()
            field_header.number_format.type = "UNKNOWN"
            field_header.number_format.n_dec = 0
            field_header.number_format.use_thou = 0
            field_header.number_format.fmt = ""
            field_header.number_format.dec = ""
            field_header.number_format.thou = ""

            symbol_types = set([type(symbol) for symbol in symbols])

            if symbol_types.issubset(set([TimeValue])):
                field_header.number_format.type = "TIME"
                field_header.number_format.fmt = self._options.time_formatter.get_qvd_format_string()
                field_header.tags.append("$numeric")
            elif symbol_types.issubset(set([DateValue])):
                field_header.number_format.type = "DATE"
                field_header.number_format.fmt = self._options.date_formatter.get_qvd_format_string()
                field_header.tags.append("$date")
                field_header.tags.append("$numeric")
                field_header.tags.append("$integer")
            elif symbol_types.issubset(set([TimestampValue])):
                field_header.number_format.type = "TIMESTAMP"
                field_header.number_format.fmt = self._options.timestamp_formatter.get_qvd_format_string()
                field_header.tags.append("$timestamp")
                field_header.tags.append("$numeric")
            elif symbol_types.issubset(set([IntervalValue])):
                field_header.number_format.type = "INTERVAL"
                field_header.number_format.fmt = self._options.interval_formatter.get_qvd_format_string()
                field_header.tags.append("$numeric")
            elif symbol_types.issubset(set([MoneyValue])):
                field_header.number_format.type = "MONEY"
                field_header.number_format.fmt = self._options.money_formatter.get_qvd_format_string()
                field_header.number_format.dec = self._options.money_formatter.decimal_separator
                field_header.number_format.thou = self._options.money_formatter.thousand_separator
                field_header.tags.append("$numeric")
            elif symbol_types.issubset(set([IntegerValue])):
                field_header.tags.append("$numeric")
                field_header.tags.append("$integer")
            elif symbol_types.issubset(set([IntegerValue, DoubleValue, DualIntegerValue, DualDoubleValue])):
                field_header.tags.append("$numeric")
            elif symbol_types.issubset(set([StringValue])):
                field_header.tags.append("$text")

                if all([symbol.display_value.isascii() for symbol in symbols]):
                    field_header.tags.append("$ascii")

            self._header.fields.append(field_header)

    def _build_index_table(self):
        """
        Builds the index table of the QVD file.
        """
        self._index_table = [None] * self._header.no_of_records
        self._index_table_buffer = b""

        # Each row in the index table is represented by one or more bytes, the number of bytes used to represent a
        # row is the so called record byte size. These bytes are used to store the indices of the symbols in the symbol
        # table for each row. Therefore, the value indices of a row are concatenated in a binary representation in
        # the order of the columns of the data frame.
        #
        # Let's assume the flowing data frame and the corresponding symbol table:
        #
        # Data Frame:
        # | A | B | C |
        # |---|---|---|
        # | 1 | 4 | 7 |
        # | 2 | 4 | 8 |
        # | 2 | 6 | 9 |
        # | 3 | 6 | 7 |
        #
        # Header:
        # | FieldName | BitOffset | BitWidth |
        # |-----------|-----------|----------|
        # | A         | 0         | 2        |
        # | B         | 2         | 1        |
        # | C         | 3         | 2        |
        #
        # Symbol Table:
        # A: [1, 2, 3]
        # B: [4, 6]
        # C: [7, 8, 9]
        #
        # The third row of the data frame for example is represented by the indices [1, 1, 2] in the symbol table.
        # These indices are then converted to a binary representation and are padded with zeros to match the length
        # of the largest index of each column, the bit width. In this case, the largest index for 'A' is 2, for 'B'
        # is 1, and for 'C' is 2. Hence, all indices in 'A' and 'C' can be represented by 2 bits, and all indices in
        # 'B' can be represented by 1 bit. In binary representation, the padded indices are [01, 1, 10]. These indices
        # are then concatenated to a single binary string. The offset of the first bit of each column's index within
        # the byte is stored in the header. In this case, the bit offset of 'A' is 0, the bit offset of 'B' is 2,
        # and the bit offset of 'C' is 3. After the indices are concatenated to a binary string, the binary string
        # itself is padded with zeros to match whole bytes. The binary string for the third row is therefore
        # [01110000], which fits into one byte, the record byte size is 1 byte.
        #
        # This process is repeated for each row of the data frame, and the resulting bytes are concatenated to the so
        # called index table, basically a byte buffer. The information about the bit width and bit offset of each column
        # is stored in the header.

        for record_index, record in enumerate(self._table._data):
            record_indices = [None] * self._header.no_of_fields

            for column_index, _ in enumerate(self._table._columns):
                # Convert the raw values to indices referring to the symbol table
                value = record[column_index]
                field_contains_none = self._symbol_table_nullability[column_index]

                # None values are represented by bias shifted negative indices
                if value is None:
                    symbol_index = 0
                else:
                    # In order to represent None values, the indices are shifted by the bias value of the column
                    if field_contains_none:
                        symbol_index = self._symbol_table[column_index][value] + 2
                    else:
                        symbol_index = self._symbol_table[column_index][value]

                # Convert the integer indices to binary representation
                index_bits = format(symbol_index, "b")
                record_indices[column_index] = index_bits

            self._index_table[record_index] = record_indices

        # Normalize the bit representation of the indices by padding with zeros
        for column_index, _ in enumerate(self._table._columns):
            # Update the field header with the new bit metadata
            field_contains_none = self._symbol_table_nullability[column_index]
            # Bit offset is the sum of the bit widths of all previous columns
            self._header.fields[column_index].bit_offset = sum(
                [self._header.fields[index].bit_width for index in range(column_index)])
            # Bit width is the maximum bit width of all indices of the column
            self._header.fields[column_index].bit_width = max(
                [len(record[column_index]) for record in self._index_table])
            # Bias is used to shift the indices to represent None values
            self._header.fields[column_index].bias = -2 if field_contains_none else 0

            # Pad the bit representation of the indices with zeros to match the bit width
            for record in self._index_table:
                record[column_index] = record[column_index].rjust(self._header.fields[column_index].bit_width, "0")

        # Concatenate the bit representation of the indices of each row to a single binary string per row
        for record in self._index_table:
            record = record[::-1]
            bits = "".join(record)
            padding_width = (8 - len(bits) % 8) % 8
            padded_bits = "0" * padding_width + bits
            byte_values = [int(padded_bits[index:index + 8], 2) for index in range(0, len(padded_bits), 8)]
            record_byte_representation = struct.pack("<" + "B" * len(byte_values), *byte_values)
            record_byte_representation = record_byte_representation[::-1]

            self._index_table_buffer += record_byte_representation

        self._header.record_byte_size = len(self._index_table_buffer) // self._header.no_of_records
        self._header.length = len(self._index_table_buffer)
        self._header.offset = len(self._symbol_table_buffer)

    def _build_header(self):
        """
        Builds the header of the QVD file.
        """
        header_root = ET.Element("QvdTableHeader")

        qv_build_no_element = ET.SubElement(header_root, "QvBuildNo")
        qv_build_no_element.text = str(self._header.qv_build_no)

        creator_doc_element = ET.SubElement(header_root, "CreatorDoc")
        creator_doc_element.text = self._header.creator_doc

        create_utc_time_element = ET.SubElement(header_root, "CreateUtcTime")
        create_utc_time_element.text = self._header.create_utc_time

        source_create_utc_time_element = ET.SubElement(header_root, "SourceCreateUtcTime")
        source_create_utc_time_element.text = self._header.source_create_utc_time

        source_file_utc_time_element = ET.SubElement(header_root, "SourceFileUtcTime")
        source_file_utc_time_element.text = self._header.source_file_utc_time

        stale_utc_time_element = ET.SubElement(header_root, "StaleUtcTime")
        stale_utc_time_element.text = self._header.stale_utc_time

        table_name_element = ET.SubElement(header_root, "TableName")
        table_name_element.text = self._header.table_name

        source_file_size_element = ET.SubElement(header_root, "SourceFileSize")
        source_file_size_element.text = str(self._header.source_file_size)

        fields_element = ET.SubElement(header_root, "Fields")

        for field in self._header.fields:
            field_element = ET.SubElement(fields_element, "QvdFieldHeader")

            field_name_element = ET.SubElement(field_element, "FieldName")
            field_name_element.text = field.field_name

            bit_offset_element = ET.SubElement(field_element, "BitOffset")
            bit_offset_element.text = str(field.bit_offset)

            bit_width_element = ET.SubElement(field_element, "BitWidth")
            bit_width_element.text = str(field.bit_width)

            bias_element = ET.SubElement(field_element, "Bias")
            bias_element.text = str(field.bias)

            number_format_element = ET.SubElement(field_element, "NumberFormat")

            type_element = ET.SubElement(number_format_element, "Type")
            type_element.text = field.number_format.type

            n_dec_element = ET.SubElement(number_format_element, "nDec")
            n_dec_element.text = str(field.number_format.n_dec)

            use_thou_element = ET.SubElement(number_format_element, "UseThou")
            use_thou_element.text = str(field.number_format.use_thou)

            fmt_element = ET.SubElement(number_format_element, "Fmt")
            fmt_element.text = field.number_format.fmt

            dec_element = ET.SubElement(number_format_element, "Dec")
            dec_element.text = field.number_format.dec

            thou_element = ET.SubElement(number_format_element, "Thou")
            thou_element.text = field.number_format.thou

            no_of_symbols_element = ET.SubElement(field_element, "NoOfSymbols")
            no_of_symbols_element.text = str(field.no_of_symbols)

            offset_element = ET.SubElement(field_element, "Offset")
            offset_element.text = str(field.offset)

            length_element = ET.SubElement(field_element, "Length")
            length_element.text = str(field.length)

            comment_element = ET.SubElement(field_element, "Comment")
            comment_element.text = field.comment

            tags_element = ET.SubElement(field_element, "Tags")

            for tag in field.tags:
                tag_element = ET.SubElement(tags_element, "String")
                tag_element.text = tag

        compression_element = ET.SubElement(header_root, "Compression")
        compression_element.text = self._header.compression

        record_byte_size_element = ET.SubElement(header_root, "RecordByteSize")
        record_byte_size_element.text = str(self._header.record_byte_size)

        no_of_records_element = ET.SubElement(header_root, "NoOfRecords")
        no_of_records_element.text = str(self._header.no_of_records)

        offset_element = ET.SubElement(header_root, "Offset")
        offset_element.text = str(self._header.offset)

        length_element = ET.SubElement(header_root, "Length")
        length_element.text = str(self._header.length)

        comment_element = ET.SubElement(header_root, "Comment")
        comment_element.text = self._header.comment

        lineage_element = ET.SubElement(header_root, "Lineage")

        for lineage_info in self._header.lineage:
            lineage_info_element = ET.SubElement(lineage_element, "LineageInfo")

            discriminator_element = ET.SubElement(lineage_info_element, "Discriminator")
            discriminator_element.text = lineage_info.discriminator

            statement_element = ET.SubElement(lineage_info_element, "Statement")
            statement_element.text = lineage_info.statement

        ET.indent(header_root, '  ')

        header_xml = ET.tostring(header_root, encoding="utf-8",
                                          xml_declaration=True, short_empty_elements=False, method="xml").decode()
        header_xml = " ".join([line + "\r\n" for line in header_xml.splitlines() if line.strip()])

        self._header_buffer = header_xml.encode()

    def _write_data(self):
        """
        Writes the data to the QVD file.
        """
        if isinstance(self._target, str):
            with open(self._target, "wb") as file:
                file.write(self._header_buffer)
                file.write(b"\0")
                file.write(self._symbol_table_buffer)
                file.write(self._index_table_buffer)
        elif isinstance(self._target, (io.RawIOBase, io.BufferedIOBase)):
            self._target.write(self._header_buffer)
            self._target.write(b"\0")
            self._target.write(self._symbol_table_buffer)
            self._target.write(self._index_table_buffer)
        else:
            raise ValueError("Unsupported target type. Please provide either a file path or a BinaryIO object.")

    def write(self):
        """
        Writes the :class:`QvdTable` object as a QVD file to the target destination.
        """
        self._build_symbol_table()
        self._build_index_table()
        self._build_header()
        self._write_data()

    def _get_symbol_byte_representation(self, value: QvdValue) -> bytes:
        """
        Returns the byte representation of a symbol value.

        :param value: The symbol value to convert.
        :return: The byte representation of the symbol value.
        """
        if isinstance(value, TimeValue):
            # Recreate display value to ensure uniform formatting
            display_value = self._options.time_formatter.format(value)

            return (b"\06" + struct.pack("<d", value.calculation_value) +
                    str.encode(display_value, encoding="utf-8") + b"\0")
        elif isinstance(value, DateValue):
            # Recreate display value to ensure uniform formatting
            display_value = self._options.date_formatter.format(value)

            return (b"\05" +
                    value.calculation_value.to_bytes(4, byteorder="little", signed=True) +
                    str.encode(display_value, encoding="utf-8") + b"\0")
        elif isinstance(value, TimestampValue):
            # Recreate display value to ensure uniform formatting
            display_value = self._options.timestamp_formatter.format(value)

            return (b"\06" + struct.pack("<d", value.calculation_value) +
                    str.encode(display_value, encoding="utf-8") + b"\0")
        elif isinstance(value, IntervalValue):
            # Recreate display value to ensure uniform formatting
            display_value = self._options.interval_formatter.format(value)

            return (b"\06" + struct.pack("<d", value.calculation_value) +
                    str.encode(display_value, encoding="utf-8") + b"\0")
        elif isinstance(value, MoneyValue):
            # Recreate display value to ensure uniform formatting
            display_value = self._options.money_formatter.format(value)

            return (b"\06" + struct.pack("<d", value.calculation_value) +
                    str.encode(display_value, encoding="utf-8") + b"\0")
        elif isinstance(value, IntegerValue):
            return b"\01" + value.calculation_value.to_bytes(4, byteorder="little", signed=True)
        elif isinstance(value, DoubleValue):
            return b"\02" + struct.pack("<d", value.calculation_value)
        elif isinstance(value, StringValue):
            return b"\04" + str.encode(value.calculation_value, encoding="utf-8") + b"\0"
        elif isinstance(value, DualIntegerValue):
            return (b"\05" +
                    value.calculation_value.to_bytes(4, byteorder="little", signed=True) +
                    str.encode(value.display_value, encoding="utf-8") +
                    b"\0")
        elif isinstance(value, DualDoubleValue):
            return (b"\06" + struct.pack("<d", value.calculation_value) +
                    str.encode(value.display_value, encoding="utf-8") + b"\0")
        else:
            raise ValueError("Unsupported symbol value type.")

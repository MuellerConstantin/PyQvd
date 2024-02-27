"""
Contains classes for parsing and representing QVD files.
"""

import uuid
import time
import os
import struct
from typing import TYPE_CHECKING
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from tabulate import tabulate

if TYPE_CHECKING:
    import pandas as pd

class QvdSymbol:
    """
    Represents a Qlik symbol/value, stored in a QVD file.
    """
    def __init__(self, int_value: int | None, double_value: float | None, string_value: str | None):
        """
        Constructs a new QVD symbol.

        :param intValue: Der Ganzzahlwert.
        :param doubleValue: Der Double-Wert.
        :param stringValue: Der Zeichenkettenwert.
        """

        self._int_value = int_value
        self._double_value = double_value
        self._string_value = string_value

    @property
    def int_value(self) -> int | None:
        """
        Returns the integer value of this symbol.

        :return: The integer value.
        """
        return self._int_value

    @property
    def double_value(self) -> float | None:
        """
        Returns the double value of this symbol.

        :return: The double value.
        """
        return self._double_value

    @property
    def string_value(self) -> str | None:
        """
        Returns the string value of this symbol.

        :return: The string value.
        """
        return self._string_value

    def to_primary_value(self) -> str | int | float | None:
        """
        Retrieves the primary value of this symbol. The primary value is a descriptive raw value.
        It is either the string value, the integer value, or the double value, prioritized in this order.

        :return: The primary value.
        """
        if self._string_value is not None:
            return self._string_value
        elif self._int_value is not None:
            return self._int_value
        elif self._double_value is not None:
            return self._double_value
        else:
            return None
    
    def to_byte_representation(self) -> bytes:
        """
        Converts the symbol to its byte representation.

        :return: The byte representation of the symbol.
        """
        if self._int_value is not None and self._string_value is not None:
            return b'\05' + self._int_value.to_bytes(4, byteorder='little', signed=True) + str.encode(self._string_value) + b'\0'
        elif self._double_value is not None and self._string_value is not None:
            return b'\06' + struct.pack('<d', self._double_value) + str.encode(self._string_value) + b'\0'
        elif self._int_value is not None:
            return b'\01' + self._int_value.to_bytes(4, byteorder='little', signed=True)
        elif self._double_value is not None:
            return b'\02' + struct.pack('<d', self._double_value)
        elif self._string_value is not None:
            return b'\04' + str.encode(self._string_value) + b'\0'
        else:
            raise ValueError('The symbol does not contain any value.')
    
    def __eq__(self, __value: object) -> bool:
        """
        Determines whether this symbol is equal to another object.

        :param __value: The other object.
        :return: True if the objects are equal, otherwise False.
        """
        if not isinstance(__value, QvdSymbol):
            return False
        
        return self._int_value == __value._int_value and self._double_value == __value._double_value and self._string_value == __value._string_value
    
    def __ne__(self, __value: object) -> bool:
        """
        Determines whether this symbol is not equal to another object.

        :param __value: The other object.
        :return: True if the objects are not equal, otherwise False.
        """
        return not self.__eq__(__value)

    @staticmethod
    def from_int_value(int_value: int):
        return QvdSymbol(int_value, None, None)

    @staticmethod
    def from_double_value(double_value: float):
        return QvdSymbol(None, double_value, None)

    @staticmethod
    def from_string_value(string_value: str):
        return QvdSymbol(None, None, string_value)

    @staticmethod
    def from_dual_int_value(int_value: int, string_value: str):
        return QvdSymbol(int_value, None, string_value)

    @staticmethod
    def from_dual_double_value(double_value: float, string_value: str):
        return QvdSymbol(None, double_value, string_value)

class QvdDataFrame:
    """
    Represents the data frame stored inside a QVD file.
    """
    def __init__(self, data: list[list[any]], columns: list[str]):
        """
        Constructs a new QVD data frame.

        :param data: The data of the data frame.
        :param columns: The columns of the data frame.
        """
        self._data = data
        self._columns = columns
    
    @property
    def data(self) -> list[list[any]]:
        """
        Returns the data of the data frame.

        :return: The data.
        """
        return self._data
    
    @property
    def columns(self) -> list[str]:
        """
        Returns the columns of the data frame.

        :return: The columns.
        """
        return self._columns
    
    @property
    def shape(self) -> tuple[int, int]:
        """
        Returns the shape of the data frame.

        :return: The shape.
        """
        return len(self._data), len(self._columns)
    
    def head(self, n: int = 5) -> 'QvdDataFrame':
        """
        Returns the first n rows of the data frame.

        :param n: The number of rows to return.
        :return: The first n rows.
        """
        return QvdDataFrame(self._data[:n], self._columns)
    
    def tail(self, n: int = 5) -> 'QvdDataFrame':
        """
        Returns the last n rows of the data frame.

        :param n: The number of rows to return.
        :return: The last n rows.
        """
        return QvdDataFrame(self._data[-n:], self._columns)
    
    def rows(self, *args: int) -> 'QvdDataFrame':
        """
        Returns the specified rows of the data frame.

        :param args: The rows to return.
        :return: The specified rows.
        """
        return QvdDataFrame([self._data[index] for index in args], self._columns)
    
    def at(self, row: int, column: str) -> any:
        """
        Returns the value at the specified row and column.

        :param row: The row index.
        :param column: The column name.
        :return: The value at the specified row and column.
        """
        return self._data[row][self._columns.index(column)]
    
    def select(self, *args: str) -> 'QvdDataFrame':
        """
        Selects the specified columns from the data frame.

        :param args: The columns to select.
        :return: The data frame with the selected columns.
        """
        indices = [self._columns.index(arg) for arg in args]
        data = [[row[index] for index in indices] for row in self._data]
        columns = [self._columns[index] for index in indices]
        return QvdDataFrame(data, columns)
    
    def to_qvd(self, path: str):
        """
        Persists the data frame to a QVD file.

        :param path: The path to the QVD file.
        """
        QvdFileWriter(path, self).save()
    
    def to_dict(self) -> dict[str, list[any]]:
        """
        Converts the data frame to a dictionary.

        :return: The dictionary representation of the data frame.
        """
        return {'columns': self._columns, 'data': self._data}
    
    def to_pandas(self) -> 'pd.DataFrame':
        """
        Converts the data frame to a pandas data frame.

        :return: The pandas data frame.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("Pandas is not installed. Please install Pandas to use this method.")

        return pd.DataFrame(self._data, columns=self._columns)
    
    def __str__(self) -> str:
        """
        Returns a string representation of the data frame.

        :return: The string representation.
        """
        return tabulate(self._data, headers=self._columns)
    
    @staticmethod
    def from_qvd(path: str) -> 'QvdDataFrame':
        """
        Loads a QVD file and returns its data frame.

        :param path: The path to the QVD file.
        :return: The data frame of the QVD file.
        """
        return QvdFileReader(path).load()
    
    @staticmethod
    def from_dict(data: dict[str, list[any]]) -> 'QvdDataFrame':
        """
        Constructs a new QVD data frame from a dictionary.

        :param data: The dictionary representation of the data frame.
        :return: The QVD data frame.
        """
        return QvdDataFrame(data['data'], data['columns'])
    
    @staticmethod
    def from_pandas(df: 'pd.DataFrame') -> 'QvdDataFrame':
        """
        Constructs a new QVD data frame from a pandas data frame.

        :param df: The pandas data frame.
        :return: The QVD data frame.
        """
        return QvdDataFrame(df.values.tolist(), df.columns.tolist())

class QvdFileReader:
    """
    Parses a QVD file and loads it into memory.
    """
    def __init__(self, path: str):
        """
        Constructs a new QVD file parser.

        :param path: The path to the QVD file.
        """
        self._path = path
        self._buffer = None
        self._header_offfset = None
        self._symbol_table_offset = None
        self._index_table_offset = None
        self._header = None
        self._symbol_table = None
        self._index_table = None

    def _read_data(self):
        """
        Reads the data of the QVD file into memory.
        """
        with open(self._path, 'rb') as file:
            self._buffer = file.read()

    def _parse_header(self):
        """
        Parses the header of the QVD file.
        """
        if not self._buffer:
            raise ValueError('The QVD file has not been loaded in the proper order or has not been loaded at all.')
        
        HEADER_DELIMITER = '\r\n\0'
        
        header_begin_index = 0
        header_delimiter_index = self._buffer.find(str.encode(HEADER_DELIMITER), header_begin_index)

        if header_delimiter_index == -1:
            raise ValueError('The XML header section does not exist or is not properly delimited from the binary data.')
        
        header_end_index = header_delimiter_index + len(HEADER_DELIMITER)
        header_buffer = self._buffer[header_begin_index:header_end_index].decode()

        self._header = ET.fromstring(header_buffer[:-1])

        if not self._header:
            raise ValueError('The XML header could not be parsed.')
        
        self._headerOffset = header_begin_index
        self._symbol_table_offset = header_end_index
        self._index_table_offset = self._symbol_table_offset + int(self._header.find('./Offset').text, 10)
    
    def _parse_symbol_table(self):
        """
        Parses the symbol table of the QVD file.
        """
        if not all([self._buffer, self._header, self._symbol_table_offset, self._index_table_offset]):
            raise ValueError('The QVD file has not been loaded in the proper order or has not been loaded at all.')

        fields = self._header.find('./Fields').findall('./QvdFieldHeader')
        symbol_buffer = self._buffer[self._symbol_table_offset:self._index_table_offset]

        self._symbol_table = [None] * len(fields)

        for index, field in enumerate(fields):
            symbols_offset = int(field.find('./Offset').text, 10)
            symbols_length = int(field.find('./Length').text, 10)

            symbols = []
            pointer = symbols_offset

            while pointer < symbols_offset + symbols_length:
                type_byte = symbol_buffer[pointer]
                pointer += 1

                if type_byte == 1:
                    byte_data = symbol_buffer[pointer:pointer + 4]
                    value = int.from_bytes(byte_data, byteorder='little', signed=True)
                    pointer += 4
                    symbols.append(QvdSymbol.from_int_value(value))
                elif type_byte == 2:
                    byte_data = symbol_buffer[pointer:pointer + 8]
                    value = struct.unpack('<d', byte_data)[0]
                    pointer += 8
                    symbols.append(QvdSymbol.from_double_value(value))
                elif type_byte == 4:
                    value = ''

                    while symbol_buffer[pointer] != 0:
                        value += chr(symbol_buffer[pointer])
                        pointer += 1
                    
                    pointer += 1
                    symbols.append(QvdSymbol.from_string_value(value))
                elif type_byte == 5:
                    byte_data = symbol_buffer[pointer:pointer + 4]
                    int_value = int.from_bytes(byte_data, byteorder='little', signed=True)
                    pointer += 4

                    string_value = ''
                    while symbol_buffer[pointer] != 0:
                        string_value += chr(symbol_buffer[pointer])
                        pointer += 1
                    
                    pointer += 1
                    symbols.append(QvdSymbol.from_dual_int_value(int_value, string_value))
                elif type_byte == 6:
                    byte_data = symbol_buffer[pointer:pointer + 8]
                    double_value = struct.unpack('<d', byte_data)[0]
                    pointer += 8

                    string_value = ''
                    while symbol_buffer[pointer] != 0:
                        string_value += chr(symbol_buffer[pointer])
                        pointer += 1
                    
                    pointer += 1
                    symbols.append(QvdSymbol.from_dual_double_value(double_value, string_value))
                else:
                    raise ValueError('The symbol type byte is not recognized. Unknown data type: ' + hex(type_byte))
            
            self._symbol_table[index] = symbols

    def _parse_index_table(self):
        """
        Parses the index table of the QVD file.
        """
        if not (self._buffer and self._header and self._index_table_offset):
            raise ValueError('The QVD file has not been loaded in the proper order or has not been loaded at all.')

        fields = self._header.find('./Fields').findall('./QvdFieldHeader')
        record_size = int(self._header.find('RecordByteSize').text, 10)
        length = int(self._header.find('Length').text, 10)

        index_buffer = self._buffer[self._index_table_offset:self._index_table_offset + length + 1]
        self._index_table = []

        pointer = 0
        while pointer < len(index_buffer):
            bytes = index_buffer[pointer:pointer + record_size]
            bytes = bytes[::-1]
            bytes = struct.unpack('<' + 'B' * len(bytes), bytes)

            mask = ''.join(format(byte, '08b') for byte in bytes)
            mask = mask[::-1]
            mask = [int(bit) for bit in mask]

            symbol_indices = []

            for field in fields:
                bit_offset = int(field.find('BitOffset').text, 10)
                bit_width = int(field.find('BitWidth').text, 10)
                bias = int(field.find('Bias').text, 10)

                if bit_width == 0:
                    symbol_index = 0
                else:
                    symbol_index = QvdFileReader._convert_bits_to_int32(mask[bit_offset:bit_offset + bit_width])

                symbol_index += bias
                symbol_indices.append(symbol_index)
            
            self._index_table.append(symbol_indices)
            pointer += record_size
    
    def load(self) -> QvdDataFrame:
        """
        Loads the QVD file into memory and parses it.

        :return: The loaded QVD file.
        """
        self._read_data()
        self._parse_header()
        self._parse_symbol_table()
        self._parse_index_table()

        def _get_row(index: int) -> list[any]:
            if index >= len(self._index_table):
                raise ValueError('Index is out of bounds')
        
            row = [None] * len(self._symbol_table)

            for field_index, symbol_index in enumerate(self._index_table[index]):
                if symbol_index < 0:
                    row[field_index] = None
                else:
                    symbol = self._symbol_table[field_index][symbol_index].to_primary_value()

                    if isinstance(symbol, str):
                        try:
                            symbol = int(symbol)
                        except ValueError:
                            try:
                                symbol = float(symbol)
                            except ValueError:
                                pass

                    row[field_index] = symbol

            return row
        
        data = [_get_row(index) for index in range(len(self._index_table))]
        columns = [field.find('FieldName').text for field in self._header.find('./Fields').findall('./QvdFieldHeader')]

        return QvdDataFrame(data, columns)

    @staticmethod
    def _convert_bits_to_int32(bits: list[int]) -> int:
        """
        Converts a list of bits to an integer.
        """
        if len(bits) == 0:
            return 0
    
        return sum(bit * (2 ** index) for index, bit in enumerate(bits))

class QvdFileWriter:
    """
    Persists a QVD file to disk.
    """
    def __init__(self, path: str, df: QvdDataFrame):
        """
        Constructs a new QVD file writer.

        :param path: The path to the QVD file.
        :param df: The data to persist.
        """
        self._path = path
        self._df = df
        self._header = None
        self._symbol_buffer = None
        self._symbol_table = None
        self._symbol_table_metadata = None
        self._index_buffer = None
        self._index_table = None
        self._index_table_metadata = None
        self._record_byte_size = None
    
    def _write_data(self):
        """
        Writes the data to the QVD file.
        """
        with open(self._path, 'wb') as file:
            file.write(self._header.encode())
            file.write(b'\0')
            file.write(self._symbol_buffer)
            file.write(self._index_buffer)

    def _build_header(self):
        """
        Builds the XML header of the QVD file.
        """

        doc = minidom.Document()

        header_element = doc.createElement('QvdTableHeader')

        """
        The following fields before the field definitions are undocumented and Qlik Sense specific. These fields
        seems to be not technically necessary for parsing a QVD file, but are mandatory for Qlik Sense to recognize
        the QVD file as a valid QVD file. Hence, some of these fields are hardcoded and some are generated randomly.
        """

        qv_build_no_element = doc.createElement('QvBuildNo')
        qv_build_no_element.appendChild(doc.createTextNode('50667'))
        header_element.appendChild(qv_build_no_element)

        creator_doc_element = doc.createElement('CreatorDoc')
        creator_doc_element.appendChild(doc.createTextNode(str(uuid.uuid4())))
        header_element.appendChild(creator_doc_element)

        create_utc_time_element = doc.createElement('CreateUtcTime')
        create_utc_time_element.appendChild(doc.createTextNode(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())))
        header_element.appendChild(create_utc_time_element)

        source_create_utc_time_element = doc.createElement('SourceCreateUtcTime')
        source_create_utc_time_element.appendChild(doc.createTextNode(''))
        header_element.appendChild(source_create_utc_time_element)

        source_file_utc_time_element = doc.createElement('SourceFileUtcTime')
        source_file_utc_time_element.appendChild(doc.createTextNode(''))
        header_element.appendChild(source_file_utc_time_element)

        source_file_size_element = doc.createElement('SourceFileSize')
        source_file_size_element.appendChild(doc.createTextNode('-1'))
        header_element.appendChild(source_file_size_element)

        stale_utc_time_element = doc.createElement('StaleUtcTime')
        stale_utc_time_element.appendChild(doc.createTextNode(''))
        header_element.appendChild(stale_utc_time_element)

        table_name_element = doc.createElement('TableName')
        table_name_element.appendChild(doc.createTextNode(os.path.splitext(os.path.basename(self._path))[0]))
        header_element.appendChild(table_name_element)

        fields_element = doc.createElement('Fields')

        for column_index, column_name in enumerate(self._df.columns):
            field_element = doc.createElement('QvdFieldHeader')

            field_name_element = doc.createElement('FieldName')
            field_name_element.appendChild(doc.createTextNode(column_name))
            field_element.appendChild(field_name_element)

            bit_offset_element = doc.createElement('BitOffset')
            bit_offset_element.appendChild(doc.createTextNode(str(self._index_table_metadata[column_index][0])))
            field_element.appendChild(bit_offset_element)

            bit_width_element = doc.createElement('BitWidth')
            bit_width_element.appendChild(doc.createTextNode(str(self._index_table_metadata[column_index][1])))
            field_element.appendChild(bit_width_element)
            
            bias_element = doc.createElement('Bias')
            bias_element.appendChild(doc.createTextNode(str(self._index_table_metadata[column_index][2])))
            field_element.appendChild(bias_element)

            no_of_symbols_element = doc.createElement('NoOfSymbols')
            no_of_symbols_element.appendChild(doc.createTextNode(str(len(self._symbol_table[column_index]))))
            field_element.appendChild(no_of_symbols_element)
            
            offset_element = doc.createElement('Offset')
            offset_element.appendChild(doc.createTextNode(str(self._symbol_table_metadata[column_index][0])))
            field_element.appendChild(offset_element)
            
            length_element = doc.createElement('Length')
            length_element.appendChild(doc.createTextNode(str(self._symbol_table_metadata[column_index][1])))
            field_element.appendChild(length_element)
            
            comment_element = doc.createElement('Comment')
            comment_element.appendChild(doc.createTextNode(''))
            field_element.appendChild(comment_element)
            
            number_format_element = doc.createElement('NumberFormat')
            
            number_format_type_element = doc.createElement('Type')
            number_format_type_element.appendChild(doc.createTextNode('UNKNOWN'))
            number_format_element.appendChild(number_format_type_element)

            number_format_n_dec_element = doc.createElement('nDec')
            number_format_n_dec_element.appendChild(doc.createTextNode('0'))
            number_format_element.appendChild(number_format_n_dec_element)

            number_format_use_thou_element = doc.createElement('UseThou')
            number_format_use_thou_element.appendChild(doc.createTextNode('0'))
            number_format_element.appendChild(number_format_use_thou_element)

            number_format_fmt_element = doc.createElement('Fmt')
            number_format_fmt_element.appendChild(doc.createTextNode(''))
            number_format_element.appendChild(number_format_fmt_element)

            number_format_dec_element = doc.createElement('Dec')
            number_format_dec_element.appendChild(doc.createTextNode(''))
            number_format_element.appendChild(number_format_dec_element)

            number_format_thou_element = doc.createElement('Thou')
            number_format_thou_element.appendChild(doc.createTextNode(''))
            number_format_element.appendChild(number_format_thou_element)

            field_element.appendChild(number_format_element)

            tags_element = doc.createElement('Tags')
            field_element.appendChild(tags_element)

            fields_element.appendChild(field_element)

        header_element.appendChild(fields_element)

        record_byte_size_element = doc.createElement('RecordByteSize')
        record_byte_size_element.appendChild(doc.createTextNode(str(self._record_byte_size)))
        header_element.appendChild(record_byte_size_element)

        no_of_records_element = doc.createElement('NoOfRecords')
        no_of_records_element.appendChild(doc.createTextNode(str(len(self._df.data))))
        header_element.appendChild(no_of_records_element)

        offset_element = doc.createElement('Offset')
        offset_element.appendChild(doc.createTextNode(str(self._symbol_table_metadata[-1][0] + self._symbol_table_metadata[-1][1])))
        header_element.appendChild(offset_element)

        length_element = doc.createElement('Length')
        length_element.appendChild(doc.createTextNode(str(len(self._index_buffer))))
        header_element.appendChild(length_element)

        compression_element = doc.createElement('Compression')
        compression_element.appendChild(doc.createTextNode(''))
        header_element.appendChild(compression_element)

        comment_element = doc.createElement('Comment')
        comment_element.appendChild(doc.createTextNode(''))
        header_element.appendChild(comment_element)

        encryption_info_element = doc.createElement('EncryptionInfo')
        encryption_info_element.appendChild(doc.createTextNode(''))
        header_element.appendChild(encryption_info_element)

        table_tags_element = doc.createElement('TableTags')
        table_tags_element.appendChild(doc.createTextNode(''))
        header_element.appendChild(table_tags_element)

        profiling_data_element = doc.createElement('ProfilingData')
        profiling_data_element.appendChild(doc.createTextNode(''))
        header_element.appendChild(profiling_data_element)

        lineage_element = doc.createElement('Lineage')
        
        lineage_info_element = doc.createElement('LineageInfo')

        discriminator_element = doc.createElement('Discriminator')
        discriminator_element.appendChild(doc.createTextNode('INLINE;'))
        lineage_info_element.appendChild(discriminator_element)

        statement_element = doc.createElement('Statement')
        statement_element.appendChild(doc.createTextNode(''))
        lineage_info_element.appendChild(statement_element)

        lineage_element.appendChild(lineage_info_element)

        header_element.appendChild(lineage_element)

        doc.appendChild(header_element)

        self._header = doc.toprettyxml(indent="  ", encoding='utf-8', standalone=True, newl='\r\n').decode()
        self._header = ' '.join([line + '\r\n' for line in self._header.splitlines() if line.strip()])
    
    def _build_symbol_table(self):
        """
        Builds the symbol table of the QVD file.
        """

        self._symbol_table = [None] * len(self._df.columns)
        self._symbol_table_metadata = [None] * len(self._df.columns)
        self._symbol_buffer = b''
        
        for column_index, column_name in enumerate(self._df.columns):
            unique_values = set([row[column_index] for row in self._df.data])

            symbols = []

            for value in unique_values:
                symbols.append(self._convert_raw_to_symbol(value))
            
            current_symbol_buffer = b''.join([symbol.to_byte_representation() for symbol in symbols])
            self._symbol_buffer += current_symbol_buffer

            symbols_length = len(current_symbol_buffer)
            symbols_offset = sum([self._symbol_table_metadata[index][1] for index in range(column_index)])

            self._symbol_table_metadata[column_index] = (symbols_offset, symbols_length)
            self._symbol_table[column_index] = symbols
    
    def _build_index_table(self):
        """
        Builds the index table of the QVD file.
        """

        self._index_table = [None] * len(self._df.data)
        self._index_table_metadata = [None] * len(self._df.columns)
        self._index_buffer = b''

        """
        Each row in the index table is represented by one or more bytes, the number of bytes used to represent a row is
        the so called record byte size. These bytes are used to store the indices of the symbols in the symbol table for
        each row. Therefore, the value indices of a row are concatenated in a binary representation in the order of the
        columns of the data frame.

        Let's assume the flowing data frame and the corresponding symbol table:

        Data Frame:
        | A | B | C |
        |---|---|---|
        | 1 | 4 | 7 |
        | 2 | 4 | 8 |
        | 2 | 6 | 9 |
        | 3 | 6 | 7 |

        Header:
        | FieldName | BitOffset | BitWidth |
        |-----------|-----------|----------|
        | A         | 0         | 2        |
        | B         | 2         | 1        |
        | C         | 3         | 2        |

        Symbol Table:
        A: [1, 2, 3]
        B: [4, 6]
        C: [7, 8, 9]

        The third row of the data frame for example is represented by the indices [1, 1, 2] in the symbol table. These indices
        are then converted to a binary representation and are padded with zeros to match the length of the largest index of
        each column, the bit width. In this case, the largest index for 'A' is 2, for 'B' is 1, and for 'C' is 2. Hence, all
        indices in 'A' and 'C' can be represented by 2 bits, and all indices in 'B' can be represented by 1 bit. In binary
        representation, the padded indices are [01, 1, 10]. These indices are then concatenated to a single binary string.
        The offset of the first bit of each column's index within the byte is stored in the header. In this case, the bit
        offset of 'A' is 0, the bit offset of 'B' is 2, and the bit offset of 'C' is 3. After the indices are concatenated
        to a binary string, the binary string itself is padded with zeros to match whole bytes. The binary string for the
        third row is therefore [01110000], which fits into one byte, the record byte size is 1 byte.

        This process is repeated for each row of the data frame, and the resulting bytes are concatenated to the so called
        index table, basically a byte buffer. The information about the bit width and bit offset of each column is stored
        in the header.
        """

        for row_index, row in enumerate(self._df.data):
            indices = [None] * len(self._df.columns)

            # Convert the raw values to indices referring to the symbol table
            for column_index, column_name in enumerate(self._df.columns):
                value = row[column_index]
                symbol = self._convert_raw_to_symbol(value)
                symbol_index = self._symbol_table[column_index].index(symbol)
                indices[column_index] = symbol_index

            # Convert the integer indices to binary representation
            for index_index, index in enumerate(indices):
                bits = self._convert_int32_to_bits(index, 8)
                bits = ''.join([str(bit) for bit in bits])
                bits = bits.lstrip('0') or '0'
                indices[index_index] = bits

            self._index_table[row_index] = indices
        
        # Normalize the bit representation of the indices by padding with zeros
        for column_index, column_name in enumerate(self._df.columns):
            # Bit offset is the sum of the bit widths of all previous columns
            bit_offset = sum([self._index_table_metadata[index][1] for index in range(column_index) if self._index_table_metadata[index] is not None])
            # Bit width is the maximum bit width of all indices of the column
            bit_width = max([len(bit_indices[column_index]) for bit_indices in self._index_table])
            bias = 0
            self._index_table_metadata[column_index] = (bit_offset, bit_width, bias)

            # Pad the bit representation of the indices with zeros to match the bit width
            for bit_indices in self._index_table:
                bit_indices[column_index] = bit_indices[column_index].rjust(bit_width, '0')
        
        # Concatenate the bit representation of the indices of each row to a single binary string per row
        for bit_indices in self._index_table:
            bits = ''.join(bit_indices)
            padded_bits = '0' * (8 - len(bits) % 8) + bits
            byte_values = [int(padded_bits[index:index + 8], 2) for index in range(0, len(padded_bits), 8)]
            byte_representation = struct.pack('<' + 'B' * len(byte_values), *byte_values)

            self._index_buffer += byte_representation
        
        self._record_byte_size = len(self._index_buffer) // len(self._df.data)

    def _convert_raw_to_symbol(self, raw: any) -> QvdSymbol:
        """
        Converts a raw value to a QVD symbol.

        :param raw: The raw value.
        :return: The QVD symbol.
        """
        if isinstance(raw, int):
            return QvdSymbol.from_dual_int_value(raw, str(raw))
        elif isinstance(raw, float):
            return QvdSymbol.from_dual_double_value(raw, str(raw))
        elif isinstance(raw, str):
            return QvdSymbol.from_string_value(raw)
        else:
            return QvdSymbol.from_string_value(str(raw))

    @staticmethod
    def _convert_int32_to_bits(value: int, width: int) -> list[int]:
        """
        Converts an integer to a list of bits.

        :param value: The integer value.
        :param width: The width of the bits.
        :return: The list of bits.
        """
        return [int(bit) for bit in format(value, '0' + str(width) + 'b')]
    
    def save(self):
        """
        Persists the data frame to a QVD file.
        """
        
        self._build_symbol_table()
        self._build_index_table()
        self._build_header()
        self._write_data()

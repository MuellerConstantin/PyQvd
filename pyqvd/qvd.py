"""
Contains classes for parsing and representing QVD files.
"""

from tabulate import tabulate
import xml.etree.ElementTree as ET
import struct

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
    
    def head(self, n: int) -> 'QvdDataFrame':
        """
        Returns the first n rows of the data frame.

        :param n: The number of rows to return.
        :return: The first n rows.
        """
        return QvdDataFrame(self._data[:n], self._columns)
    
    def tail(self, n: int) -> 'QvdDataFrame':
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
    
    def to_dict(self) -> dict[str, list[any]]:
        """
        Converts the data frame to a dictionary.

        :return: The dictionary representation of the data frame.
        """
        return {'columns': self._columns, 'data': self._data}
    
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

class QvdFileReader:
    """
    Parses a QVD file and loads it into memory. Basically, it is a builder for QvdFile instances, containing
    the parsing logic for the QVD file format.
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
        with open(self._path, 'rb') as file:
            self._buffer = file.read()

    def _parse_header(self):
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
                    row[field_index] = self._symbol_table[field_index][symbol_index].to_primary_value()

            return row
        
        data = [_get_row(index) for index in range(len(self._index_table))]
        columns = [field.find('FieldName').text for field in self._header.find('./Fields').findall('./QvdFieldHeader')]

        return QvdDataFrame(data, columns)

    @staticmethod
    def _convert_bits_to_int32(bits: list[int]) -> int:
        if len(bits) == 0:
            return 0
    
        return sum(bit * (2 ** index) for index, bit in enumerate(bits))

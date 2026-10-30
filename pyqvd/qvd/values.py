"""
Module contains the abstract :class:`QvdValue` base class and the physical value types of the
symbol table of a QVD file.
"""

from copy import deepcopy
from abc import ABCMeta, abstractmethod
from typing import Dict

class QvdValue(metaclass=ABCMeta):
    """
    Base class for all QVD data types. All values in a QVD file must inherit from this class.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    @property
    @abstractmethod
    def display_value(self) -> str:
        """
        Returns the representational value of this QVD value. This value is used for display
        purposes.

        :return: The display value.
        """

    @property
    @abstractmethod
    def calculation_value(self) -> object:
        """
        Returns the calculation value of this QVD value. This value is used for calculations
        and sorting operations.

        :return: The calculation value.
        """

    @abstractmethod
    def __eq__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is equal to another object.

        :param __value: The other object.
        :return: True if the objects are equal; otherwise, False.
        """
        return NotImplemented

    def __ne__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is not equal to another object.

        :param __value: The other object.
        :return: True if the objects are not equal; otherwise, False.
        """
        return not self.__eq__(__value)

    @abstractmethod
    def __lt__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is less than another object.

        :param __value: The other object.
        :return: True if this value is less than the other object; otherwise, False.
        """
        return NotImplemented

    @abstractmethod
    def __le__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is less than or equal to another object.

        :param __value: The other object.
        :return: True if this value is less than or equal to the other object; otherwise, False.
        """
        return NotImplemented

    @abstractmethod
    def __gt__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is greater than another object.

        :param __value: The other object.
        :return: True if this value is greater than the other object; otherwise, False.
        """
        return NotImplemented

    @abstractmethod
    def __ge__(self, __value: object) -> bool:
        """
        Determines whether this QVD value is greater than or equal to another object.

        :param __value: The other object.
        :return: True if this value is greater than or equal to the other object; otherwise, False.
        """
        return NotImplemented

    @abstractmethod
    def __hash__(self) -> int:
        """
        Returns the hash value of this QVD value.

        :return: The hash value.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Returns a string representation of this QVD value.

        :return: The string representation.
        """
        return str(self.display_value)

    def __repr__(self) -> str:
        """
        Returns a string representation of this QVD value.

        :return: The string representation.
        """
        return self.__str__()

class IntegerValue(QvdValue):
    """
    Represents an integer value in a QVD file.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    def __init__(self, value: int):
        """
        Constructs a new integer value.

        :param value: The integer value.
        """
        self._value: int = value
        self._hash = None

    @property
    def display_value(self) -> str:
        return f"{self._value}"

    @property
    def calculation_value(self) -> int:
        return self._value

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value

        return self.calculation_value == __value

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value

        return self.calculation_value < __value

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value

        return self.calculation_value <= __value

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value

        return self.calculation_value > __value

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value

        return self.calculation_value >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "IntegerValue":
        return IntegerValue(self._value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "IntegerValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = IntegerValue(deepcopy(self._value, memo))
        memo[id(self)] = new_copy

        return new_copy

class DoubleValue(QvdValue):
    """
    Represents a double value in a QVD file.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    def __init__(self, value: float):
        """
        Constructs a new double value.

        :param value: The double value.
        """
        self._value: float = value
        self._hash = None

    @property
    def display_value(self) -> str:
        return f"{self._value}"

    @property
    def calculation_value(self) -> float:
        return self._value

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value

        return self.calculation_value == __value

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value

        return self.calculation_value < __value

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value

        return self.calculation_value <= __value

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value

        return self.calculation_value > __value

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value

        return self.calculation_value >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "DoubleValue":
        return DoubleValue(self._value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "DoubleValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = DoubleValue(deepcopy(self._value, memo))
        memo[id(self)] = new_copy

        return new_copy

class StringValue(QvdValue):
    """
    Represents a string value in a QVD file.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    def __init__(self, value: str):
        """
        Constructs a new string value.

        :param value: The string value.
        """
        self._value: str = value
        self._hash = None

    @property
    def display_value(self) -> str:
        return self._value

    @property
    def calculation_value(self) -> str:
        return self._value

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, str):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value

        return self.calculation_value == __value

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, str):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value

        return self.calculation_value < __value

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, str):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value

        return self.calculation_value <= __value

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, str):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value

        return self.calculation_value > __value

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, str):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value

        return self.calculation_value >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "StringValue":
        return StringValue(self._value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "StringValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = StringValue(deepcopy(self._value, memo))
        memo[id(self)] = new_copy

        return new_copy

class DualIntegerValue(QvdValue):
    """
    Represents a dual value with an integer value and a string value in a QVD file.
    
    Dual values are used to store both a display value and a calculation value in a single field.
    This is useful when the display representation of a value is different from the calculation
    representation. For example, you may want to display a date as "MM/DD/YYYY" but store it as
    an integer value representing the number of days since a certain date.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    def __init__(self, int_value: int, string_value: str):
        """
        Constructs a new dual integer value.

        :param int_value: The integer value.
        :param string_value: The string value.
        """
        self._int_value: int = int_value
        self._string_value: str = string_value
        self._hash = None

    @property
    def display_value(self) -> str:
        return self._string_value

    @property
    def calculation_value(self) -> int:
        return self._int_value

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value

        return self.calculation_value == __value

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value

        return self.calculation_value < __value

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value

        return self.calculation_value <= __value#

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value

        return self.calculation_value > __value

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, int):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value

        return self.calculation_value >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "DualIntegerValue":
        return DualIntegerValue(self._int_value, self._string_value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "DualIntegerValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = DualIntegerValue(deepcopy(self._int_value, memo), deepcopy(self._string_value, memo))
        memo[id(self)] = new_copy

        return new_copy

class DualDoubleValue(QvdValue):
    """
    Represents a dual value with a double value and a string value in a QVD file.

    Dual values are used to store both a display value and a calculation value in a single field.
    This is useful when the display representation of a value is different from the calculation
    representation. For example, you may want to display a monetary value as "$1,000.00" but store
    it as a double value representing the number of cents.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    def __init__(self, double_value: float, string_value: str):
        """
        Constructs a new dual double value.

        :param double_value: The double value.
        :param string_value: The string value.
        """
        self._double_value: float = double_value
        self._string_value: str = string_value
        self._hash = None

    @property
    def display_value(self) -> str:
        return self._string_value

    @property
    def calculation_value(self) -> float:
        return self._double_value

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value

        return self.calculation_value == __value

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value

        return self.calculation_value < __value

    def __le__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value

        return self.calculation_value <= __value

    def __gt__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value

        return self.calculation_value > __value

    def __ge__(self, __value: object) -> bool:
        if not isinstance(__value, QvdValue) and not isinstance(__value, float):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value

        return self.calculation_value >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "DualDoubleValue":
        return DualDoubleValue(self._double_value, self._string_value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "DualDoubleValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = DualDoubleValue(deepcopy(self._double_value, memo), deepcopy(self._string_value, memo))
        memo[id(self)] = new_copy

        return new_copy

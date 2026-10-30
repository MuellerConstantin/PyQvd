"""
Module contains the logical value types (date, time, timestamp, interval and money) that are built
on top of the physical dual value types.
"""

from copy import deepcopy
import datetime as dt
from decimal import Decimal
from typing import Dict
from pyqvd.qvd.values import QvdValue, DualIntegerValue, DualDoubleValue

class TimeValue(DualDoubleValue):
    """
    Represents a time value in a QVD file.

    Times are stored as dual double values where the double value represents the fraction of a day
    and the string value represents the time in a human-readable format. This data type does not
    exist in QVD files and is provided for convenience. In QVD files, times are stored as dual
    double values with a number format of "TIME" if the column is a uniform time column.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    @property
    def time(self) -> dt.time:
        """
        Returns the time value.

        :return: The time value.
        """
        return TimeValue._serial_number_to_time(self._double_value)

    def __eq__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.time)):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value == __value

        return self.time == __value

    def __lt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.time)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value < __value

        return self.time < __value

    def __le__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.time)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value <= __value

        return self.time <= __value

    def __gt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.time)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value > __value

        return self.time > __value

    def __ge__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.time)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value >= __value

        return self.time >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "TimeValue":
        return TimeValue(self._double_value, self._string_value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "TimeValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = TimeValue(deepcopy(self._double_value, memo), deepcopy(self._string_value, memo))
        memo[id(self)] = new_copy

        return new_copy

    @staticmethod
    def _time_to_serial_number(time: dt.time) -> float:
        # pylint: disable-next=invalid-name
        microseconds = ((time.hour * 60 + time.minute) * 60 + time.second) * 1_000_000 + time.microsecond
        serial_number = microseconds / 86_400_000_000

        return serial_number

    @staticmethod
    def _serial_number_to_time(serial_number: float) -> dt.time:
        frac = serial_number % 1.0  # time-of-day only
        total_us = round(frac * 86_400_000_000)  # microseconds in a day
        total_us %= 86_400_000_000  # wrap 24:00 → 00:00
        hours, rem = divmod(total_us, 3_600_000_000)
        minutes, rem = divmod(rem, 60_000_000)
        seconds, micros = divmod(rem, 1_000_000)
        return dt.time(int(hours), int(minutes), int(seconds), int(micros))

    @staticmethod
    def from_time(time: dt.time) -> "TimeValue":
        """
        Creates a new time value from a time.

        :param time: The time value.
        :return: The time value.
        """
        serial_number = TimeValue._time_to_serial_number(time)
        display_value = time.strftime("%H:%M:%S")

        return TimeValue(serial_number, display_value)

    @staticmethod
    def from_serial_number(serial_number: float) -> "TimeValue":
        """
        Creates a new time value from a serial number.

        :param serial_number: The serial number representing the time.
        :return: The time value.
        """
        time = TimeValue._serial_number_to_time(serial_number)
        display_value = time.strftime("%H:%M:%S")

        return TimeValue(serial_number, display_value)

class DateValue(DualIntegerValue):
    """
    Represents a date value in a QVD file.

    Dates are stored as dual integer values where the integer value represents the number of days
    since the base date (December 30, 1899) and the string value represents the date in a human-
    readable format. This data type does not exist in QVD files and is provided for convenience.
    In QVD files, dates are stored as dual integer values with a number format of "DATE" if the
    column is a uniform date column.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    @property
    def date(self) -> dt.date:
        """
        Returns the date value.

        :return: The date value.
        """
        return DateValue._serial_number_to_date(self._int_value)

    def __eq__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, int) and
            not isinstance(__value, dt.date)):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value
        if isinstance(__value, int):
            return self.calculation_value == __value

        return self.date == __value

    def __lt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, int) and
            not isinstance(__value, dt.date)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value
        if isinstance(__value, int):
            return self.calculation_value < __value

        return self.date < __value

    def __le__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, int) and
            not isinstance(__value, dt.date)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value
        if isinstance(__value, int):
            return self.calculation_value <= __value

        return self.date <= __value

    def __gt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, int) and
            not isinstance(__value, dt.date)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value
        if isinstance(__value, int):
            return self.calculation_value > __value

        return self.date > __value

    def __ge__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, int) and
            not isinstance(__value, dt.date)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value
        if isinstance(__value, int):
            return self.calculation_value >= __value

        return self.date >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "DateValue":
        return DateValue(self._int_value, self._string_value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "DateValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = DateValue(deepcopy(self._int_value, memo), deepcopy(self._string_value, memo))
        memo[id(self)] = new_copy

        return new_copy

    @staticmethod
    def _date_to_serial_number(date: dt.date) -> int:
        # pylint: disable-next=invalid-name
        BASE_DATE = dt.date(1899, 12, 30)
        delta = date - BASE_DATE
        serial_number = delta.days

        return serial_number

    @staticmethod
    def _serial_number_to_date(serial_number: int) -> dt.date:
        # pylint: disable-next=invalid-name
        BASE_DATE = dt.date(1899, 12, 30)
        delta = dt.timedelta(days=serial_number)
        date = BASE_DATE + delta

        return date

    @staticmethod
    def from_date(date: dt.date) -> "DateValue":
        """
        Creates a new date value from a date.

        :param date: The date value.
        :return: The date value.
        """
        serial_number = DateValue._date_to_serial_number(date)
        display_value = date.strftime("%Y-%m-%d")

        return DateValue(serial_number, display_value)

    @staticmethod
    def from_serial_number(serial_number: int) -> "DateValue":
        """
        Creates a new date value from a serial number.

        :param serial_number: The serial number representing the date.
        :return: The date value.
        """
        date = DateValue._serial_number_to_date(serial_number)
        display_value = date.strftime("%Y-%m-%d")

        return DateValue(serial_number, display_value)

class TimestampValue(DualDoubleValue):
    """
    Represents a timestamp value in a QVD file.

    Timestamps are stored as dual double values where the double value represents the fraction of a
    day and the string value represents the timestamp in a human-readable format. This data type does
    not exist in QVD files and is provided for convenience. In QVD files, timestamps are stored as
    dual double values with a number format of "DATETIME" if the column is a uniform timestamp column.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    @property
    def timestamp(self) -> dt.datetime:
        """
        Returns the timestamp value.

        :return: The timestamp value.
        """
        return TimestampValue._serial_number_to_timestamp(self._double_value)

    def __eq__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.datetime)):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value == __value

        return self.timestamp == __value

    def __lt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.datetime)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value < __value

        return self.timestamp < __value

    def __le__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.datetime)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value <= __value

        return self.timestamp <= __value

    def __gt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.datetime)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value > __value

        return self.timestamp > __value

    def __ge__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.datetime)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value >= __value

        return self.timestamp >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "TimestampValue":
        return TimestampValue(self._double_value, self._string_value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "TimestampValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = TimestampValue(deepcopy(self._double_value, memo), deepcopy(self._string_value, memo))
        memo[id(self)] = new_copy

        return new_copy

    @staticmethod
    def _timestamp_to_serial_number(timestamp: dt.datetime) -> float:
        # pylint: disable-next=invalid-name
        BASE_TIMESTAMP = dt.datetime(1899, 12, 30)
        delta = timestamp - BASE_TIMESTAMP
        excel_serial_date = delta / dt.timedelta(days=1)

        return excel_serial_date

    @staticmethod
    def _serial_number_to_timestamp(serial_number: float) -> dt.datetime:
        # pylint: disable-next=invalid-name
        BASE_TIMESTAMP = dt.datetime(1899, 12, 30)
        delta = dt.timedelta(days=serial_number)
        timestamp = BASE_TIMESTAMP + delta

        return timestamp

    @staticmethod
    def from_timestamp(timestamp: dt.datetime) -> "TimestampValue":
        """
        Creates a new timestamp value from a timestamp.

        :param timestamp: The timestamp or time value.
        :return: The timestamp value.
        """
        serial_number = TimestampValue._timestamp_to_serial_number(timestamp)
        display_value = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return TimestampValue(serial_number, display_value)

    @staticmethod
    def from_serial_number(serial_number: float) -> "TimestampValue":
        """
        Creates a new timestamp value from a serial number.

        :param serial_number: The serial number representing the timestamp.
        :return: The timestamp value.
        """
        timestamp = TimestampValue._serial_number_to_timestamp(serial_number)
        display_value = timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return TimestampValue(serial_number, display_value)

class IntervalValue(DualDoubleValue):
    """
    Represents an interval value in a QVD file.

    Intervals are stored as dual double values where the double value represents the fraction of a
    day and the string value represents the interval in a human-readable format. This data type does
    not exist in QVD files and is provided for convenience. In QVD files, intervals are stored as
    dual double values with a number format of "INTERVAL" if the column is a uniform interval column.

    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    @property
    def interval(self) -> dt.timedelta:
        """
        Returns the interval value.

        :return: The interval value.
        """
        return IntervalValue._serial_number_to_interval(self._double_value)

    def __eq__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.timedelta)):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value == __value

        return self.interval == __value

    def __lt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.timedelta)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value < __value

        return self.interval < __value

    def __le__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.timedelta)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value <= __value

        return self.interval <= __value

    def __gt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.timedelta)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value > __value

        return self.interval > __value

    def __ge__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, dt.timedelta)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value >= __value

        return self.interval >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "IntervalValue":
        return IntervalValue(self._double_value, self._string_value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "IntervalValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = IntervalValue(deepcopy(self._double_value, memo), deepcopy(self._string_value, memo))
        memo[id(self)] = new_copy

        return new_copy

    @staticmethod
    def _interval_to_serial_number(interval: dt.timedelta) -> float:
        return interval / dt.timedelta(days=1)

    @staticmethod
    def _serial_number_to_interval(serial_number: float) -> dt.timedelta:
        # timedelta rounds to the nearest microsecond, truncating would turn floating point
        # inaccuracies such as 61.99999 seconds into a whole second less
        return dt.timedelta(days=serial_number)

    @staticmethod
    def from_interval(interval: dt.timedelta) -> "IntervalValue":
        """
        Creates a new interval value from an interval.

        :param interval: The interval value.
        :return: The interval value.
        """
        serial_number = IntervalValue._interval_to_serial_number(interval)

        days = interval.days
        hours, seconds = divmod(interval.seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)

        display_value = f"{days} {hours:02}:{minutes:02}:{seconds:02}"

        return IntervalValue(serial_number, display_value)

    @staticmethod
    def from_serial_number(serial_number: float) -> "IntervalValue":
        """
        Creates a new interval value from a serial number.

        :param serial_number: The serial number representing the interval.
        :return: The interval value.
        """
        interval = IntervalValue._serial_number_to_interval(serial_number)

        days = interval.days
        hours, seconds = divmod(interval.seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)

        display_value = f"{days} {hours:02}:{minutes:02}:{seconds:02}"

        return IntervalValue(serial_number, display_value)

class MoneyValue(DualDoubleValue):
    """
    Represents a money value in a QVD file. Money values are stored as dual double values where the
    double value represents the monetary value and the string value represents the money in a human-
    readable format. This data type does not exist in QVD files and is provided for convenience. In
    QVD files, money values are stored as dual double values with a number format of "MONEY" if the
    column is a uniform money column.

    .. important::

        It is important to note that Python does not have a built-in money data type. This class is
        provided as a convenience for working with money values in QVD files. It is recommended to use
        the ``decimal.Decimal`` class for monetary calculations in Python. Because it is not possible to
        differ between a ``decimal.Decimal`` value that is representing money and a ``decimal.Decimal``
        value that is representing a non-monetary value, all ``decimal.Decimal`` values are considered
        to be monetary values and will therefore be converted to ``MoneyValue`` objects when importing
        data from a dictionary or a pandas DataFrame for example.
    
    .. important::

        Instances of this class are immutable. After initialization, attributes
        should not be modified. This guarantees stable hashing and allows instances
        to be safely used as dictionary keys or set members.
    """
    @property
    def money(self) -> Decimal:
        """
        Returns the money value.

        :return: The money value.
        """
        return Decimal.from_float(self._double_value)

    def __eq__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, Decimal)):
            return False

        if isinstance(__value, QvdValue):
            return self.calculation_value == __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value == __value

        return self.money == __value

    def __lt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, Decimal)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value < __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value < __value

        return self.money < __value

    def __le__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, Decimal)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value <= __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value <= __value

        return self.money <= __value

    def __gt__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, Decimal)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value > __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value > __value

        return self.money > __value

    def __ge__(self, __value: object) -> bool:
        if (not isinstance(__value, QvdValue) and
            not isinstance(__value, float) and
            not isinstance(__value, Decimal)):
            return NotImplemented

        if isinstance(__value, QvdValue):
            return self.calculation_value >= __value.calculation_value
        if isinstance(__value, float):
            return self.calculation_value >= __value

        return self.money >= __value

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.calculation_value)

        return self._hash

    def __copy__(self) -> "MoneyValue":
        return MoneyValue(self._double_value, self._string_value)

    def __deepcopy__(self, memo: Dict[int, object]) -> "MoneyValue":
        if id(self) in memo:
            return memo[id(self)]

        new_copy = MoneyValue(deepcopy(self._double_value, memo), deepcopy(self._string_value, memo))
        memo[id(self)] = new_copy

        return new_copy

    @staticmethod
    def from_money(money: Decimal) -> "MoneyValue":
        """
        Creates a new money value from a money value.

        :param money: The money value.
        :return: The money value.
        """
        display_value = f"$ {money:,.2f}"
        calculation_value = float(money)

        return MoneyValue(calculation_value, display_value)

    @staticmethod
    def from_serial_number(serial_number: float) -> "MoneyValue":
        """
        Creates a new money value from a serial number.

        :param serial_number: The serial number representing the money.
        :return: The money value.
        """
        money = Decimal.from_float(serial_number)
        display_value = f"$ {money:,.2f}"

        return MoneyValue(serial_number, display_value)

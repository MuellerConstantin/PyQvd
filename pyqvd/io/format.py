"""
Module for handling QVD values and formats.
"""

from datetime import datetime
from typing import Literal, Mapping, Callable
from pyqvd.qvd import DateValue, TimeValue, TimestampValue, IntervalValue, MoneyValue

DATETIME_FORMAT_TOKENS: Mapping[str, Callable[[datetime], str]] = {
    "YYYY": lambda value: value.strftime("%Y"),
    "YY": lambda value: value.strftime("%y"),
    "MMMM": lambda value: value.strftime("%B"),
    "MMM": lambda value: value.strftime("%b"),
    "MM": lambda value: value.strftime("%m"),
    "DD": lambda value: value.strftime("%d"),
    "hh": lambda value: value.strftime("%H"),
    "HH": lambda value: value.strftime("%I"),
    "mm": lambda value: value.strftime("%M"),
    "ss": lambda value: value.strftime("%S"),
    "ffffff": lambda value: value.strftime("%f"),
    "fffff": lambda value: value.strftime("%f")[:-1],
    "ffff": lambda value: value.strftime("%f")[:-2],
    "fff": lambda value: value.strftime("%f")[:-3],
    "ff": lambda value: value.strftime("%f")[:-4],
    "f": lambda value: value.strftime("%f")[:-5],
    "tt": lambda value: value.strftime("%p"),
}

INTERVAL_FORMAT_TOKENS = {
    "D",
    "hh",
    "mm",
    "ss",
    "ffffff",
    "fffff",
    "ffff",
    "fff",
    "ff",
    "f",
}

class DateValueFormatter:
    """
    Class for formatting date values.
    """
    def __init__(self, qvd_format: str):
        self._qvd_format = qvd_format

    def format(self, value: DateValue) -> str:
        """
        Format the date value.
        """
        result = self._qvd_format

        for qvd_token, transformer in DATETIME_FORMAT_TOKENS.items():
            result = result.replace(qvd_token, transformer(value.date))

        return result

    def get_qvd_format_string(self) -> str:
        """
        Get the QVD format string.
        """
        return self._qvd_format

class TimeValueFormatter:
    """
    Class for formatting time values.
    """
    def __init__(self, qvd_format: str):
        self._qvd_format = qvd_format

    def format(self, value: TimeValue) -> str:
        """
        Format the time value.
        """
        result = self._qvd_format

        for qvd_token, transformer in DATETIME_FORMAT_TOKENS.items():
            result = result.replace(qvd_token, transformer(value.time))

        return result

    def get_qvd_format_string(self) -> str:
        """
        Get the QVD format string.
        """
        return self._qvd_format

class TimestampValueFormatter:
    """
    Class for formatting timestamp values.
    """
    def __init__(self, qvd_format: str):
        self._qvd_format = qvd_format

    def format(self, value: TimestampValue) -> str:
        """
        Format the timestamp value.
        """
        result = self._qvd_format

        for qvd_token, transformer in DATETIME_FORMAT_TOKENS.items():
            result = result.replace(qvd_token, transformer(value.timestamp))

        return result

    def get_qvd_format_string(self) -> str:
        """
        Get the QVD format string.
        """
        return self._qvd_format

class IntervalValueFormatter:
    """
    Class for formatting interval values.
    """
    def __init__(self, qvd_format: str):
        self._qvd_format = qvd_format

    def format(self, value: IntervalValue) -> str:
        """
        Format the interval value.
        """
        days_present = "D" in self._qvd_format
        hours_present = "hh" in self._qvd_format
        minutes_present = "mm" in self._qvd_format

        days = value.interval.days
        hours, seconds = divmod(value.interval.seconds, 60 * 60)
        minutes, seconds = divmod(seconds, 60)

        result = self._qvd_format

        for qvd_token in INTERVAL_FORMAT_TOKENS:
            if qvd_token == "D":
                result = result.replace(qvd_token, str(days))
            elif qvd_token == "hh":
                if not days_present:
                    result = result.replace(qvd_token, str(hours + days * 24).zfill(2))
                else:
                    result = result.replace(qvd_token, str(hours).zfill(2))
            elif qvd_token == "mm":
                if not hours_present:
                    if not days_present:
                        result = result.replace(qvd_token, str(minutes + (hours + days * 24) * 60).zfill(2))
                    else:
                        result = result.replace(qvd_token, str(minutes + hours * 60).zfill(2))
                else:
                    result = result.replace(qvd_token, str(minutes).zfill(2))
            elif qvd_token == "ss":
                if not minutes_present:
                    if not hours_present:
                        if not days_present:
                            result = result.replace(qvd_token,
                                                    str(seconds + (minutes + (hours + days * 24) * 60) * 60).zfill(2))
                        else:
                            result = result.replace(qvd_token, str(seconds + (minutes + hours * 60) * 60).zfill(2))
                    else:
                        result = result.replace(qvd_token, str(seconds + minutes * 60).zfill(2))
                else:
                    result = result.replace(qvd_token, str(seconds).zfill(2))
            elif qvd_token in {"f", "ff", "fff", "ffff", "fffff", "ffffff"}:
                milliseconds_length = len(qvd_token)
                milliseconds = value.interval.microseconds // 1000
                result = result.replace(qvd_token, str(milliseconds).zfill(milliseconds_length))

        return result

    def get_qvd_format_string(self) -> str:
        """
        Get the QVD format string.
        """
        return self._qvd_format

class MoneyValueFormatter:
    """
    Class for formatting money values.
    """
    def __init__(self, thousand_separator: str = None,
                 decimal_separator: str = ".",
                 currency_symbol: str = None,
                 currency_symbol_position: Literal["precede", "follow"] = "precede",
                 currency_symbol_space_separated: bool = False,
                 decimal_precision: int = 2):
        self._thousand_separator = thousand_separator if thousand_separator else ""
        self._decimal_separator = decimal_separator if decimal_separator else "."
        self._currency_symbol = currency_symbol if currency_symbol else ""
        self._currency_symbol_position = currency_symbol_position
        self._currency_symbol_space_separated = currency_symbol_space_separated
        self._decimal_precision = decimal_precision

    @property
    def thousand_separator(self) -> str:
        """
        Get the thousand separator.
        """
        return self._thousand_separator

    @property
    def decimal_separator(self) -> str:
        """
        Get the decimal separator.
        """
        return self._decimal_separator

    @property
    def currency_symbol(self) -> str:
        """
        Get the currency symbol.
        """
        return self._currency_symbol

    @property
    def currency_symbol_position(self) -> Literal["precede", "follow"]:
        """
        Get the currency symbol position.
        """
        return self._currency_symbol_position

    @property
    def currency_symbol_space_separated(self) -> bool:
        """
        Get whether the currency symbol is space separated.
        """
        return self._currency_symbol_space_separated

    @property
    def decimal_precision(self) -> int:
        """
        Get the decimal precision.
        """
        return self._decimal_precision

    def format(self, value: MoneyValue) -> str:
        """
        Format the money value.
        """
        formatted_value = ""

        if self._currency_symbol and self._currency_symbol_position == "precede":
            formatted_value += self._currency_symbol

            if self._currency_symbol_space_separated:
                formatted_value += " "

        if self._thousand_separator:
            formatted_value += f"{value.money:,.{self._decimal_precision}f}"

            if self._decimal_separator != ".":
                formatted_value = formatted_value.replace(".", "\0")

            if self._thousand_separator != ",":
                formatted_value = formatted_value.replace(",", self._thousand_separator)

            if self._decimal_separator != ".":
                formatted_value = formatted_value.replace("\0", self._decimal_separator)
        else:
            formatted_value += f"{value.money:.{self._decimal_precision}f}"

            if self._decimal_separator != ".":
                formatted_value = formatted_value.replace(".", self._decimal_separator)

        if self._currency_symbol and self._currency_symbol_position == "follow":
            if self._currency_symbol_space_separated:
                formatted_value += " "

            formatted_value += self._currency_symbol

        return formatted_value

    def get_qvd_format_string(self) -> str:
        """
        Get the QVD format string.
        """
        qvd_format_positive = ""
        qvd_format_negative = ""

        if self._currency_symbol and self._currency_symbol_position == "precede":
            qvd_format_positive += self._currency_symbol
            qvd_format_negative += self._currency_symbol

            if self._currency_symbol_space_separated:
                qvd_format_positive += " "
                qvd_format_negative += " "

        qvd_format_negative += "-"

        if self._thousand_separator:
            qvd_format_positive += f"#{self._thousand_separator}##"
            qvd_format_negative += f"#{self._thousand_separator}##"
        else:
            qvd_format_positive += "###"
            qvd_format_negative += "###"

        qvd_format_positive += f"0{self._decimal_separator}{'0' * self._decimal_precision}"
        qvd_format_negative += f"0{self._decimal_separator}{'0' * self._decimal_precision}"

        if self._currency_symbol and self._currency_symbol_position == "follow":
            if self._currency_symbol_space_separated:
                qvd_format_positive += " "
                qvd_format_negative += " "

            qvd_format_positive += self._currency_symbol
            qvd_format_negative += self._currency_symbol

        return f"{qvd_format_positive};{qvd_format_negative}"

"""
Test the format module.
"""

from datetime import datetime
from decimal import Decimal
from pyqvd import DateValue, TimeValue, TimestampValue, IntervalValue, MoneyValue
from pyqvd.io.format import (DateValueFormatter, TimeValueFormatter, TimestampValueFormatter,
                             IntervalValueFormatter, MoneyValueFormatter)

def test_date_value_formatter_with_format0():
    """
    Test the DateValueFormatter class with format "YYYY-MM-DD".
    """
    formatter = DateValueFormatter("YYYY-MM-DD")
    date_value = DateValue.from_date(datetime(2021, 1, 1).date())
    assert formatter.format(date_value) == "2021-01-01"
    assert formatter.get_qvd_format_string() == "YYYY-MM-DD"

def test_date_value_formatter_with_format1():
    """
    Test the DateValueFormatter class with format "DD.MM.YYYY".
    """
    formatter = DateValueFormatter("DD.MM.YYYY")
    date_value = DateValue.from_date(datetime(2021, 1, 1).date())
    assert formatter.format(date_value) == "01.01.2021"
    assert formatter.get_qvd_format_string() == "DD.MM.YYYY"

def test_date_value_formatter_with_format2():
    """
    Test the DateValueFormatter class with format "MM/DD/YYYY".
    """
    formatter = DateValueFormatter("MM/DD/YYYY")
    date_value = DateValue.from_date(datetime(2021, 1, 1).date())
    assert formatter.format(date_value) == "01/01/2021"
    assert formatter.get_qvd_format_string() == "MM/DD/YYYY"

def test_date_value_formatter_with_format3():
    """
    Test the DateValueFormatter class with format "YYYY-MM-DD hh:mm:ss".
    """
    formatter = DateValueFormatter("YYYY-MM-DD hh:mm:ss")
    date_value = DateValue.from_date(datetime(2021, 1, 1).date())
    assert formatter.format(date_value) == "2021-01-01 00:00:00"
    assert formatter.get_qvd_format_string() == "YYYY-MM-DD hh:mm:ss"

def test_time_value_formatter_with_format0():
    """
    Test the TimeValueFormatter class with format "hh:mm:ss".
    """
    formatter = TimeValueFormatter("hh:mm:ss")
    time_value = TimeValue.from_time(datetime(2021, 1, 1, 12, 52, 11).time())
    assert formatter.format(time_value) == "12:52:11"
    assert formatter.get_qvd_format_string() == "hh:mm:ss"

def test_time_value_formatter_with_format1():
    """
    Test the TimeValueFormatter class with format "hh:mm:ss.ffffff".
    """
    formatter = TimeValueFormatter("hh:mm:ss.ffffff")
    time_value = TimeValue.from_time(datetime(2021, 1, 1, 12, 52, 11).time())
    assert formatter.format(time_value) == "12:52:11.000000"
    assert formatter.get_qvd_format_string() == "hh:mm:ss.ffffff"

def test_time_value_formatter_with_format2():
    """
    Test the TimeValueFormatter class with format "hh:mm:ss.fff".
    """
    formatter = TimeValueFormatter("hh:mm:ss.fff")
    time_value = TimeValue.from_time(datetime(2021, 1, 1, 12, 52, 11).time())
    assert formatter.format(time_value) == "12:52:11.000"
    assert formatter.get_qvd_format_string() == "hh:mm:ss.fff"

def test_time_value_formatter_with_format3():
    """
    Test the TimeValueFormatter class with format "hh:mm:ss.ff".
    """
    formatter = TimeValueFormatter("hh:mm:ss.ff")
    time_value = TimeValue.from_time(datetime(2021, 1, 1, 12, 52, 11).time())
    assert formatter.format(time_value) == "12:52:11.00"
    assert formatter.get_qvd_format_string() == "hh:mm:ss.ff"

def test_time_value_formatter_with_format4():
    """
    Test the TimeValueFormatter class with format "HH:mm:ss.ff tt".
    """
    formatter = TimeValueFormatter("HH:mm:ss.ff tt")
    time_value = TimeValue.from_time(datetime(2021, 1, 1, 21, 52, 11).time())
    assert formatter.format(time_value) == "09:52:11.00 PM"
    assert formatter.get_qvd_format_string() == "HH:mm:ss.ff tt"

def test_timestamp_value_formatter_with_format0():
    """
    Test the TimestampValueFormatter class with format "YYYY-MM-DD hh:mm:ss".
    """
    formatter = TimestampValueFormatter("YYYY-MM-DD hh:mm:ss")
    timestamp_value = TimestampValue.from_timestamp(datetime(2021, 1, 1, 12, 52, 11))
    assert formatter.format(timestamp_value) == "2021-01-01 12:52:11"
    assert formatter.get_qvd_format_string() == "YYYY-MM-DD hh:mm:ss"

def test_timestamp_value_formatter_with_format1():
    """
    Test the TimestampValueFormatter class with format "YYYY-MM-DD hh:mm:ss.ffffff".
    """
    formatter = TimestampValueFormatter("YYYY-MM-DD hh:mm:ss.ffffff")
    timestamp_value = TimestampValue.from_timestamp(datetime(2021, 1, 1, 12, 52, 11))
    assert formatter.format(timestamp_value) == "2021-01-01 12:52:11.000000"
    assert formatter.get_qvd_format_string() == "YYYY-MM-DD hh:mm:ss.ffffff"

def test_timestamp_value_formatter_with_format2():
    """
    Test the TimestampValueFormatter class with format "YYYY-MM-DD hh:mm:ss.fff".
    """
    formatter = TimestampValueFormatter("YYYY-MM-DD hh:mm:ss.fff")
    timestamp_value = TimestampValue.from_timestamp(datetime(2021, 1, 1, 12, 52, 11))
    assert formatter.format(timestamp_value) == "2021-01-01 12:52:11.000"
    assert formatter.get_qvd_format_string() == "YYYY-MM-DD hh:mm:ss.fff"

def test_timestamp_value_formatter_with_format3():
    """
    Test the TimestampValueFormatter class with format "YYYY-MM-DD hh:mm:ss.ff".
    """
    formatter = TimestampValueFormatter("YYYY-MM-DD hh:mm:ss.ff")
    timestamp_value = TimestampValue.from_timestamp(datetime(2021, 1, 1, 12, 52, 11))
    assert formatter.format(timestamp_value) == "2021-01-01 12:52:11.00"
    assert formatter.get_qvd_format_string() == "YYYY-MM-DD hh:mm:ss.ff"

def test_timestamp_value_formatter_with_format4():
    """
    Test the TimestampValueFormatter class with format "YYYY-MM-DD HH:mm:ss.ff tt".
    """
    formatter = TimestampValueFormatter("YYYY-MM-DD HH:mm:ss.ff tt")
    timestamp_value = TimestampValue.from_timestamp(datetime(2021, 1, 1, 21, 52, 11))
    assert formatter.format(timestamp_value) == "2021-01-01 09:52:11.00 PM"
    assert formatter.get_qvd_format_string() == "YYYY-MM-DD HH:mm:ss.ff tt"

def test_interval_value_formatter_with_format0():
    """
    Test the IntervalValueFormatter class with format "D hh:mm:ss".
    """
    formatter = IntervalValueFormatter("D hh:mm:ss")
    interval_value = IntervalValue.from_interval(datetime(2021, 1, 1, 12, 52, 11) - datetime(2021, 1, 1, 0, 0, 0))
    assert formatter.format(interval_value) == "0 12:52:11"
    assert formatter.get_qvd_format_string() == "D hh:mm:ss"

def test_interval_value_formatter_with_format1():
    """
    Test the IntervalValueFormatter class with format "hh:mm:ss".
    """
    formatter = IntervalValueFormatter("hh:mm:ss")
    interval_value = IntervalValue.from_interval(datetime(2021, 1, 1, 12, 52, 11) - datetime(2021, 1, 1, 0, 0, 0))
    assert formatter.format(interval_value) == "12:52:11"
    assert formatter.get_qvd_format_string() == "hh:mm:ss"

def test_interval_value_formatter_with_format2():
    """
    Test the IntervalValueFormatter class with format "hh:mm:ss.ffffff".
    """
    formatter = IntervalValueFormatter("hh:mm:ss.ffffff")
    interval_value = IntervalValue.from_interval(datetime(2021, 1, 1, 12, 52, 11) - datetime(2021, 1, 1, 0, 0, 0))
    assert formatter.format(interval_value) == "12:52:11.000000"
    assert formatter.get_qvd_format_string() == "hh:mm:ss.ffffff"

def test_interval_value_formatter_with_format3():
    """
    Test the IntervalValueFormatter class with format "mm:ss.fff".
    """
    formatter = IntervalValueFormatter("mm:ss.fff")
    interval_value = IntervalValue.from_interval(datetime(2021, 1, 1, 12, 52, 11) - datetime(2021, 1, 1, 0, 0, 0))
    assert formatter.format(interval_value) == "772:11.000"
    assert formatter.get_qvd_format_string() == "mm:ss.fff"

def test_interval_value_formatter_with_format4():
    """
    Test the IntervalValueFormatter class with format "ss.ffffff".
    """
    formatter = IntervalValueFormatter("ss.ffffff")
    interval_value = IntervalValue.from_interval(datetime(2021, 1, 1, 12, 52, 11) - datetime(2021, 1, 1, 0, 0, 0))
    assert formatter.format(interval_value) == "46331.000000"
    assert formatter.get_qvd_format_string() == "ss.ffffff"

def test_money_value_formatter_with_format0():
    """
    Test the MoneyValueFormatter class with format "$ #,##0.00".
    """
    formatter = MoneyValueFormatter(currency_symbol="$", decimal_separator=".",
                                    thousand_separator=",", currency_symbol_position="precede",
                                    currency_symbol_space_separated=True)
    money_value = MoneyValue.from_money(Decimal.from_float(12213.45))
    assert formatter.format(money_value) == "$ 12,213.45"
    assert formatter.get_qvd_format_string() == "$ #,##0.00;$ -#,##0.00"

def test_money_value_formatter_with_format1():
    """
    Test the MoneyValueFormatter class with format "#.##0,00 €".
    """
    formatter = MoneyValueFormatter(currency_symbol="€", decimal_separator=",",
                                    thousand_separator=".", currency_symbol_position="follow",
                                    currency_symbol_space_separated=True)
    money_value = MoneyValue.from_money(Decimal.from_float(12213.45))
    assert formatter.format(money_value) == "12.213,45 €"
    assert formatter.get_qvd_format_string() == "#.##0,00 €;-#.##0,00 €"

def test_money_value_formatter_with_format2():
    """
    Test the MoneyValueFormatter class with format "###0.00".
    """
    formatter = MoneyValueFormatter(decimal_separator=".")
    money_value = MoneyValue.from_money(Decimal.from_float(12213.45))
    assert formatter.format(money_value) == "12213.45"
    assert formatter.get_qvd_format_string() == "###0.00;-###0.00"

def test_money_value_formatter_with_format3():
    """
    Test the MoneyValueFormatter class with format "###0.0000".
    """
    formatter = MoneyValueFormatter(decimal_separator=".", decimal_precision=4)
    money_value = MoneyValue.from_money(Decimal.from_float(12213.4533))
    assert formatter.format(money_value) == "12213.4533"
    assert formatter.get_qvd_format_string() == "###0.0000;-###0.0000"

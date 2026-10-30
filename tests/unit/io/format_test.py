"""
Test the format module.
"""

from datetime import datetime, timedelta
from decimal import Decimal
import pytest
from pyqvd import DateValue, TimeValue, TimestampValue, IntervalValue, MoneyValue
from pyqvd.io.format import (DATETIME_FORMAT_TOKENS, DateValueFormatter, TimeValueFormatter,
                             TimestampValueFormatter, IntervalValueFormatter, MoneyValueFormatter)

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

@pytest.mark.parametrize(
    "qvd_format, expected",
    [
        ("ss.f", "62.0"),
        ("ss.ff", "62.00"),
        ("ss.fff", "62.005"),
        ("ss.ffff", "62.0050"),
        ("ss.fffff", "62.00500"),
        ("ss.ffffff", "62.005000"),
        ("mm:ss.fff", "01:02.005"),
    ],
)
def test_interval_value_formatter_with_fractional_seconds(qvd_format: str, expected: str):
    """
    Test the IntervalValueFormatter class with fractional second tokens, which have to yield the
    leading digits of the fraction and must not interfere with each other.
    """
    formatter = IntervalValueFormatter(qvd_format)
    interval_value = IntervalValue.from_interval(timedelta(minutes=1, seconds=2, milliseconds=5))
    assert formatter.format(interval_value) == expected

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

@pytest.mark.parametrize(
    "formatter, value, expected",
    [
        (DateValueFormatter("YY-MM-DD"), DateValue.from_date(datetime(2021, 3, 7).date()), "21-03-07"),
        (DateValueFormatter("DD. MMMM YYYY"), DateValue.from_date(datetime(2021, 3, 7).date()), "07. March 2021"),
        (DateValueFormatter("MMM DD, YYYY"), DateValue.from_date(datetime(2021, 3, 7).date()), "Mar 07, 2021"),
        (DateValueFormatter("YYYY/YYYY"), DateValue.from_date(datetime(2021, 3, 7).date()), "2021/2021"),
        (DateValueFormatter("Datum"), DateValue.from_date(datetime(2021, 3, 7).date()), "Datum"),
        (TimeValueFormatter("HH:mm tt"), TimeValue.from_time(datetime(2021, 3, 7, 14, 5, 9).time()), "02:05 PM"),
        (TimeValueFormatter("hh-mm-ss"), TimeValue.from_time(datetime(2021, 3, 7, 14, 5, 9).time()), "14-05-09"),
        (TimestampValueFormatter("DD.MM.YY HH:mm:ss tt"),
         TimestampValue.from_timestamp(datetime(2021, 3, 7, 14, 5, 9)), "07.03.21 02:05:09 PM"),
        (TimestampValueFormatter("MMMM YYYY"),
         TimestampValue.from_timestamp(datetime(2021, 3, 7, 14, 5, 9)), "March 2021"),
    ],
)
def test_datetime_value_formatters_with_distinct_fields(formatter, value, expected: str):
    """
    Test the date, time and timestamp formatters with values whose fields all differ, so that
    mixed up tokens are detected.
    """
    assert formatter.format(value) == expected

def _format_with_every_token(qvd_format: str, value: datetime) -> str:
    """
    Reference implementation replacing every supported token in its defined order.
    """
    result = qvd_format

    for qvd_token, transformer in DATETIME_FORMAT_TOKENS.items():
        result = result.replace(qvd_token, transformer(value))

    return result

REFERENCE_FORMATS = [
    "YYYY-MM-DD hh:mm:ss",
    "YYYY YY MMMM MMM MM DD hh HH mm ss ffffff fffff ffff fff ff f tt",
    "YYYYY MMMMM fffffff ttt",
    "DD/MM/YYYY HH:mm tt",
    "plain text",
    "",
]

REFERENCE_DATETIMES = [
    datetime(2021, 3, 7, 14, 5, 9),
    datetime(1999, 12, 31, 0, 0, 0),
    datetime(2024, 2, 29, 23, 59, 59),
    datetime(2000, 7, 1, 9, 30, 0),
]

@pytest.mark.parametrize("qvd_format", REFERENCE_FORMATS)
@pytest.mark.parametrize("moment", REFERENCE_DATETIMES)
def test_datetime_value_formatters_match_reference(qvd_format: str, moment: datetime):
    """
    Test if the date, time and timestamp formatters yield exactly the result of replacing every
    token in order, including overlapping and repeated tokens.
    """
    date_value = DateValue.from_date(moment.date())
    time_value = TimeValue.from_time(moment.time())
    timestamp_value = TimestampValue.from_timestamp(moment)

    assert DateValueFormatter(qvd_format).format(date_value) == \
        _format_with_every_token(qvd_format, date_value.date)
    assert TimeValueFormatter(qvd_format).format(time_value) == \
        _format_with_every_token(qvd_format, time_value.time)
    assert TimestampValueFormatter(qvd_format).format(timestamp_value) == \
        _format_with_every_token(qvd_format, timestamp_value.timestamp)

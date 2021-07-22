import datetime
from enum import Enum

from inventories.models import (
    Transaction, MaterialGroup, Material,
    balance, movement_between, weighted_avg_price, period_weighted_avg_price
)

class Resolution(Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'

def datetime_range(start=None, end=None, resolution=Resolution.DAY):
    """
    Yields tuples (start_of_period, end_of_period).
    If resolution is Resolution.DAY, returns all days between and including 'start' and 'end'.
    If resolution is Resolution.WEEK, returns all weeks (from Monday to Sunday) between and including 'start' and 'end'.
    If resolution is Resolution.MONTH, returns all weeks (from 1 to end_of_month) between and including 'start' and 'end'.
    """
    assert isinstance(resolution, Resolution)
    
    def monthdelta(date, months):
        day, month, year = date.day, (date.month + months - 1) % 12 + 1, date.year + (date.month + months - 1) // 12
        return datetime.datetime(year, month, day, tzinfo=date.tzinfo) - date
    
    if resolution == Resolution.DAY:
        start_of_period = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_period = start_of_period + datetime.timedelta(days=1, microseconds=-1)
        last_period_end = end.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1, microseconds=-1)
        while end_of_period.date() <= last_period_end.date():
            yield (start_of_period, end_of_period)
            start_of_period = start_of_period + datetime.timedelta(days=1)
            end_of_period = start_of_period + datetime.timedelta(days=1, microseconds=-1)

    elif resolution == Resolution.WEEK:
        start_of_period = (start - datetime.timedelta(days=start.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_period = start_of_period + datetime.timedelta(days=7, microseconds=-1)
        last_period_end = end - datetime.timedelta(days=end.weekday()) + datetime.timedelta(days=7, microseconds=-1)
        while end_of_period.date() <= last_period_end.date():
            yield (start_of_period, end_of_period)
            start_of_period = start_of_period + datetime.timedelta(days=7)
            end_of_period = start_of_period + datetime.timedelta(days=7, microseconds=-1)

    elif resolution == Resolution.MONTH:
        start_of_period = start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_of_period = start_of_period + monthdelta(start_of_period, months=1) - datetime.timedelta(microseconds=1)
        last_period_end = end.replace(day=1) + monthdelta(end.replace(day=1), months=1) - datetime.timedelta(microseconds=1)
        while end_of_period.date() <= last_period_end.date():
            yield (start_of_period, end_of_period)
            start_of_period = start_of_period + monthdelta(start_of_period, months=1) 
            end_of_period = start_of_period + monthdelta(start_of_period, months=1) - datetime.timedelta(microseconds=1)


# def daily_material_report(date_from, date_to, material):
#     qty_closing = None
#     report = []
#     for start_of_period, end_of_period in datetime_range(start=date_from, end=date_to, resolution=Resolution.DAY):
#         qty_opening = qty_closing or material.balance_at(start_of_period - datetime.timedelta(days=1))
#         qty_in = material.movement_between(Transaction.TYPE_IN, start_of_period, end_of_period)
#         qty_out = material.movement_between(Transaction.TYPE_OUT, start_of_period, end_of_period)
#         qty_closing = qty_opening + qty_in - qty_out
#         data = {
#             'start_of_period': start_of_period,
#             'end_of_period': end_of_period,
#             'qty_opening': qty_opening,
#             'qty_in': qty_in,
#             'qty_out': qty_out,
#             'qty_closing': qty_closing,
#         }
#         report.append(data)
#     return report

def generate_report(date_from, date_to, resolution, filter_by=None):
    assert isinstance(date_from, datetime.datetime)
    assert isinstance(date_to, datetime.datetime)
    assert isinstance(resolution, Resolution)
    assert isinstance(filter_by, (MaterialGroup, Material)) or filter_by is None
    
    qty_closing = None
    price_closing = None
    report = []
    for start_of_period, end_of_period in datetime_range(start=date_from, end=date_to, resolution=resolution):
        qty_opening = qty_closing if qty_closing is not None else balance(start_of_period - datetime.timedelta(microseconds=1), filter_by)
        qty_in = movement_between(Transaction.TYPE_IN, start_of_period, end_of_period, filter_by)
        qty_out = movement_between(Transaction.TYPE_OUT, start_of_period, end_of_period, filter_by)
        qty_closing = qty_opening + qty_in - qty_out
        price_opening = price_closing if price_closing is not None else weighted_avg_price(start_of_period - datetime.timedelta(microseconds=1), filter_by)
        price_in = period_weighted_avg_price(Transaction.TYPE_IN, start_of_period, end_of_period, filter_by)
        price_out = period_weighted_avg_price(Transaction.TYPE_OUT, start_of_period, end_of_period, filter_by)
        price_closing = weighted_avg_price(end_of_period, filter_by)
        val_opening = qty_opening * price_opening
        val_in = qty_in * price_in
        val_out = qty_out * price_out
        val_closing = qty_closing * price_closing
        data = {
            'start_of_period': start_of_period.strftime('%Y-%m-%d'),
            'end_of_period': end_of_period.strftime('%Y-%m-%d'),
            'qty_opening': qty_opening,
            'qty_in': qty_in,
            'qty_out': qty_out,
            'qty_closing': qty_closing,
            'val_opening': val_opening,
            'val_in': val_in,
            'val_out': val_out,
            'val_closing': val_closing,
            'price_opening': price_opening,
            'price_in': price_in,
            'price_out': price_out,
            'price_closing': price_closing,
        }
        report.append(data)
    print(report)
    return report
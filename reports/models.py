import datetime
from enum import Enum

from inventories.models import (
    Transaction, MaterialGroup, Material,
    balance, movement_between, sales_and_purchases, weighted_avg_price, period_weighted_avg_price
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


def normalized(data):
    assert isinstance(data, list)

    if len(data) == 0:
        return []

    sum_of_data = sum(data)
    if sum_of_data == 0:
        return []
    
    return [x / sum_of_data for x in data]

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

def summary_report(date_from, date_to, resolution, filter_by=None):
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
            'start_of_period':  start_of_period.strftime('%Y-%m-%d'),
            'end_of_period':    end_of_period.strftime('%Y-%m-%d'),
            'qty_opening':      round(float(qty_opening), 2),
            'qty_in':           round(float(qty_in), 2),
            'qty_out':          round(float(qty_out), 2),
            'qty_closing':      round(float(qty_closing), 2),
            'val_opening':      round(float(val_opening), 2),
            'val_in':           round(float(val_in), 2),
            'val_out':          round(float(val_out), 2),
            'val_closing':      round(float(val_closing), 2),
            'price_opening':    round(float(price_opening), 2),
            'price_in':         round(float(price_in), 2),
            'price_out':        round(float(price_out), 2),
            'price_closing':    round(float(price_closing), 2),
        }
        report.append(data)

    return report


def stock_level_report(date_from, date_to, by_material_group=False):
    """
    Returns : {
        'dates': [list_of_datetime_objects],
        'material_or_materialgroup_name_1': [list_of_daily_balances],
        'material_or_materialgroup_name_2': [list_of_daily_balances],
        ...
        'material_or_materialgroup_name_n': [list_of_daily_balances],
    }
    """
    result = {}
    # get dates
    dt_range = list(datetime_range(date_from, date_to))
    dates = [d for _, d in dt_range]
    result['dates'] = dates
    # get balances
    filters = MaterialGroup.objects.order_by('name').all() if by_material_group else Material.objects.order_by('name').all()
    for filter_by in filters:
        name = filter_by.name
        balances = [float(balance(d, filter_by=filter_by)) for _, d in dt_range]
        result[name] = balances

    return result

def weekly_sales_and_purchases_report(date_from, date_to):
    """
    Returns : {
        'week': [list_of_week_strings],
        'sales': [list_of_daily_revenues],
        'purchases': [list_of_daily_costs],
    }
    """
    result = {}
    # get dates
    dt_range = list(datetime_range(date_from, date_to, resolution=Resolution.WEEK))
    weeks = [f'W{d.date().isocalendar()[1]}' for d, _ in dt_range]
    result['week'] = weeks
    # get financials
    sales, purchases = [], []
    for df, dt in dt_range:
        temp = sales_and_purchases(df, dt)
        sales.append(float(temp[0]))
        purchases.append(float(temp[1]))
    result['sales'] = sales
    result['purchases'] = purchases

    return result


def sales_and_purchases_report(date_from, date_to, by_material_group=False, normalize=False):
    """
    Returns : {
        'item': [list_of_material_or_material_groups],
        'sales': [list_of_period_sales_per_item],
        'purchases': [list_of_period_purchaases_per_item],
    }
    """
    result = {}
    result['item'] = []
    result['sales'] = []
    result['purchases'] = []
    
    material_groups = MaterialGroup.objects.order_by('name').all()
    materials = Material.objects.order_by('material_group__name','name').filter(material_group__in=material_groups)
    filters = material_groups if by_material_group else materials
    # filters = MaterialGroup.objects.order_by('name').all() if by_material_group else Material.objects.order_by('material_group__name','name').all()
    for filter in filters:
        sales, purchases = sales_and_purchases(date_from, date_to, filter_by=filter)
        result['item'].append(filter.name)
        result['sales'].append(float(sales))
        result['purchases'].append(float(-purchases)) 
    
    if normalize: 
        result['sales'] = normalized(result['sales'])
        result['purchases'] = normalized(result['purchases'])

    return result
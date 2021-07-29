import datetime
import pytz
from math import pi

from django.http import JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import get_user_model

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool
from bokeh.models.widgets import Panel, Tabs
from bokeh.models.ranges import Range1d
from bokeh.embed import components
from bokeh.palettes import Category20c
from bokeh.transform import cumsum

from inventories.models import Transaction, MaterialGroup, Material
from reports.models import (
    Resolution, 
    summary_report, 
    stock_level_report, weekly_sales_and_purchases_report, sales_and_purchases_report
)

tz = pytz.timezone(settings.TIME_ZONE)

class DashboardView(TemplateView):
    template_name='reports/dashboard.html'

class TransactionsView(TemplateView):
    template_name='reports/transactions.html'

class SummaryView(TemplateView):
    template_name='reports/summary.html'


def get_material_groups(request):
    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 
    material_groups = MaterialGroup.serialize_all()
    return JsonResponse(material_groups, safe=False) 
    

def get_materials(request, material_group_id):
    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 
    # load material group filter
    if material_group_id == 'all':
        material_group = None
    else:
        try:
            material_group = MaterialGroup.objects.get(pk=material_group_id)
        except MaterialGroup.DoesNotExist:
            return JsonResponse({"error": "Material Group not found."}, status=404)
    
    materials = Material.serialize_all(material_group)
    return JsonResponse(materials, safe=False) 


def get_transactions(request):

    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 

    # check inputs
    data = request.GET
    # transaction type
    transaction_types = data.getlist('transaction_types')

    if transaction_types:
        if isinstance(transaction_types, list):
            if not set(transaction_types).issubset(set([Transaction.TYPE_IN, Transaction.TYPE_OUT, ''])):
                return JsonResponse({"error": "Transaction Type not found."}, status=404)
        elif transaction_types not in (Transaction.TYPE_IN, Transaction.TYPE_OUT):
            return JsonResponse({"error": "Transaction Type not found."}, status=404)
    # material group
    if data.get('material_group') is not None:
        try:
            material_group = MaterialGroup.objects.get(pk=data['material_group']) 
        except MaterialGroup.DoesNotExist:
            return JsonResponse({"error": "Material Group not found."}, status=404)
    else:
        material_group = None
    # material
    if data.get('material') is not None:
        try:
            material = Material.objects.get(pk=data['material']) 
        except Material.DoesNotExist:
            return JsonResponse({"error": "Material not found."}, status=404)
    else:
        material = None
    # start date
    if data.get('date_from') is not None:
        try:
            date_from = datetime.datetime.fromisoformat(data['date_from'])
            if date_from.tzinfo is None:
                date_from = tz.localize(date_from)
        except ValueError:
            return JsonResponse({"error": "Invalid date"}, status=400)
    else:
        date_from = None
    # end date
    if data.get('date_to') is not None:
        try:
            date_to = datetime.datetime.fromisoformat(data['date_to'])
            if date_to.tzinfo is None:
                date_to = tz.localize(date_to)
        except ValueError:
            return JsonResponse({"error": "Invalid date"}, status=400)
    else:
        date_to = None
    
    result = Transaction.serialized_filtered_transactions(
        transaction_types=transaction_types,
        material_group=material_group,
        material=material,
        date_from=date_from,
        date_to=date_to
    )

    return JsonResponse(result, safe=False) 

def get_summary(request):
    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 

    # check inputs
    data = request.GET

    # resolution
    if data.get('resolution') is not None:
        try:
            resolution = Resolution(data['resolution'])
        except ValueError:
            return JsonResponse({"error": "Resolution not found."}, status=404)
    else:
        return JsonResponse({"error": "Resolution missing."}, status=400)
    # material group / material
    if data.get('material') is not None:
        try:
            filter_by = Material.objects.get(pk=data['material']) 
        except Material.DoesNotExist:
            return JsonResponse({"error": "Material not found."}, status=404)
    elif data.get('material_group') is not None:
        try:
            filter_by = MaterialGroup.objects.get(pk=data['material_group']) 
        except MaterialGroup.DoesNotExist:
            return JsonResponse({"error": "Material Group not found."}, status=404)
    else:
        filter_by = None

    # start date
    if data.get('date_from') is not None:
        try:
            date_from = datetime.datetime.fromisoformat(data['date_from'])
            if date_from.tzinfo is None:
                date_from = tz.localize(date_from)
        except ValueError:
            return JsonResponse({"error": "Invalid date"}, status=400)
    else:
        return JsonResponse({"error": "Invalid date"}, status=400)
    # end date
    if data.get('date_to') is not None:
        try:
            date_to = datetime.datetime.fromisoformat(data['date_to'])
            if date_to.tzinfo is None:
                date_to = tz.localize(date_to)
        except ValueError:
            return JsonResponse({"error": "Invalid date"}, status=400)
    else:
        return JsonResponse({"error": "Invalid date"}, status=400)

    result = summary_report(date_from, date_to, resolution, filter_by)

    return JsonResponse(result, safe=False)


def get_stock_levels(request):
    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 

    date_from = tz.localize(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=30))
    date_to = tz.localize(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1, microseconds=-1))
    report = stock_level_report(date_from, date_to, by_material_group=True)
    
    chart_tabs = Tabs()
    dates = report['dates']
    for key, values in report.items():
        if key == 'dates':
            continue
        assert len(values) == len(dates)

        source = ColumnDataSource(
            data=dict(
                dates=dates,
                values=values,
            )
        )

        hover = HoverTool(
            tooltips=[
                ("Date",    "@dates{%F}"),
                ("Balance", "@values{0,0}"),
            ],
            formatters={
                "@dates":   "datetime",
                "@values":  "numeral",
            },
            mode='vline'
        )

        plot = figure(
            x_axis_type="datetime",
            y_axis_label='kg',
            y_range=Range1d(
                min(values) * 1.1 if min(values) < 0 else 0, 
                max(values) * 1.1 if max(values) > 0 else 10
            ),
            width_policy='max',
            height_policy='max',
            max_height=200,
            toolbar_location="below",
            tools=[hover],
        )
        # plot.line('dates', 'values', source=source, line_width=2)
        plot.vbar(x='dates', top='values', source=source, width=24*60*60*1000*0.7, fill_alpha=0.7)
        plot.xaxis.formatter.days = '%b %d'
        plot.xaxis.major_label_orientation = pi/2
        plot.yaxis.formatter = NumeralTickFormatter(format="0,0")
        tab = Panel(child=plot, title=key)   
        chart_tabs.tabs.append(tab)

    script, div = components(chart_tabs)

    return render(request, 'reports/dashboard_content.html', 
        {'div': div, 'script':script}
    )


def get_weekly_sales_and_purchases(request):
    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 

    date_from = tz.localize(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=30))
    # min_timestamp = date_from.timestamp() * 1000
    date_to = tz.localize(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1, microseconds=-1))
    # max_timestamp = date_to.timestamp() * 1000
    report = weekly_sales_and_purchases_report(date_from, date_to)

    source = ColumnDataSource(
        data=report
    )
    source.data['profit'] = [s + p for s, p in zip(report['sales'], report['purchases'])]

    hover = HoverTool(
        tooltips=[
            ("Week",        "@week"),
            ("Sales",       "@sales{0,0}"),
            ("Purchases",   "@purchases{0,0}"),
            ("Profit",      "@profit{0,0}")
        ],
        formatters={
            "@sales":       "numeral",
            "@purchases":   "numeral",
            "@profit":      "numeral",
        },
        mode='vline',
        names=['profit']
    )

    plot = figure(
        y_axis_label='$',
        x_range=report['week'],
        y_range=Range1d(
            min(report['purchases']) * 1.1 if min(report['purchases']) < 0 else 0, 
            max(report['sales']) * 1.1 if max(report['sales']) > 0 else 10
        ),
        width_policy='max',
        height_policy='max',
        max_height=200,
        toolbar_location="below",
        tools=[hover],
    )
    
    plot.vbar(        
        x='week', top='sales', source=source, 
        width=0.7, 
        fill_color='green', 
        fill_alpha=0.6,
        line_color='green',
        name='sales'
    )
    plot.vbar(
        x='week', top='purchases', source=source, 
        width=0.7, 
        fill_color='purple', 
        fill_alpha=0.6,
        line_color='purple',
        name='purchases'
    )
    plot.line(
        x='week', y='profit', source=source,
        line_width=3,
        color="blue",
        name='profit_line'
    )
    plot.circle(
        x='week', y='profit', source=source,
        line_color="blue", 
        fill_color="white", 
        size=5,
        name='profit'
    )
    plot.yaxis.formatter = NumeralTickFormatter(format="0,0")

    script, div = components(plot)

    return render(request, 'reports/dashboard_content.html', 
        {'div': div, 'script':script}
    )


def get_summary_sales_and_purchases(request):

    def get_plot(report_material_group, report_material, field):
        hover = HoverTool(
            # tooltips=f"@item: @{field}",
            tooltips=[
                ("Item",    "@item $swatch:color"),
                ("Pct",     f"@{field}"),
                ("fill color", "$swatch:color"),
            ],
            formatters={
                f"@{field}":  "numeral",
            },
            names=['material_group', 'material'],
            point_policy="follow_mouse"
        )

        plot = figure(
            width_policy='max',
            height_policy='max',
            max_height=200,
            toolbar_location="below",
            tools=[hover],
        )

        # outer donut: by material group
        source_material_group = ColumnDataSource(data=report_material_group)
        source_material_group.data['angle'] = [x * 2 * pi for x in source_material_group.data[f'{field}']]
        source_material_group.data['color'] = Category20c[len(source_material_group.data[f'{field}'])]
        plot.annular_wedge(
            x=0, y=0, source=source_material_group, 
            inner_radius=0.15, 
            outer_radius=0.25, 
            direction="anticlock",
            start_angle=cumsum('angle', include_zero=True), 
            end_angle=cumsum('angle'),
            line_color="white", 
            fill_color='color', 
            name='material_group'
        )

        # inner donut: by material
        source_material = ColumnDataSource(data=report_material)
        source_material.data['angle'] = [x * 2 * pi for x in source_material.data[f'{field}']]
        source_material.data['color'] = Category20c[len(source_material.data[f'{field}'])]
        plot.annular_wedge(
            x=0, y=0, source=source_material, 
            inner_radius=0.05, 
            outer_radius=0.14, 
            direction="anticlock",
            start_angle=cumsum('angle', include_zero=True), 
            end_angle=cumsum('angle'),
            line_color="white", 
            fill_color='color', 
            name='material'
        )

        plot.axis.axis_label=None
        plot.axis.visible=False
        plot.grid.grid_line_color = None

        return plot


    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 

    date_from = tz.localize(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=30))
    # min_timestamp = date_from.timestamp() * 1000
    date_to = tz.localize(datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1, microseconds=-1))
    # max_timestamp = date_to.timestamp() * 1000

    chart_tabs = Tabs()

    # get report data
    report_material_group = sales_and_purchases_report(date_from, date_to, by_material_group=True, normalize=True)
    report_material = sales_and_purchases_report(date_from, date_to, by_material_group=False, normalize=True)
    # get plots
    plot_sales = get_plot(report_material_group, report_material, 'sales')
    plot_purchases = get_plot(report_material_group, report_material, 'purchases')
    # get tabs
    tab_sales = Panel(child=plot_sales, title='Sales')   
    tab_purchases = Panel(child=plot_purchases, title='Purchases')   
    chart_tabs.tabs = [tab_sales, tab_purchases]

    script, div = components(chart_tabs)

    return render(request, 'reports/dashboard_content.html', 
        {'div': div, 'script':script}
    )

def get_user_statuses(request):
    # only GET method is accepted
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) 

    User = get_user_model()
    report = User.statuses()
    print(report)
    return render(request, 'reports/dashboard_table.html', 
        {'report': report}
    )
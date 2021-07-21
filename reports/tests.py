import datetime
import json
import uuid
import pytz

from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from inventories.models import MaterialGroup, Material, Transaction

from .models import (
    Resolution,
    datetime_range, generate_report
)

client = Client()
tz = pytz.timezone(settings.TIME_ZONE)

class ReportSupportFunctionsTests(TestCase):

    def test_datetime_range_daily(self):
        rng = datetime_range(
            start=datetime.datetime(2021, 7, 1),
            end=datetime.datetime(2021, 7, 3),
            resolution=Resolution.DAY
        )
        self.assertEqual(next(rng), (datetime.datetime(2021, 7, 1), datetime.datetime(2021, 7, 1)))
        self.assertEqual(next(rng), (datetime.datetime(2021, 7, 2), datetime.datetime(2021, 7, 2)))
        self.assertEqual(next(rng), (datetime.datetime(2021, 7, 3), datetime.datetime(2021, 7, 3)))
        self.assertRaises(StopIteration)

    def test_datetime_range_weekly(self):
        rng = datetime_range(
            start=datetime.datetime(2021, 7, 8),
            end=datetime.datetime(2021, 7, 20),
            resolution=Resolution.WEEK
        )
        self.assertEqual(next(rng), (datetime.datetime(2021, 7, 5), datetime.datetime(2021, 7, 11)))
        self.assertEqual(next(rng), (datetime.datetime(2021, 7, 12), datetime.datetime(2021, 7, 18)))
        self.assertEqual(next(rng), (datetime.datetime(2021, 7, 19), datetime.datetime(2021, 7, 25)))
        self.assertRaises(StopIteration)

    def test_datetime_range_monthly(self):
        rng = datetime_range(
            start=datetime.datetime(2021, 3, 20),
            end=datetime.datetime(2021, 5, 15),
            resolution=Resolution.MONTH
        )
        self.assertEqual(next(rng), (datetime.datetime(2021, 3, 1), datetime.datetime(2021, 3, 31)))
        self.assertEqual(next(rng), (datetime.datetime(2021, 4, 1), datetime.datetime(2021, 4, 30)))
        self.assertEqual(next(rng), (datetime.datetime(2021, 5, 1), datetime.datetime(2021, 5, 31)))
        self.assertRaises(StopIteration)


class GetTransactionsTests(TestCase):
    
    @classmethod
    def setUp(self):

        self.mat_group_1 = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        self.mat_group_2 = MaterialGroup.objects.get_or_create(name = 'steel')[0]
        self.mat_11 = Material.objects.get_or_create(name='alu cooler', material_group=self.mat_group_1)[0]
        self.mat_12 = Material.objects.get_or_create(name='alu can', material_group=self.mat_group_1)[0]
        self.mat_21 = Material.objects.get_or_create(name='steel can', material_group=self.mat_group_2)[0]
        
        self.t1 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=self.mat_11,
            transaction_time=tz.localize(datetime.datetime(2021,2,3)),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='some notes'
        )

        self.t2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=self.mat_12,
            transaction_time=tz.localize(datetime.datetime(2021,3,4)),
            gross_weight=20.0,
            tare_weight=4.0,
            unit_price=10.0,
            notes='some notes'
        )

        self.t2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_OUT,
            material=self.mat_21,
            transaction_time=tz.localize(datetime.datetime(2021,4,5)),
            gross_weight=30.0,
            tare_weight=5.0,
            unit_price=15.0,
            notes='some notes'
        )


    def test_get_all_transactions(self): 
        payload = {}
        response = client.get(
            reverse('get_transactions'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 3)        
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_transactions_no_type_provided(self):
        payload = {
            'transaction_types': ['']
        }
        response = client.get(
            reverse('get_transactions'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 0)


    def test_get_transactions_filtered_by_single_type(self):
        payload = {
            'transaction_types': ['IN']
        }
        response = client.get(
            reverse('get_transactions'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 2)
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_transactions_filtered_by_multiple_types(self):
        payload = {
            'transaction_types': ['IN', 'OUT']
        }
        response = client.get(
            reverse('get_transactions'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 3)
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_transactions_filtered_by_material_group(self): 
        payload = {
            'material_group': self.mat_group_1.pk
        }
        response = client.get(
            reverse('get_transactions'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 2)
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_transactions_filtered_by_material(self): 
        payload = {
            'material': self.mat_11.pk
        }
        response = client.get(
            reverse('get_transactions'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 1)
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_transactions_filtered_by_date_from(self): 
        payload = {
            'date_from': '2021-03-01'
        }
        response = client.get(
            reverse('get_transactions'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 2)
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_transactions_filtered_by_material_group_and_date_from(self):
        payload = {
            'material_group': self.mat_group_1.pk,
            'date_from': '2021-03-01'
        }
        response = client.get(
            reverse('get_transactions'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 1)
        for d in data:
            self.assertTrue(isinstance(d, dict))        


class GetMaterialGroupsTests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.mat_group_0 = MaterialGroup.objects.get_or_create(name = 'undefined')[0]
        cls.mat_group_1 = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        cls.mat_group_2 = MaterialGroup.objects.get_or_create(name = 'steel')[0]


    def test_get_material_groups_returns_all_instances(self):
        response = client.get(
            reverse('get_material_groups')
        )
        json_data = response.json()
        self.assertEqual(len(json_data), 3)
        # check content and sorting
        self.assertEqual(uuid.UUID(json_data[0]['id']), self.mat_group_1.id) # aluminium
        self.assertEqual(json_data[0]['name'], self.mat_group_1.name) # aluminium
        self.assertEqual(uuid.UUID(json_data[1]['id']), self.mat_group_2.id) # steel
        self.assertEqual(json_data[1]['name'], self.mat_group_2.name) # steel
        self.assertEqual(uuid.UUID(json_data[2]['id']), self.mat_group_0.id) # undefined
        self.assertEqual(json_data[2]['name'], self.mat_group_0.name) # undefined


class GetMaterialsTests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.mat_group_0 = MaterialGroup.objects.get_or_create(name = 'undefined')[0]
        cls.mat_group_1 = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        cls.mat_group_2 = MaterialGroup.objects.get_or_create(name = 'steel')[0]

        cls.mat_11 = Material.objects.get_or_create(name='alu cooler', material_group=cls.mat_group_1)[0]
        cls.mat_12 = Material.objects.get_or_create(name='alu can', material_group=cls.mat_group_1)[0]
        cls.mat_21 = Material.objects.get_or_create(name='steel can', material_group=cls.mat_group_2)[0]

    def test_get_materials_unfiltered(self):
        response = client.get(
            reverse('get_materials', kwargs={'material_group_id': 'all'})
        )
        json_data = response.json()
        self.assertEqual(len(json_data), 3)
        # check content and sorting
        self.assertEqual(uuid.UUID(json_data[0]['id']), self.mat_12.id) # alu can
        self.assertEqual(json_data[0]['name'], self.mat_12.name) # alu can
        self.assertEqual(uuid.UUID(json_data[0]['material_group_id']), self.mat_12.material_group.id) # alu can
        self.assertEqual(uuid.UUID(json_data[1]['id']), self.mat_11.id) # alu cooler
        self.assertEqual(json_data[1]['name'], self.mat_11.name) # alu cooler
        self.assertEqual(uuid.UUID(json_data[1]['material_group_id']), self.mat_11.material_group.id) # alu cooler
        self.assertEqual(uuid.UUID(json_data[2]['id']), self.mat_21.id) # steel can
        self.assertEqual(json_data[2]['name'], self.mat_21.name) # steel can
        self.assertEqual(uuid.UUID(json_data[2]['material_group_id']), self.mat_21.material_group.id) # steel can


    def test_get_materials_filtered(self):
        # filter by aluminium group
        material_group_id = str(self.mat_group_1.id)
        response = client.get(
            reverse('get_materials', kwargs={'material_group_id': material_group_id})
        )
        json_data = response.json()
        self.assertEqual(len(json_data), 2)
        # check content and sorting
        self.assertEqual(uuid.UUID(json_data[0]['id']), self.mat_12.id) # alu can
        self.assertEqual(json_data[0]['name'], self.mat_12.name) # alu can
        self.assertEqual(uuid.UUID(json_data[0]['material_group_id']), self.mat_12.material_group.id) # alu can
        self.assertEqual(uuid.UUID(json_data[1]['id']), self.mat_11.id) # alu cooler
        self.assertEqual(json_data[1]['name'], self.mat_11.name) # alu cooler
        self.assertEqual(uuid.UUID(json_data[1]['material_group_id']), self.mat_11.material_group.id) # alu cooler


class GenerateReportTests(TestCase):
    maxDiff = None

    @classmethod
    def setUp(self):

        mat_group_1 = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        mat_group_2 = MaterialGroup.objects.get_or_create(name = 'steel')[0]
        mat_11 = Material.objects.get_or_create(name='alu cooler', material_group=mat_group_1)[0]
        mat_12 = Material.objects.get_or_create(name='alu can', material_group=mat_group_1)[0]
        mat_21 = Material.objects.get_or_create(name='steel can', material_group=mat_group_2)[0]
        
        Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat_11,
            transaction_time=tz.localize(datetime.datetime(2021,2,3)),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='some notes'
        )

        Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat_12,
            transaction_time=tz.localize(datetime.datetime(2021,3,4)),
            gross_weight=20.0,
            tare_weight=4.0,
            unit_price=10.0,
            notes='some notes'
        )

        Transaction.objects.create(
            transaction_type=Transaction.TYPE_OUT,
            material=mat_21,
            transaction_time=tz.localize(datetime.datetime(2021,4,5)),
            gross_weight=30.0,
            tare_weight=5.0,
            unit_price=15.0,
            notes='some notes'
        )

    def test_daily_material_report_1(self):
        date_from = tz.localize(datetime.datetime(2021,2,1))
        date_to = tz.localize(datetime.datetime(2021,2,2))
        resolution = Resolution.DAY
        filter_by = Material.objects.get(name = 'alu cooler')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,2,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,1).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,2,2).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,2).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            }            
        ]
        self.assertListEqual(report, expected)

    def test_daily_material_report_2(self):
        date_from = tz.localize(datetime.datetime(2021,2,2))
        date_to = tz.localize(datetime.datetime(2021,2,4))
        resolution = Resolution.DAY
        filter_by = Material.objects.get(name = 'alu cooler')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,2,2).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,2).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,2,3).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,3).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 8,
                'qty_out': 0,
                'qty_closing': 8,
            },           
            {
                'start_of_period': datetime.date(2021,2,4).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,4).strftime('%Y-%m-%d'),
                'qty_opening': 8,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 8,
            },   
        ]
        self.assertListEqual(report, expected)

    def test_daily_material_report_3(self):
        date_from = tz.localize(datetime.datetime(2021,4,4))
        date_to = tz.localize(datetime.datetime(2021,4,6))
        resolution = Resolution.DAY
        filter_by = Material.objects.get(name = 'steel can')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,4,4).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,4).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,4,5).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,5).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 25,
                'qty_closing': -25,
            },           
            {
                'start_of_period': datetime.date(2021,4,6).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,6).strftime('%Y-%m-%d'),
                'qty_opening': -25,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': -25,
            },   
        ]
        self.assertListEqual(report, expected)


    def test_weekly_material_report_1(self):
        date_from = tz.localize(datetime.datetime(2021,1,7))
        date_to = tz.localize(datetime.datetime(2021,1,14))
        resolution = Resolution.WEEK
        filter_by = Material.objects.get(name = 'alu cooler')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,1,4).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,1,10).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,1,11).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,1,17).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            }            
        ]
        self.assertListEqual(report, expected)

    def test_weekly_material_report_2(self):
        date_from = tz.localize(datetime.datetime(2021,1,29))
        date_to = tz.localize(datetime.datetime(2021,2,10))
        resolution = Resolution.WEEK
        filter_by = Material.objects.get(name = 'alu cooler')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,1,25).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,1,31).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,2,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,7).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 8,
                'qty_out': 0,
                'qty_closing': 8,
            },           
            {
                'start_of_period': datetime.date(2021,2,8).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,14).strftime('%Y-%m-%d'),
                'qty_opening': 8,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 8,
            },   
        ]
        self.assertListEqual(report, expected)

    def test_weekly_material_report_3(self):
        date_from = tz.localize(datetime.datetime(2021,4,1))
        date_to = tz.localize(datetime.datetime(2021,4,15))
        resolution = Resolution.WEEK
        filter_by = Material.objects.get(name = 'steel can')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,3,29).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,4).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,4,5).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,11).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 25,
                'qty_closing': -25,
            },           
            {
                'start_of_period': datetime.date(2021,4,12).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,18).strftime('%Y-%m-%d'),
                'qty_opening': -25,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': -25,
            },   
        ]
        self.assertListEqual(report, expected)


    def test_monthly_material_report_1(self):
        date_from = tz.localize(datetime.datetime(2021,1,7))
        date_to = tz.localize(datetime.datetime(2021,1,14))
        resolution = Resolution.MONTH
        filter_by = Material.objects.get(name = 'alu cooler')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,1,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,1,31).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },         
        ]
        self.assertListEqual(report, expected)

    def test_monthly_material_report_2(self):
        date_from = tz.localize(datetime.datetime(2021,1,29))
        date_to = tz.localize(datetime.datetime(2021,3,10))
        resolution = Resolution.MONTH
        filter_by = Material.objects.get(name = 'alu cooler')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,1,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,1,31).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,2,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,28).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 8,
                'qty_out': 0,
                'qty_closing': 8,
            },           
            {
                'start_of_period': datetime.date(2021,3,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,3,31).strftime('%Y-%m-%d'),
                'qty_opening': 8,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 8,
            },   
        ]
        self.assertListEqual(report, expected)

    def test_monthly_material_report_3(self):
        date_from = tz.localize(datetime.datetime(2021,3,20))
        date_to = tz.localize(datetime.datetime(2021,5,15))
        resolution = Resolution.MONTH
        filter_by = Material.objects.get(name = 'steel can')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,3,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,3,31).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,4,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,30).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 25,
                'qty_closing': -25,
            },           
            {
                'start_of_period': datetime.date(2021,5,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,5,31).strftime('%Y-%m-%d'),
                'qty_opening': -25,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': -25,
            },   
        ]
        self.assertListEqual(report, expected)


    def test_daily_material_group_report_1(self):
        date_from = tz.localize(datetime.datetime(2021,2,1))
        date_to = tz.localize(datetime.datetime(2021,2,2))
        resolution = Resolution.DAY
        filter_by = MaterialGroup.objects.get(name = 'aluminium')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,2,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,1).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,2,2).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,2).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            }            
        ]
        self.assertListEqual(report, expected)

    def test_daily_material_group_report_2(self):
        date_from = tz.localize(datetime.datetime(2021,3,3))
        date_to = tz.localize(datetime.datetime(2021,3,5))
        resolution = Resolution.DAY
        filter_by = MaterialGroup.objects.get(name = 'aluminium')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,3,3).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,3,3).strftime('%Y-%m-%d'),
                'qty_opening': 8,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 8,
            },
            {
                'start_of_period': datetime.date(2021,3,4).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,3,4).strftime('%Y-%m-%d'),
                'qty_opening': 8,
                'qty_in': 16,
                'qty_out': 0,
                'qty_closing': 24,
            },           
            {
                'start_of_period': datetime.date(2021,3,5).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,3,5).strftime('%Y-%m-%d'),
                'qty_opening': 24,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 24,
            },   
        ]
        self.assertListEqual(report, expected)

    def test_daily_material_group_report_3(self):
        date_from = tz.localize(datetime.datetime(2021,4,4))
        date_to = tz.localize(datetime.datetime(2021,4,6))
        resolution = Resolution.DAY
        filter_by = MaterialGroup.objects.get(name = 'steel')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,4,4).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,4).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,4,5).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,5).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 25,
                'qty_closing': -25,
            },           
            {
                'start_of_period': datetime.date(2021,4,6).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,6).strftime('%Y-%m-%d'),
                'qty_opening': -25,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': -25,
            },   
        ]
        self.assertListEqual(report, expected)


    def test_weekly_material_group_report_1(self):
        date_from = tz.localize(datetime.datetime(2021,1,7))
        date_to = tz.localize(datetime.datetime(2021,1,14))
        resolution = Resolution.WEEK
        filter_by = MaterialGroup.objects.get(name = 'aluminium')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,1,4).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,1,10).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,1,11).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,1,17).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            }            
        ]
        self.assertListEqual(report, expected)

    def test_weekly_material_group_report_2(self):
        date_from = tz.localize(datetime.datetime(2021,2,25))
        date_to = tz.localize(datetime.datetime(2021,3,10))
        resolution = Resolution.WEEK
        filter_by = MaterialGroup.objects.get(name = 'aluminium')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,2,22).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,28).strftime('%Y-%m-%d'),
                'qty_opening': 8,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 8,
            },
            {
                'start_of_period': datetime.date(2021,3,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,3,7).strftime('%Y-%m-%d'),
                'qty_opening': 8,
                'qty_in': 16,
                'qty_out': 0,
                'qty_closing': 24,
            },           
            {
                'start_of_period': datetime.date(2021,3,8).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,3,14).strftime('%Y-%m-%d'),
                'qty_opening': 24,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 24,
            },   
        ]
        self.assertListEqual(report, expected)

    def test_weekly_material_group_report_3(self):
        date_from = tz.localize(datetime.datetime(2021,4,1),)
        date_to = tz.localize(datetime.datetime(2021,4,15))
        resolution = Resolution.WEEK
        filter_by = MaterialGroup.objects.get(name = 'steel')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,3,29).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,4).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,4,5).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,11).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 25,
                'qty_closing': -25,
            },           
            {
                'start_of_period': datetime.date(2021,4,12).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,18).strftime('%Y-%m-%d'),
                'qty_opening': -25,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': -25,
            },   
        ]
        self.assertListEqual(report, expected)


    def test_monthly_material_group_report_1(self):
        date_from = tz.localize(datetime.datetime(2021,1,7))
        date_to = tz.localize(datetime.datetime(2021,1,14))
        resolution = Resolution.MONTH
        filter_by = MaterialGroup.objects.get(name = 'aluminium')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,1,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,1,31).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },         
        ]
        self.assertListEqual(report, expected)

    def test_monthly_material_group_report_2(self):
        date_from = tz.localize(datetime.datetime(2021,1,29))
        date_to = tz.localize(datetime.datetime(2021,3,10))
        resolution = Resolution.MONTH
        filter_by = MaterialGroup.objects.get(name = 'aluminium')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,1,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,1,31).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,2,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,2,28).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 8,
                'qty_out': 0,
                'qty_closing': 8,
            },           
            {
                'start_of_period': datetime.date(2021,3,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,3,31).strftime('%Y-%m-%d'),
                'qty_opening': 8,
                'qty_in': 16,
                'qty_out': 0,
                'qty_closing': 24,
            },   
        ]
        self.assertListEqual(report, expected)

    def test_monthly_material_group_report_3(self):
        date_from = tz.localize(datetime.datetime(2021,3,20))
        date_to = tz.localize(datetime.datetime(2021,5,15))
        resolution = Resolution.MONTH
        filter_by = MaterialGroup.objects.get(name = 'steel')
        report = generate_report(date_from, date_to, resolution, filter_by)
        expected = [
            {
                'start_of_period': datetime.date(2021,3,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,3,31).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,4,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,4,30).strftime('%Y-%m-%d'),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 25,
                'qty_closing': -25,
            },           
            {
                'start_of_period': datetime.date(2021,5,1).strftime('%Y-%m-%d'),
                'end_of_period': datetime.date(2021,5,31).strftime('%Y-%m-%d'),
                'qty_opening': -25,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': -25,
            },   
        ]
        self.assertListEqual(report, expected)


class GetSummaryTests(TestCase):
    
    @classmethod
    def setUp(self):

        self.mat_group_1 = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        self.mat_group_2 = MaterialGroup.objects.get_or_create(name = 'steel')[0]
        self.mat_11 = Material.objects.get_or_create(name='alu cooler', material_group=self.mat_group_1)[0]
        self.mat_12 = Material.objects.get_or_create(name='alu can', material_group=self.mat_group_1)[0]
        self.mat_21 = Material.objects.get_or_create(name='steel can', material_group=self.mat_group_2)[0]
        
        self.t1 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=self.mat_11,
            transaction_time=tz.localize(datetime.datetime(2021,2,3)),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='some notes'
        )

        self.t2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=self.mat_12,
            transaction_time=tz.localize(datetime.datetime(2021,3,4)),
            gross_weight=20.0,
            tare_weight=4.0,
            unit_price=10.0,
            notes='some notes'
        )

        self.t2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_OUT,
            material=self.mat_21,
            transaction_time=tz.localize(datetime.datetime(2021,4,5)),
            gross_weight=30.0,
            tare_weight=5.0,
            unit_price=15.0,
            notes='some notes'
        )


    def test_get_daily_report_all(self): 
        payload = {
            'resolution': 'day',
            'date_from': '2021-03-01',
            'date_to': '2021-03-31'
        }
        response = client.get(
            reverse('get_summary'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 31)        
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_weekly_report_all(self): 
        payload = {
            'resolution': 'week',
            'date_from': '2021-03-01',
            'date_to': '2021-03-31'
        }
        response = client.get(
            reverse('get_summary'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 5)        
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_monthly_report_all(self): 
        payload = {
            'resolution': 'month',
            'date_from': '2021-03-01',
            'date_to': '2021-04-15'
        }
        response = client.get(
            reverse('get_summary'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 2)        
        for d in data:
            self.assertTrue(isinstance(d, dict))

    def test_get_daily_material_report(self): 
        payload = {
            'resolution': 'day',
            'date_from': '2021-03-01',
            'date_to': '2021-03-31',
            'material': self.mat_11.pk
        }
        response = client.get(
            reverse('get_summary'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 31)        
        for d in data:
            self.assertTrue(isinstance(d, dict))

    def test_get_weekly_material_report(self): 
        payload = {
            'resolution': 'week',
            'date_from': '2021-03-01',
            'date_to': '2021-03-31',
            'material': self.mat_11.pk
        }
        response = client.get(
            reverse('get_summary'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 5)        
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_monthly_material_report(self): 
        payload = {
            'resolution': 'month',
            'date_from': '2021-03-01',
            'date_to': '2021-04-15',
            'material': self.mat_11.pk
        }
        response = client.get(
            reverse('get_summary'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 2)        
        for d in data:
            self.assertTrue(isinstance(d, dict))

    def test_get_daily_material_group_report(self): 
        payload = {
            'resolution': 'day',
            'date_from': '2021-03-01',
            'date_to': '2021-03-31',
            'material_group': self.mat_group_1.pk
        }
        response = client.get(
            reverse('get_summary'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 31)        
        for d in data:
            self.assertTrue(isinstance(d, dict))

    def test_get_weekly_material_group_report(self): 
        payload = {
            'resolution': 'week',
            'date_from': '2021-03-01',
            'date_to': '2021-03-31',
            'material_group': self.mat_group_1.pk
        }
        response = client.get(
            reverse('get_summary'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 5)        
        for d in data:
            self.assertTrue(isinstance(d, dict))


    def test_get_monthly_material_group_report(self): 
        payload = {
            'resolution': 'month',
            'date_from': '2021-03-01',
            'date_to': '2021-04-15',
            'material_group': self.mat_group_1.pk
        }
        response = client.get(
            reverse('get_summary'),
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(len(data), 2)        
        for d in data:
            self.assertTrue(isinstance(d, dict))




    # def test_get_nonexisting_post_raises_error(self):

    #     response = client.get(reverse('post', kwargs={'post_id': 99}))
    #     data = response.json()
    #     self.assertEqual(data['error'], "Post not found.")
    #     self.assertEqual(response.status_code, 404)


    # def test_change_post_content(self):

    #     p1 = Post.objects.get(pk=1)

    #     # test content before request
    #     self.assertEqual(p1.content, 'abc')

    #     # put request
    #     response = client.put(
    #         reverse('post', kwargs={'post_id': p1.id}),
    #         data=json.dumps(self.payload_change_content),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 204)
        
    #     # test content after request     
    #     p1 = Post.objects.get(pk=1)   
    #     self.assertEqual(p1.content, 'def')


    # def test_like_unlike(self):
    #     p2 = Post.objects.get(pk=2)
    #     u1 = User.objects.get(username='u1')

    #     # test initial status
    #     self.assertEqual(list(p2.liked_by.all()), [])

    #     # like
    #     response = client.put(
    #         reverse('post', kwargs={'post_id': p2.id}),
    #         data=json.dumps(self.payload_like),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 204)
    #     p2 = Post.objects.get(pk=2)
    #     self.assertEqual(list(p2.liked_by.all()), [u1])

    #     # like again
    #     response = client.put(
    #         reverse('post', kwargs={'post_id': p2.id}),
    #         data=json.dumps(self.payload_like),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 204)
    #     p2 = Post.objects.get(pk=2)
    #     self.assertEqual(list(p2.liked_by.all()), [u1])

    #     # unlike
    #     response = client.put(
    #         reverse('post', kwargs={'post_id': p2.id}),
    #         data=json.dumps(self.payload_unlike),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 204)
    #     p2 = Post.objects.get(pk=2)
    #     self.assertEqual(list(p2.liked_by.all()), [])

    #     # unlike again
    #     response = client.put(
    #         reverse('post', kwargs={'post_id': p2.id}),
    #         data=json.dumps(self.payload_unlike),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 204)
    #     p2 = Post.objects.get(pk=2)
    #     self.assertEqual(list(p2.liked_by.all()), [])


    # def test_post_method_raises_error(self):

    #     p1 = Post.objects.get(pk=1)

    #     # put request
    #     response = client.post(
    #         reverse('post', kwargs={'post_id': p1.id}),
    #         data=json.dumps(self.payload_change_content),
    #         content_type='application/json'
    #     )
    #     data = response.json()
    #     self.assertEqual(data['error'], "GET or PUT request required.")
    #     self.assertEqual(response.status_code, 400)


    # def test_request_denied_for_non_authenticated_user(self):
    #     client.logout()
        
    #     p1 = Post.objects.get(pk=1)

    #     # put request
    #     response = client.put(
    #         reverse('post', kwargs={'post_id': p1.id}),
    #         data=json.dumps(self.payload_change_content),
    #         content_type='application/json'
    #     )

    #     # Make sure status code is 302: redirect to /accounts/login/?next=/following
    #     self.assertEqual(response.status_code, 302)

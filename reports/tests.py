import datetime
import json
import uuid

from django.test import TestCase, Client
from django.urls import reverse

from inventories.models import MaterialGroup, Material, Transaction

from .models import datetime_range, daily_material_report

client = Client()


class ReportSupportFunctionsTest(TestCase):

    def test_datetime_range_daily(self):
        rng = datetime_range(
            start=datetime.date(2021, 7, 1),
            end=datetime.date(2021, 7, 3),
            resolution='days'
        )
        self.assertEqual(next(rng), (datetime.date(2021, 7, 1), datetime.date(2021, 7, 1)))
        self.assertEqual(next(rng), (datetime.date(2021, 7, 2), datetime.date(2021, 7, 2)))
        self.assertEqual(next(rng), (datetime.date(2021, 7, 3), datetime.date(2021, 7, 3)))
        self.assertRaises(StopIteration)

    def test_datetime_range_weekly(self):
        rng = datetime_range(
            start=datetime.date(2021, 7, 8),
            end=datetime.date(2021, 7, 20),
            resolution='weeks'
        )
        self.assertEqual(next(rng), (datetime.date(2021, 7, 5), datetime.date(2021, 7, 11)))
        self.assertEqual(next(rng), (datetime.date(2021, 7, 12), datetime.date(2021, 7, 18)))
        self.assertEqual(next(rng), (datetime.date(2021, 7, 19), datetime.date(2021, 7, 25)))
        self.assertRaises(StopIteration)

    def test_datetime_range_monthly(self):
        rng = datetime_range(
            start=datetime.date(2021, 7, 8),
            end=datetime.date(2021, 9, 20),
            resolution='months'
        )
        self.assertEqual(next(rng), (datetime.date(2021, 7, 1), datetime.date(2021, 7, 31)))
        self.assertEqual(next(rng), (datetime.date(2021, 8, 1), datetime.date(2021, 8, 31)))
        self.assertEqual(next(rng), (datetime.date(2021, 9, 1), datetime.date(2021, 9, 30)))
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
            transaction_time=datetime.date(2021,2,3),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='some notes'
        )

        self.t2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=self.mat_12,
            transaction_time=datetime.date(2021,3,4),
            gross_weight=20.0,
            tare_weight=4.0,
            unit_price=10.0,
            notes='some notes'
        )

        self.t2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_OUT,
            material=self.mat_21,
            transaction_time=datetime.date(2021,4,5),
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


class SummaryReportsTests(TestCase):

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
            transaction_time=datetime.date(2021,2,3),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='some notes'
        )

        Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat_12,
            transaction_time=datetime.date(2021,3,4),
            gross_weight=20.0,
            tare_weight=4.0,
            unit_price=10.0,
            notes='some notes'
        )

        Transaction.objects.create(
            transaction_type=Transaction.TYPE_OUT,
            material=mat_21,
            transaction_time=datetime.date(2021,4,5),
            gross_weight=30.0,
            tare_weight=5.0,
            unit_price=15.0,
            notes='some notes'
        )

    def test_daily_material_report_1(self):
        alu = Material.objects.get(name = 'alu cooler')
        report = daily_material_report(datetime.date(2021,2,1), datetime.date(2021,2,2), alu)
        expected = [
            {
                'start_of_period': datetime.date(2021,2,1),
                'end_of_period': datetime.date(2021,2,1),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,2,2),
                'end_of_period': datetime.date(2021,2,2),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            }            
        ]
        self.assertListEqual(report, expected)

    def test_daily_material_report_2(self):
        alu = Material.objects.get(name = 'alu cooler')
        report = daily_material_report(datetime.date(2021,2,2), datetime.date(2021,2,4), alu)
        expected = [
            {
                'start_of_period': datetime.date(2021,2,2),
                'end_of_period': datetime.date(2021,2,2),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,2,3),
                'end_of_period': datetime.date(2021,2,3),
                'qty_opening': 0,
                'qty_in': 8,
                'qty_out': 0,
                'qty_closing': 8,
            },           
            {
                'start_of_period': datetime.date(2021,2,4),
                'end_of_period': datetime.date(2021,2,4),
                'qty_opening': 8,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 8,
            },   
        ]
        self.assertListEqual(report, expected)

    def test_daily_material_report_3(self):
        steel = Material.objects.get(name = 'steel can')
        report = daily_material_report(datetime.date(2021,4,4), datetime.date(2021,4,6), steel)
        expected = [
            {
                'start_of_period': datetime.date(2021,4,4),
                'end_of_period': datetime.date(2021,4,4),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': 0,
            },
            {
                'start_of_period': datetime.date(2021,4,5),
                'end_of_period': datetime.date(2021,4,5),
                'qty_opening': 0,
                'qty_in': 0,
                'qty_out': 25,
                'qty_closing': -25,
            },           
            {
                'start_of_period': datetime.date(2021,4,6),
                'end_of_period': datetime.date(2021,4,6),
                'qty_opening': -25,
                'qty_in': 0,
                'qty_out': 0,
                'qty_closing': -25,
            },   
        ]
        self.assertListEqual(report, expected)



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

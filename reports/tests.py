import datetime
import json
import uuid

from django.test import TestCase, Client
from django.urls import reverse

from inventories.models import MaterialGroup, Material, Transaction, UUIDEncoder


client = Client()


class GetTransactionsTests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        mat_group_1 = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        mat_group_2 = MaterialGroup.objects.get_or_create(name = 'steel')[0]
        mat_11 = Material.objects.get_or_create(name='alu cooler', material_group=mat_group_1)[0]
        mat_12 = Material.objects.get_or_create(name='alu can', material_group=mat_group_1)[0]
        mat_21 = Material.objects.get_or_create(name='steel can', material_group=mat_group_2)[0]
        
        cls.t1 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat_11,
            transaction_time=datetime.date(2021,2,3),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='some notes'
        )

        cls.t2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat_12,
            transaction_time=datetime.date(2021,3,4),
            gross_weight=20.0,
            tare_weight=4.0,
            unit_price=10.0,
            notes='some notes'
        )

        cls.t2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_OUT,
            material=mat_21,
            transaction_time=datetime.date(2021,4,5),
            gross_weight=30.0,
            tare_weight=5.0,
            unit_price=15.0,
            notes='some notes'
        )

        cls.payload_all = {}
        cls.payload_type0 = {
            'transaction_types': ['']
        }
        cls.payload_type1 = {
            'transaction_types': ['IN']
        }
        cls.payload_type2 = {
            'transaction_types': ['IN', 'OUT']
        }
        cls.payload_mat_group = {
            'material_group': mat_group_1.pk
        }
        cls.payload_mat = {
            'material': mat_11.pk
        }
        cls.payload_datefrom = {
            'date_from': '2021-03-01'
        }
        cls.payload_mat_group_datefrom = {
            'material_group': mat_group_1.pk,
            'date_from': '2021-03-01'
        }

    # def setUp(self):
    #     # log in user 1
    #     u1 = User.objects.get(pk=1)
    #     client.force_login(u1)


    # def tearDown(self):
    #     client.logout()


    def test_get_all_transactions(self): 
        response = client.get(
            reverse('get_transactions'),
            data=self.payload_all,
            content_type='application/json'
        )
        json_data = response.json()
        data = json.loads(json_data['transactions'])

        self.assertEqual(len(data), 3)
        self.assertEqual(response.status_code, 200)


    def test_get_transactions_no_type_provided(self):
        response = client.get(
            reverse('get_transactions'),
            data=self.payload_type0,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        data = json.loads(json_data['transactions'])

        self.assertEqual(len(data), 0)


    def test_get_transactions_filtered_by_single_type(self):
        response = client.get(
            reverse('get_transactions'),
            data=self.payload_type1,
            content_type='application/json'
        )
        json_data = response.json()
        data = json.loads(json_data['transactions'])

        self.assertEqual(len(data), 2)
        self.assertEqual(response.status_code, 200)


    def test_get_transactions_filtered_by_multiple_types(self):
        response = client.get(
            reverse('get_transactions'),
            data=self.payload_type2,
            content_type='application/json'
        )
        json_data = response.json()
        data = json.loads(json_data['transactions'])

        self.assertEqual(len(data), 3)
        self.assertEqual(response.status_code, 200)


    def test_get_transactions_filtered_by_material_group(self): 
        response = client.get(
            reverse('get_transactions'),
            data=self.payload_mat_group,
            content_type='application/json'
        )
        json_data = response.json()
        data = json.loads(json_data['transactions'])

        self.assertEqual(len(data), 2)
        self.assertEqual(response.status_code, 200)


    def test_get_transactions_filtered_by_material(self): 
        response = client.get(
            reverse('get_transactions'),
            data=self.payload_mat,
            content_type='application/json'
        )
        json_data = response.json()
        data = json.loads(json_data['transactions'])

        self.assertEqual(len(data), 1)
        self.assertEqual(response.status_code, 200)


    def test_get_transactions_filtered_by_date_from(self): 
        response = client.get(
            reverse('get_transactions'),
            data=self.payload_datefrom,
            content_type='application/json'
        )
        json_data = response.json()
        data = json.loads(json_data['transactions'])

        self.assertEqual(len(data), 2)
        self.assertEqual(response.status_code, 200)


    def test_get_transactions_filtered_by_material_group_and_date_from(self):
        response = client.get(
            reverse('get_transactions'),
            data=self.payload_mat_group_datefrom,
            content_type='application/json'
        )
        json_data = response.json()
        data = json.loads(json_data['transactions'])

        self.assertEqual(len(data), 1)
        self.assertEqual(response.status_code, 200)


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
        print(json_data)
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
        material_group_id = UUIDEncoder().default(self.mat_group_1.id)
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

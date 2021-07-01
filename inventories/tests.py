import datetime
from datetime import timezone

from django.test import TestCase, Client
from django.urls import reverse

from .models import MaterialGroup, Material, Transaction


class MaterialGroupTests(TestCase):
    
    def setUp(self):
        self.material_group = MaterialGroup.objects.create(
            name = 'aluminium',
        )
 

    def test_material_group_listing(self):
        self.assertEqual(f'{self.material_group.name}', 'aluminium')

    def test_material_group_list_view(self):
        response = self.client.get(reverse('material_group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aluminium')
        self.assertTemplateUsed(response, 'inventories/material_group_list.html')
    
    def test_material_group_detail_view(self):
        response = self.client.get(self.material_group.get_absolute_url())
        no_response = self.client.get('/inventories/material_groups/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'aluminium')
        self.assertTemplateUsed(response, 'inventories/material_group_detail.html')


class MaterialTests(TestCase):
    
    def setUp(self):
        self.material = Material.objects.create(
            name = 'alu cooler',
            material_group = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        )
 

    def test_material_listing(self):
        self.assertEqual(f'{self.material.name}', 'alu cooler')
        self.assertEqual(f'{self.material.material_group.name}', 'aluminium')

    def test_material_list_view(self):
        response = self.client.get(reverse('material_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/material_list.html')
    
    def test_material_detail_view(self):
        response = self.client.get(self.material.get_absolute_url())
        no_response = self.client.get('/inventories/materials/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/material_detail.html')


class TransactionTests(TestCase):
    
    def setUp(self):
        mat_group = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        mat = Material.objects.get_or_create(name='alu cooler', material_group=mat_group)[0]
        
        self.transaction = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat,
            transaction_time=datetime.date(2021,2,3),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='some notes'
        )
 

    def test_transaction_listing(self):
        self.assertEqual(f'{self.transaction.transaction_type}', Transaction.TYPE_IN)
        self.assertEqual(f'{self.transaction.material.name}', 'alu cooler')
        self.assertEqual(f'{self.transaction.material.material_group.name}', 'aluminium')
        self.assertEqual(self.transaction.gross_weight, 10.0)
        self.assertEqual(self.transaction.tare_weight, 2.0)
        self.assertEqual(self.transaction.unit_price, 5.0)
        self.assertEqual(f'{self.transaction.notes}', 'some notes')
        self.assertEqual(self.transaction.net_weight, 8.0)
        self.assertEqual(self.transaction.net_value, 40.0)

    def test_transaction_list_view(self):
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/transaction_list.html')
    
    def test_transaction_detail_view(self):
        response = self.client.get(self.transaction.get_absolute_url())
        no_response = self.client.get('/inventories/transactions/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/transaction_detail.html')
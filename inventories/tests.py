import datetime
import pytz

from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

from .models import (
    MaterialGroup, Material, Transaction,
    balance, movement_between
)

tz = pytz.timezone(settings.TIME_ZONE)

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
        self.assertTemplateUsed(response, 'inventories/inventory_list.html')
    
    def test_material_group_detail_view(self):
        response = self.client.get(self.material_group.get_absolute_url())
        no_response = self.client.get('/inventories/inventory_groups/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'aluminium')
        self.assertTemplateUsed(response, 'inventories/inventory_detail.html')

    def test_material_group_create_view(self):
        response = self.client.get(reverse('material_group_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventories/inventory_new.html')

    def test_material_group_edit_view(self):
        response = self.client.get(reverse('material_group_edit', args=[f'{self.material_group.id}']))
        no_response = self.client.get('/inventories/inventory_edit/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'aluminium')
        self.assertTemplateUsed(response, 'inventories/inventory_edit.html')

    def test_material_group_delete_view(self):
        response = self.client.get(reverse('material_group_delete', args=[f'{self.material_group.id}']))
        no_response = self.client.get('/inventories/inventory_delete/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'aluminium')
        self.assertContains(response, 'delete')
        self.assertTemplateUsed(response, 'inventories/inventory_delete.html')        


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
        self.assertTemplateUsed(response, 'inventories/inventory_list.html')
    
    def test_material_detail_view(self):
        response = self.client.get(self.material.get_absolute_url())
        no_response = self.client.get('/inventories/materials/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/inventory_detail.html')

    def test_material_create_view(self):
        response = self.client.get(reverse('material_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventories/inventory_new.html')

    def test_material_edit_view(self):
        response = self.client.get(reverse('material_edit', args=[f'{self.material.id}']))
        no_response = self.client.get('/inventories/inventory_edit/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/inventory_edit.html')

    def test_material_delete_view(self):
        response = self.client.get(reverse('material_delete', args=[f'{self.material.id}']))
        no_response = self.client.get('/inventories/inventory_delete/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertContains(response, 'delete')
        self.assertTemplateUsed(response, 'inventories/inventory_delete.html')  


class TransactionTests(TestCase):
    
    def setUp(self):
        mat_group = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        mat = Material.objects.get_or_create(name='alu cooler', material_group=mat_group)[0]
        
        self.goods_receipt = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat,
            transaction_time=tz.localize(datetime.datetime(2021,2,3)),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='some notes'
        )

        self.goods_dispatch = Transaction.objects.create(
            transaction_type=Transaction.TYPE_OUT,
            material=mat,
            transaction_time=tz.localize(datetime.datetime(2021,3,4)),
            gross_weight=20.0,
            tare_weight=4.0,
            unit_price=10.0,
            notes='some notes'
        )


    def test_transaction_listing(self):
        self.assertEqual(f'{self.goods_receipt.transaction_type}', Transaction.TYPE_IN)
        self.assertEqual(f'{self.goods_receipt.material.name}', 'alu cooler')
        self.assertEqual(f'{self.goods_receipt.material.material_group.name}', 'aluminium')
        self.assertEqual(self.goods_receipt.gross_weight, 10.0)
        self.assertEqual(self.goods_receipt.tare_weight, 2.0)
        self.assertEqual(self.goods_receipt.unit_price, 5.0)
        self.assertEqual(f'{self.goods_receipt.notes}', 'some notes')
        self.assertEqual(self.goods_receipt.net_weight, 8.0)
        self.assertEqual(self.goods_receipt.net_value, 40.0)

        self.assertEqual(f'{self.goods_dispatch.transaction_type}', Transaction.TYPE_OUT)
        self.assertEqual(f'{self.goods_dispatch.material.name}', 'alu cooler')
        self.assertEqual(f'{self.goods_dispatch.material.material_group.name}', 'aluminium')
        self.assertEqual(self.goods_dispatch.gross_weight, 20.0)
        self.assertEqual(self.goods_dispatch.tare_weight, 4.0)
        self.assertEqual(self.goods_dispatch.unit_price, 10.0)
        self.assertEqual(f'{self.goods_dispatch.notes}', 'some notes')
        self.assertEqual(self.goods_dispatch.net_weight, 16.0)
        self.assertEqual(self.goods_dispatch.net_value, 160.0)

    # def test_transactions_with_annotations(self):
    #     alu = Material.objects.get(name='alu cooler')
    #     result = Transaction.transactions_with_annotations(material=alu)
    #     self.assertEqual(result.count(), 2)
    #     self.assertEqual(result[0].net_signed_weight, 8)
    #     self.assertEqual(result[0].net_signed_value, 40)
    #     self.assertEqual(result[0].balance, 8)
    #     self.assertEqual(result[1].net_signed_weight, -16)
    #     self.assertEqual(result[1].net_signed_value, -160)
    #     self.assertEqual(result[1].balance, -8)

    def test_material_group_balance(self):
        alu = MaterialGroup.objects.get(name = 'aluminium')
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,2)), filter_by=alu), 0)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,3)), filter_by=alu), 8)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,4)), filter_by=alu), 8)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,3)), filter_by=alu), 8)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,4)), filter_by=alu), -8)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,5)), filter_by=alu), -8)

    def test_material_balance(self):
        alu = Material.objects.get(name = 'alu cooler')
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,2)), filter_by=alu), 0)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,3)), filter_by=alu), 8)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,4)), filter_by=alu), 8)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,3)), filter_by=alu), 8)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,4)), filter_by=alu), -8)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,5)), filter_by=alu), -8)

    def test_material_group_movement(self):
        alu = MaterialGroup.objects.get(name = 'aluminium')
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,2)), filter_by=alu), 0)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,3)), filter_by=alu), 8)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 8)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,2,3)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 8)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,2,4)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 0)

        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,3,3)), filter_by=alu), 0)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,3,4)), filter_by=alu), 16)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 16)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,3,4)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 16)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,3,5)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 0)

    def test_material_movement(self):
        alu = Material.objects.get(name = 'alu cooler')
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,2)), filter_by=alu), 0)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,3)), filter_by=alu), 8)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 8)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,2,3)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 8)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,2,4)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 0)

        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,3,3)), filter_by=alu), 0)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,3,4)), filter_by=alu), 16)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 16)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,3,4)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 16)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,3,5)), tz.localize(datetime.datetime(2021,5,31)), filter_by=alu), 0)


    def test_transaction_list_view(self):
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/transaction_list.html')
    
    def test_transaction_detail_view(self):
        response = self.client.get(self.goods_receipt.get_absolute_url())
        no_response = self.client.get('/inventories/transactions/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/transaction_detail.html')

    def test_goods_receipt_create_view(self):
        response = self.client.get(reverse('goods_receipt_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventories/goods_receipt_new.html')

    def test_goods_dispatch_create_view(self):
        response = self.client.get(reverse('goods_dispatch_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventories/goods_dispatch_new.html')

    def test_goods_receipt_edit_view(self):
        response = self.client.get(reverse('goods_receipt_edit', args=[f'{self.goods_receipt.id}']))
        no_response = self.client.get('/inventories/goods_receipts/12345/edit')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/goods_receipt_edit.html')

    def test_transaction_delete_view(self):
        response = self.client.get(reverse('transaction_delete', args=[f'{self.goods_receipt.id}']))
        no_response = self.client.get('/inventories/transactions/12345/delete')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertContains(response, 'delete')
        self.assertTemplateUsed(response, 'inventories/transaction_delete.html')
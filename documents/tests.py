# -*- coding: iso-8859-2 -*-

import datetime

from django.test import TestCase, Client
from django.urls import reverse

from .models import GoodsReceiptNote
from partners.models import Vendor
from inventories.models import MaterialGroup, Material, Transaction


class GoodsReceiptNoteTests(TestCase):
    
    def setUp(self):
        
        self.vendor_1 = Vendor.objects.create(
            name = 'Test Vendor',
            country = 'Hungary',
            postcode = '1234',
            city = 'Budapest',
            address = 'Kisvirág utca 23.',
            tax_number = '12345678-2-41',
            is_private_person = False,
            contact_name = 'Nagy János',
            contact_phone = '+36 30 1234567',
            contact_email = 'nagy.janos@email.com',
        )

        self.mat_group = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        self.mat_1 = Material.objects.get_or_create(name='alu cooler', material_group=self.mat_group)[0]
        self.mat_2 = Material.objects.get_or_create(name='alu can', material_group=self.mat_group)[0]
        
        self.transaction_1 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=self.mat_1,
            transaction_time=datetime.date(2021,2,3),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='transaction 1'
        )

        self.transaction_2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=self.mat_2,
            transaction_time=datetime.date(2021,2,3),
            gross_weight=10.0,
            tare_weight=2.0,
            unit_price=5.0,
            notes='transaction 2'
        )

        self.goods_receipt_note_1 = GoodsReceiptNote.objects.create(
            date=datetime.date(2021,2,3),
            vendor=self.vendor_1,
            notes='Some notes'
        )
        self.goods_receipt_note_1.transactions.add(self.transaction_1)
        self.goods_receipt_note_1.transactions.add(self.transaction_2)

        self.goods_receipt_note_2 = GoodsReceiptNote.objects.create(
            date=datetime.date(2021,2,4),
            vendor=self.vendor_1,
            notes='Some notes 2'
        )

    def test_goods_receipt_note_listing(self):
        # grn 1
        self.assertEqual(self.goods_receipt_note_1.date, datetime.date(2021,2,3))
        self.assertEqual(f'{self.goods_receipt_note_1.vendor.name}', 'Test Vendor')
        self.assertEqual(f'{self.goods_receipt_note_1.notes}', 'Some notes')
        self.assertEqual(f'{self.goods_receipt_note_1.grn}', '2021/000001')
        self.assertEqual(self.goods_receipt_note_1.transactions.count(), 2)
        self.assertEqual(list(self.goods_receipt_note_1.transactions.all()), [self.transaction_1, self.transaction_2])
        # grn 2
        self.assertEqual(self.goods_receipt_note_2.date, datetime.date(2021,2,4))
        self.assertEqual(f'{self.goods_receipt_note_2.vendor.name}', 'Test Vendor')
        self.assertEqual(f'{self.goods_receipt_note_2.notes}', 'Some notes 2')
        self.assertEqual(f'{self.goods_receipt_note_2.grn}', '2021/000002')
        self.assertEqual(self.goods_receipt_note_2.transactions.count(), 0)
        self.assertEqual(list(self.goods_receipt_note_2.transactions.all()), [])

    def test_goods_receipt_note_create_view(self):
        response = self.client.get(reverse('goods_receipt_note_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/goods_receipt_note_new.html')

    def test_goods_receipt_note_list_view(self):
        response = self.client.get(reverse('goods_receipt_note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Feb. 3, 2021')
        self.assertContains(response, 'Test Vendor')
        self.assertContains(response, '2021/000001')
        self.assertContains(response, '2021/000002')
        self.assertTemplateUsed(response, 'documents/goods_receipt_note_list.html')
    
    def test_goods_receipt_note_detail_view(self):
        response = self.client.get(self.goods_receipt_note_1.get_absolute_url())
        no_response = self.client.get('/documents/goods_receipt_notes/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Vendor')
        self.assertContains(response, 'alu cooler')
        self.assertContains(response, 'alu can')
        self.assertContains(response, 'Some notes')
        self.assertContains(response, 'transaction 1')
        self.assertContains(response, 'transaction 2')
        self.assertTemplateUsed(response, 'documents/goods_receipt_note_detail.html')
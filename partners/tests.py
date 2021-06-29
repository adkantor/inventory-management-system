# -*- coding: iso-8859-2 -*-

from django.test import TestCase, Client
from django.urls import reverse

from .models import Vendor, Customer


class VendorTests(TestCase):
    
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name = 'Test Customer',
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
 

    def test_vendor_listing(self):
        self.assertEqual(f'{self.vendor.name}', 'Test Customer')
        self.assertEqual(f'{self.vendor.country}', 'Hungary')
        self.assertEqual(f'{self.vendor.postcode}', '1234')
        self.assertEqual(f'{self.vendor.city}', 'Budapest')
        self.assertEqual(f'{self.vendor.address}', 'Kisvirág utca 23.')
        self.assertEqual(f'{self.vendor.tax_number}', '12345678-2-41')
        self.assertFalse(self.vendor.is_private_person)
        self.assertEqual(f'{self.vendor.contact_name}', 'Nagy János')
        self.assertEqual(f'{self.vendor.contact_phone}', '+36 30 1234567')
        self.assertEqual(f'{self.vendor.contact_email}', 'nagy.janos@email.com')

    def test_vendor_list_view(self):
        response = self.client.get(reverse('vendor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Customer')
        self.assertTemplateUsed(response, 'partners/vendor_list.html')
    
    def test_book_detail_view(self):
        response = self.client.get(self.vendor.get_absolute_url())
        no_response = self.client.get('/partners/vendors/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Customer')
        self.assertTemplateUsed(response, 'partners/vendor_detail.html')

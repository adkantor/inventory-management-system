# -*- coding: iso-8859-2 -*-

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

from .models import Vendor, Customer



class VendorTests(TestCase):
    
    def setUp(self):
        
        self.vendor = Vendor.objects.create(
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
        
        self.user = get_user_model().objects.create_user(
            username='authorizeruser', 
            email='user@email.com', 
            password='testPass123'
        )

        self.create_permission = Permission.objects.get(codename='add_vendor')
        self.update_permission = Permission.objects.get(codename='change_vendor')
        self.delete_permission = Permission.objects.get(codename='delete_vendor')
 

    def test_vendor_listing(self):
        self.assertEqual(f'{self.vendor.name}', 'Test Vendor')
        self.assertEqual(f'{self.vendor.country}', 'Hungary')
        self.assertEqual(f'{self.vendor.postcode}', '1234')
        self.assertEqual(f'{self.vendor.city}', 'Budapest')
        self.assertEqual(f'{self.vendor.address}', 'Kisvirág utca 23.')
        self.assertEqual(f'{self.vendor.tax_number}', '12345678-2-41')
        self.assertFalse(self.vendor.is_private_person)
        self.assertEqual(f'{self.vendor.contact_name}', 'Nagy János')
        self.assertEqual(f'{self.vendor.contact_phone}', '+36 30 1234567')
        self.assertEqual(f'{self.vendor.contact_email}', 'nagy.janos@email.com')

    def test_vendor_list_view_for_logged_out_user(self):
        url = reverse('vendor_list')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_vendor_list_view_for_logged_in_user(self):
        url = reverse('vendor_list')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Vendor')
        self.assertTemplateUsed(response, 'partners/partner_list.html')

    def test_vendor_detail_view_for_logged_out_user(self):
        url = self.vendor.get_absolute_url()
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_vendor_detail_view_for_logged_in_user(self):
        url = self.vendor.get_absolute_url()
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        no_response = self.client.get('/partners/vendors/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Vendor')
        self.assertTemplateUsed(response, 'partners/partner_detail.html')

    def test_vendor_create_view_for_logged_out_user(self):
        url = reverse('vendor_new')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_vendor_create_view_for_logged_in_user_without_permission(self):
        url = reverse('vendor_new')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_vendor_create_view_for_logged_in_user_with_permission(self):
        url = reverse('vendor_new')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.create_permission)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partners/partner_new.html')

    def test_vendor_edit_view_for_logged_out_user(self):
        url = reverse('vendor_edit', args=[f'{self.vendor.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_vendor_edit_view_for_logged_in_user_without_permission(self):
        url = reverse('vendor_edit', args=[f'{self.vendor.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_vendor_edit_view_for_logged_in_user_with_permission(self):
        url = reverse('vendor_edit', args=[f'{self.vendor.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.update_permission)
        response = self.client.get(url)
        no_response = self.client.get('/partners/vendors/12345/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Vendor')
        self.assertTemplateUsed(response, 'partners/partner_edit.html')

    def test_vendor_delete_view_for_logged_out_user(self):
        url = reverse('vendor_delete', args=[f'{self.vendor.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')    

    def test_vendor_delete_view_for_logged_in_user_without_permission(self):
        url = reverse('vendor_delete', args=[f'{self.vendor.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  

    def test_vendor_delete_view_for_logged_in_user_with_permission(self):
        url = reverse('vendor_delete', args=[f'{self.vendor.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.delete_permission)
        response = self.client.get(url)
        no_response = self.client.get('/partners/vendors/12345/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Vendor')
        self.assertContains(response, 'delete')
        self.assertTemplateUsed(response, 'partners/partner_delete.html')   


class CustomerTests(TestCase):
    
    def setUp(self):

        self.customer = Customer.objects.create(
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
        
        self.user = get_user_model().objects.create_user(
            username='authorizeruser', 
            email='user@email.com', 
            password='testPass123'
        )

        self.create_permission = Permission.objects.get(codename='add_customer')
        self.update_permission = Permission.objects.get(codename='change_customer')
        self.delete_permission = Permission.objects.get(codename='delete_customer')


    def test_customer_listing(self):
        self.assertEqual(f'{self.customer.name}', 'Test Customer')
        self.assertEqual(f'{self.customer.country}', 'Hungary')
        self.assertEqual(f'{self.customer.postcode}', '1234')
        self.assertEqual(f'{self.customer.city}', 'Budapest')
        self.assertEqual(f'{self.customer.address}', 'Kisvirág utca 23.')
        self.assertEqual(f'{self.customer.tax_number}', '12345678-2-41')
        self.assertFalse(self.customer.is_private_person)
        self.assertEqual(f'{self.customer.contact_name}', 'Nagy János')
        self.assertEqual(f'{self.customer.contact_phone}', '+36 30 1234567')
        self.assertEqual(f'{self.customer.contact_email}', 'nagy.janos@email.com')

    def test_customer_list_view_for_logged_out_user(self):
        url = reverse('customer_list')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_customer_list_view_for_logged_in_user(self):
        url = reverse('customer_list')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Customer')
        self.assertTemplateUsed(response, 'partners/partner_list.html')

    def test_customer_detail_view_for_logged_out_user(self):
        url = self.customer.get_absolute_url()
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_customer_detail_view_for_logged_in_user(self):
        url = self.customer.get_absolute_url()
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        no_response = self.client.get('/partners/customers/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Customer')
        self.assertTemplateUsed(response, 'partners/partner_detail.html')

    def test_customer_create_view_for_logged_out_user(self):
        url = reverse('customer_new')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_customer_create_view_for_logged_in_user_without_permission(self):
        url = reverse('customer_new')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_customer_create_view_for_logged_in_user_with_permission(self):
        url = reverse('customer_new')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.create_permission)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partners/partner_new.html')

    def test_customer_edit_view_for_logged_out_user(self):
        url = reverse('customer_edit', args=[f'{self.customer.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_customer_edit_view_for_logged_in_user_without_permission(self):
        url = reverse('customer_edit', args=[f'{self.customer.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_customer_edit_view_for_logged_in_user_with_permission(self):
        url = reverse('customer_edit', args=[f'{self.customer.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.update_permission)
        response = self.client.get(url)
        no_response = self.client.get('/partners/customers/12345/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Customer')
        self.assertTemplateUsed(response, 'partners/partner_edit.html')

    def test_customer_delete_view_for_logged_out_user(self):
        url = reverse('customer_delete', args=[f'{self.customer.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')    

    def test_customer_delete_view_for_logged_in_user_without_permission(self):
        url = reverse('customer_delete', args=[f'{self.customer.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  

    def test_customer_delete_view_for_logged_in_user_with_permission(self):
        url = reverse('customer_delete', args=[f'{self.customer.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.delete_permission)
        response = self.client.get(url)
        no_response = self.client.get('/partners/customers/12345/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test Customer')
        self.assertContains(response, 'delete')
        self.assertTemplateUsed(response, 'partners/partner_delete.html')
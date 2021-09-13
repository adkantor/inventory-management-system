import datetime
import pytz

from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

from .models import (
    MaterialGroup, Material, Transaction,
    balance, sales_and_purchases, movement_between, weighted_avg_price, period_weighted_avg_price
)

tz = pytz.timezone(settings.TIME_ZONE)



class MaterialGroupTests(TestCase):
    
    def setUp(self):
        
        self.material_group = MaterialGroup.objects.create(
            name = 'aluminium',
        )

        self.user = get_user_model().objects.create_user(
            username='authorizeruser', 
            email='user@email.com', 
            password='testPass123'
        )

        self.create_permission = Permission.objects.get(codename='add_materialgroup')
        self.update_permission = Permission.objects.get(codename='change_materialgroup')
        self.delete_permission = Permission.objects.get(codename='delete_materialgroup')


    def test_material_group_listing(self):
        self.assertEqual(f'{self.material_group.name}', 'aluminium')

    def test_material_group_list_view_for_logged_out_user(self):
        url = reverse('material_group_list')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_material_group_list_view_for_logged_in_user(self):
        url = reverse('material_group_list')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aluminium')
        self.assertTemplateUsed(response, 'inventories/inventory_list.html')

    def test_material_group_detail_view_for_logged_out_user(self):
        url = self.material_group.get_absolute_url()
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_material_group_detail_view_for_logged_in_user(self):
        url = self.material_group.get_absolute_url()
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        no_response = self.client.get('/inventories/material_groups/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'aluminium')
        self.assertTemplateUsed(response, 'inventories/inventory_detail.html')

    def test_material_group_create_view_for_logged_out_user(self):
        url = reverse('material_group_new')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_material_group_create_view_for_logged_in_user_without_permission(self):
        url = reverse('material_group_new')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_material_group_create_view_for_logged_in_user_with_permission(self):
        url = reverse('material_group_new')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.create_permission)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventories/inventory_new.html')

    def test_material_group_edit_view_for_logged_out_user(self):
        url = reverse('material_group_edit', args=[f'{self.material_group.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_material_group_edit_view_for_logged_in_user_without_permission(self):
        url = reverse('material_group_edit', args=[f'{self.material_group.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_material_group_edit_view_for_logged_in_user_with_permission(self):
        url = reverse('material_group_edit', args=[f'{self.material_group.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.update_permission)
        response = self.client.get(url)
        no_response = self.client.get('/inventories/material_groups/12345/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'aluminium')
        self.assertTemplateUsed(response, 'inventories/inventory_edit.html')

    def test_material_group_delete_view_for_logged_out_user(self):
        url = reverse('material_group_delete', args=[f'{self.material_group.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')    

    def test_material_group_delete_view_for_logged_in_user_without_permission(self):
        url = reverse('material_group_delete', args=[f'{self.material_group.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  

    def test_material_group_delete_view_for_logged_in_user_with_permission(self):
        url = reverse('material_group_delete', args=[f'{self.material_group.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.delete_permission)
        response = self.client.get(url)
        no_response = self.client.get('/inventories/material_groups/12345/delete/')
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

        self.user = get_user_model().objects.create_user(
            username='authorizeruser', 
            email='user@email.com', 
            password='testPass123'
        )

        self.create_permission = Permission.objects.get(codename='add_material')
        self.update_permission = Permission.objects.get(codename='change_material')
        self.delete_permission = Permission.objects.get(codename='delete_material')


    def test_material_listing(self):
        self.assertEqual(f'{self.material.name}', 'alu cooler')
        self.assertEqual(f'{self.material.material_group.name}', 'aluminium')

    def test_material_list_view_for_logged_out_user(self):
        url = reverse('material_list')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_material_list_view_for_logged_in_user(self):
        url = reverse('material_list')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/inventory_list.html')

    def test_material_detail_view_for_logged_out_user(self):
        url = self.material.get_absolute_url()
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_material_detail_view_for_logged_in_user(self):
        url = self.material.get_absolute_url()
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        no_response = self.client.get('/inventories/materials/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/inventory_detail.html')

    def test_material_create_view_for_logged_out_user(self):
        url = reverse('material_new')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_material_create_view_for_logged_in_user_without_permission(self):
        url = reverse('material_new')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_material_create_view_for_logged_in_user_with_permission(self):
        url = reverse('material_new')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.create_permission)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventories/inventory_new.html')

    def test_material_edit_view_for_logged_out_user(self):
        url = reverse('material_edit', args=[f'{self.material.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_material_edit_view_for_logged_in_user_without_permission(self):
        url = reverse('material_edit', args=[f'{self.material.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_material_edit_view_for_logged_in_user_with_permission(self):
        url = reverse('material_edit', args=[f'{self.material.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.update_permission)
        response = self.client.get(url)
        no_response = self.client.get('/inventories/materials/12345/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'alu cooler')
        self.assertTemplateUsed(response, 'inventories/inventory_edit.html')

    def test_material_delete_view_for_logged_out_user(self):
        url = reverse('material_delete', args=[f'{self.material.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')    

    def test_material_delete_view_for_logged_in_user_without_permission(self):
        url = reverse('material_delete', args=[f'{self.material.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)  

    def test_material_delete_view_for_logged_in_user_with_permission(self):
        url = reverse('material_delete', args=[f'{self.material.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.delete_permission)
        response = self.client.get(url)
        no_response = self.client.get('/inventories/materials/12345/delete/')
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



class CalculationTests(TestCase):
    
    def setUp(self):
        mat_group = MaterialGroup.objects.get_or_create(name = 'aluminium')[0]
        mat = Material.objects.get_or_create(name='alu cooler', material_group=mat_group)[0]
        
        self.goods_receipt_1 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat,
            transaction_time=tz.localize(datetime.datetime(2021,2,3,2,1)),
            gross_weight=32.0,
            tare_weight=2.0,
            unit_price=10.0,
            notes='some notes'
        )

        self.goods_receipt_2 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat,
            transaction_time=tz.localize(datetime.datetime(2021,2,3,4,5)),
            gross_weight=72.0,
            tare_weight=2.0,
            unit_price=10.0,
            notes='some notes'
        )

        self.goods_dispatch_1 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_OUT,
            material=mat,
            transaction_time=tz.localize(datetime.datetime(2021,3,4)),
            gross_weight=54.0,
            tare_weight=4.0,
            unit_price=30.0,
            notes='some notes'
        )

        self.goods_receipt_3 = Transaction.objects.create(
            transaction_type=Transaction.TYPE_IN,
            material=mat,
            transaction_time=tz.localize(datetime.datetime(2021,6,3)),
            gross_weight=152.0,
            tare_weight=2.0,
            unit_price=15.0,
            notes='some notes'
        )

    def test_material_group_balance(self):
        alu = MaterialGroup.objects.get(name = 'aluminium')
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,2,23,59)), filter_by=alu), 0)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,3,23,59)), filter_by=alu), 100)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,4,23,59)), filter_by=alu), 100)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,3,23,59)), filter_by=alu), 100)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,4,23,59)), filter_by=alu), 50)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,5,23,59)), filter_by=alu), 50)

    def test_material_balance(self):
        alu = Material.objects.get(name = 'alu cooler')
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,2,23,59)), filter_by=alu), 0)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,3,23,59)), filter_by=alu), 100)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,2,4,23,59)), filter_by=alu), 100)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,3,23,59)), filter_by=alu), 100)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,4,23,59)), filter_by=alu), 50)
        self.assertEqual(balance(tz.localize(datetime.datetime(2021,3,5,23,59)), filter_by=alu), 50)

    def test_material_group_sales_and_purchases(self):
        alu = MaterialGroup.objects.get(name = 'aluminium')
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,2,23,59)), filter_by=alu), (0, 0))
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,3,23,59)), filter_by=alu), (0, -1000))
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,2,3)), tz.localize(datetime.datetime(2021,2,3,23,59)), filter_by=alu), (0, -1000))
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,2,4)), tz.localize(datetime.datetime(2021,2,4,23,59)), filter_by=alu), (0, 0))
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,3,4)), tz.localize(datetime.datetime(2021,3,4,23,59)), filter_by=alu), (1500, 0))

    def test_material_sales_and_purchases(self):
        alu = Material.objects.get(name = 'alu cooler')
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,2,23,59)), filter_by=alu), (0, 0))
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,3,23,59)), filter_by=alu), (0, -1000))
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,2,3)), tz.localize(datetime.datetime(2021,2,3,23,59)), filter_by=alu), (0, -1000))
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,2,4)), tz.localize(datetime.datetime(2021,2,4,23,59)), filter_by=alu), (0, 0))
        self.assertEqual(sales_and_purchases(tz.localize(datetime.datetime(2021,3,4)), tz.localize(datetime.datetime(2021,3,4,23,59)), filter_by=alu), (1500, 0))

    def test_material_group_movement(self):
        alu = MaterialGroup.objects.get(name = 'aluminium')
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,2,23,59)), filter_by=alu), 0)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,3,23,59)), filter_by=alu), 100)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 100)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,2,3)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 100)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,2,4)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 0)

        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,3,3,23,59)), filter_by=alu), 0)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,3,4,23,59)), filter_by=alu), 50)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 50)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,3,4)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 50)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,3,5)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 0)

    def test_material_movement(self):
        alu = Material.objects.get(name = 'alu cooler')
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,2,23,59)), filter_by=alu), 0)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,2,3,23,59)), filter_by=alu), 100)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 100)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,2,3)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 100)
        self.assertEqual(movement_between(Transaction.TYPE_IN, tz.localize(datetime.datetime(2021,2,4)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 0)

        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,3,3,23,59)), filter_by=alu), 0)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,3,4,23,59)), filter_by=alu), 50)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,1,1)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 50)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,3,4)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 50)
        self.assertEqual(movement_between(Transaction.TYPE_OUT, tz.localize(datetime.datetime(2021,3,5)), tz.localize(datetime.datetime(2021,5,31,23,59)), filter_by=alu), 0)

    def test_material_group_weighted_avg_price(self):
        alu = MaterialGroup.objects.get(name = 'aluminium')
        self.assertEqual(weighted_avg_price(tz.localize(datetime.datetime(2021,2,1)), filter_by=alu), 0)
        self.assertEqual(weighted_avg_price(tz.localize(datetime.datetime(2021,2,4)), filter_by=alu), 10)
        self.assertEqual(weighted_avg_price(tz.localize(datetime.datetime(2021,3,5)), filter_by=alu), 10)
        self.assertEqual(weighted_avg_price(tz.localize(datetime.datetime(2021,6,5)), filter_by=alu), 13.75)

    def test_material_weighted_avg_price(self):
        alu = Material.objects.get(name = 'alu cooler')
        self.assertEqual(weighted_avg_price(tz.localize(datetime.datetime(2021,2,1)), filter_by=alu), 0)
        self.assertEqual(weighted_avg_price(tz.localize(datetime.datetime(2021,2,4)), filter_by=alu), 10)
        self.assertEqual(weighted_avg_price(tz.localize(datetime.datetime(2021,3,5)), filter_by=alu), 10)
        self.assertEqual(weighted_avg_price(tz.localize(datetime.datetime(2021,6,5)), filter_by=alu), 13.75)

    def test_material_group_period_weighted_avg_price(self):
        alu = MaterialGroup.objects.get(name = 'aluminium')
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_IN, 
                tz.localize(datetime.datetime(2021,2,1)), 
                tz.localize(datetime.datetime(2021,2,2) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 0)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_IN, 
                tz.localize(datetime.datetime(2021,2,1)), 
                tz.localize(datetime.datetime(2021,2,4) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 10)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_IN, 
                tz.localize(datetime.datetime(2021,2,1)), 
                tz.localize(datetime.datetime(2021,6,5) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 13)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_IN, 
                tz.localize(datetime.datetime(2021,3,1)), 
                tz.localize(datetime.datetime(2021,6,5) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 15)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_OUT, 
                tz.localize(datetime.datetime(2021,3,1)), 
                tz.localize(datetime.datetime(2021,3,4) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 0)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_OUT, 
                tz.localize(datetime.datetime(2021,3,1)), 
                tz.localize(datetime.datetime(2021,3,5) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 30)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_OUT, 
                tz.localize(datetime.datetime(2021,3,5)), 
                tz.localize(datetime.datetime(2021,3,10) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 0)   

    def test_material_period_weighted_avg_price(self):
        alu = Material.objects.get(name = 'alu cooler')
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_IN, 
                tz.localize(datetime.datetime(2021,2,1)), 
                tz.localize(datetime.datetime(2021,2,2) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 0)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_IN, 
                tz.localize(datetime.datetime(2021,2,1)), 
                tz.localize(datetime.datetime(2021,2,4) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 10)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_IN, 
                tz.localize(datetime.datetime(2021,2,1)), 
                tz.localize(datetime.datetime(2021,6,5) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 13)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_IN, 
                tz.localize(datetime.datetime(2021,3,1)), 
                tz.localize(datetime.datetime(2021,6,5) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 15)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_OUT, 
                tz.localize(datetime.datetime(2021,3,1)), 
                tz.localize(datetime.datetime(2021,3,4) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 0)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_OUT, 
                tz.localize(datetime.datetime(2021,3,1)), 
                tz.localize(datetime.datetime(2021,3,5) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 30)
        self.assertEqual(
            period_weighted_avg_price(
                Transaction.TYPE_OUT, 
                tz.localize(datetime.datetime(2021,3,5)), 
                tz.localize(datetime.datetime(2021,3,10) - datetime.timedelta(microseconds=1)), 
                filter_by=alu
            ), 0)   
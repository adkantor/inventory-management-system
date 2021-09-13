from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission



class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        u1 = User.objects.create_user(
            username='normal_user',
            email='abcd@gmail.com',
            password='test1'
        )
        self.assertEqual(u1.username, 'normal_user')
        self.assertEqual(u1.email, 'abcd@gmail.com')
        self.assertTrue(u1.is_active)
        self.assertFalse(u1.is_staff)
        self.assertFalse(u1.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        u1 = User.objects.create_superuser(
            username='super_user',
            email='efgh@gmail.com',
            password='test1'
        )
        self.assertEqual(u1.username, 'super_user')
        self.assertEqual(u1.email, 'efgh@gmail.com')
        self.assertTrue(u1.is_active)
        self.assertTrue(u1.is_staff)
        self.assertTrue(u1.is_superuser)

    def test_statuses(self):
        User = get_user_model()
        User.objects.create_user(
            username='boss',
            email='boss@email.com',
            password='test1'
        )
        User.objects.create_user(
            username='staff',
            email='staff@email.com',
            password='test2'
        )
        User.objects.create_user(
            username='inactive',
            email='inactive@email.com',
            password='test3',
            is_active=False
        )
        result = User.statuses()
        self.assertEqual(len(result), 2)



class EmployeesTests(TestCase):

    def setUp(self):
        
        self.user = get_user_model().objects.create_user(
            username='authorizeruser', 
            email='user@email.com', 
            password='testPass123'
        )

        self.employee = get_user_model().objects.create_user(
            username='employee', 
            email='employee@email.com', 
            password='testPass123'
        )

        self.special_permission = Permission.objects.get(codename='can_view_all_users')
        self.create_permission = Permission.objects.get(codename='can_add_user')
        self.delete_permission = Permission.objects.get(codename='can_delete_all_users')

    def test_employee_list_view_for_logged_out_user(self):
        url = reverse('employee_list')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_employee_list_view_for_logged_in_user_without_permission(self):
        url = reverse('employee_list')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_employee_list_view_for_logged_in_user_with_permission(self):
        url = reverse('employee_list')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'employee@email.com')
        self.assertTemplateUsed(response, 'users/employee_list.html')

    def test_employee_detail_view_for_logged_out_user(self):
        url = reverse('employee_detail', args=[f'{self.employee.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_employee_detail_view_for_logged_in_user_without_permission(self):
        url = reverse('employee_detail', args=[f'{self.employee.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_employee_detail_view_for_logged_in_user_with_permission(self):
        url = reverse('employee_detail', args=[f'{self.employee.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(url)
        no_response = self.client.get('/users/employees/12345/detail/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'employee@email.com')
        self.assertTemplateUsed(response, 'users/employee_detail.html')

    def test_employee_edit_view_for_logged_out_user(self):
        url = reverse('employee_edit', args=[f'{self.employee.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_employee_edit_view_for_logged_in_user_without_permission(self):
        url = reverse('employee_edit', args=[f'{self.employee.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_employee_edit_view_for_logged_in_user_with_permission(self):
        url = reverse('employee_edit', args=[f'{self.employee.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(url)
        no_response = self.client.get('/users/employees/12345/edit/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'First name')
        self.assertTemplateUsed(response, 'users/employee_edit.html')

    def test_employee_create_view_for_logged_out_user(self):
        url = reverse('employee_create')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_employee_create_view_for_logged_in_user_without_permission(self):
        url = reverse('employee_create')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_employee_create_view_for_logged_in_user_with_permission(self):
        url = reverse('employee_create')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.create_permission)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First Name')

    def test_employee_delete_view_for_logged_out_user(self):
        url = reverse('employee_delete', args=[f'{self.employee.id}'])
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_employee_delete_view_for_logged_in_user_without_permission(self):
        url = reverse('employee_delete', args=[f'{self.employee.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_employee_delete_view_for_logged_in_user_with_permission(self):
        url = reverse('employee_delete', args=[f'{self.employee.id}'])
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        # add permission
        self.user.user_permissions.add(self.delete_permission)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure')
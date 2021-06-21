from django.test import TestCase

from django.contrib.auth import get_user_model



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
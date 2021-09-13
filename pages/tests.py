from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

from .views import HomePageView


class HomepageTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username='authorizeruser', 
            email='user@email.com', 
            password='testPass123'
        )


    def test_homepage_view_for_logged_out_user(self):
        url = reverse('home')
        # log-out user
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{reverse("account_login")}?next={url}')
        response = self.client.get(f'{reverse("account_login")}?next={url}')
        self.assertContains(response, 'Sign In')

    def test_homepage_view_for_logged_in_user(self):
        url = reverse('home')
        # log-in user
        self.client.login(email='user@email.com', password='testPass123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inventory Management System')
        self.assertTemplateUsed(response, 'home.html')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        password_tk = 'my_Pass'
        User.objects.create_user(username='my_user', password=password_tk)
        self.client.login(username='my_user', password=password_tk)

        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertIn(
            'Invalid logout request',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_with_another_user(self):
        password_tk = 'my_Pass'
        User.objects.create_user(username='my_user', password=password_tk)
        self.client.login(username='my_user', password=password_tk)

        response = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={
                'username': 'another_user'
            }
        )
        self.assertIn(
            'Invalid logout user',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_successfully(self):
        password_tk = 'my_Pass'
        User.objects.create_user(username='my_user', password=password_tk)
        self.client.login(username='my_user', password=password_tk)

        response = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={
                'username': 'my_user'
            }
        )
        self.assertIn(
            'Logged out successfully',
            response.content.decode('utf-8')
        )

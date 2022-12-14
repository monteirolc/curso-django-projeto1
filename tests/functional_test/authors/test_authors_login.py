import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password)
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder_input(
            form, 'Type your username')
        password_field = self.get_by_placeholder_input(
            form, 'Type your password')

        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        form.submit()

        self.assertIn('You are logged in with my_user.',
                      self.browser.find_element(By.TAG_NAME, 'body').text
                      )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_show_error_message_if_user_is_wrong(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username = form.find_element(By.NAME, 'username')
        password = form.find_element(By.NAME, 'password')
        username.send_keys('Blabla')
        password.send_keys('1245')
        form.submit()
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_empty_show_error_message_if_user_is_wrong(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login'))
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username = form.find_element(By.NAME, 'username')
        password = form.find_element(By.NAME, 'password')
        username.send_keys('')
        password.send_keys('')
        form.submit()
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

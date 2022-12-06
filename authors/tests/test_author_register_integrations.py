from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': ' first',
            'last_name': ' last',
            'email': 'email@email.com',
            'password': 'A@bc12345678',
            'password2': 'A@bc12345678',

        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Username not be empty, It must have between 3 and 40 chars'),  # noqa
        ('first_name', 'First name is required'),
        ('last_name', 'Last name is required'),
        ('password', 'Password must not be empty'),
        ('password2', 'Password confirmation must not be empty'),
        ('email', 'E-mail not be empty')
    ])
    def test_fields_connot_be_empty_showing_error_messages(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get(field))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_min_length_should_be_3(self):
        self.form_data['username'] = 'Ed'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Min length is 3'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_length_should_be_40(self):
        self.form_data['username'] = 'E' * 41
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Max length is 40'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_is_strong(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@Aabc1234'
        self.form_data['password2'] = '@Aabc12345'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Password and Password confirmation must be equal'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_send_valid_post_request_to_registration_create_view_returns_valid_message(self):  # noqa
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Your user is created, please log in.'
        self.assertIn(msg, response.content.decode('utf-8'))

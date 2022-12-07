from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('password', 'Type your password here'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('email', 'The e-mail must be valid',),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password confirmation'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Username not be empty, It must have between 3 and 40 chars'),  # noqa
        ('first_name', 'First name is required'),
        ('last_name', 'Last name is required'),
        ('password', 'Password must not be empty'),
        ('password2', 'Password confirmation must not be empty'),
        ('email', 'E-mail not be empty and must be unique.')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'Ed'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Min length is 3'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'E' * 41
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Max length is 40'
        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@Aabc1234'
        self.form_data['password2'] = '@Aabc12345'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Password and Password confirmation must be equal'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'testuser',
            'email': 'maile@mailmail.com',
            'password': '@Bc123456',
            'password2': '@Bc123456',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc123456'
        )

        self.assertTrue(is_authenticated)

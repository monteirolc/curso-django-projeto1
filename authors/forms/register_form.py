from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_attr, add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['password'], 'Type your password here')
        add_placeholder(self.fields['password2'], 'Repeat your password')

        add_attr(self.fields['username'], 'css', 'a-css-class')

    last_name = forms.CharField(
        label='Last name',
        error_messages={'required': 'Last name is required'},
        help_text='Enter up to 150 chars',
    )

    first_name = forms.CharField(
        label='First name',
        error_messages={'required': 'First name is required'},
        help_text='Enter up to 150 chars'
    )

    password = forms.CharField(
        error_messages={'required': 'Password must not be empty'},
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password],
        label='Password',
        widget=forms.PasswordInput(

        )
    )

    password2 = forms.CharField(
        label='Password confirmation',
        error_messages={'required': 'Password confirmation must not be empty'},
        widget=forms.PasswordInput(

        )
    )

    email = forms.EmailField(
        label='E-mail',
        error_messages={'required': 'E-mail not be empty and must be unique.'},
        help_text='The e-mail must be valid',
    )

    username = forms.CharField(
        label='Username',
        error_messages={
            'required': 'Username not be empty, It must have between 3 and 40 chars',  # noqa
            'min_length': 'Min length is 3',
            'max_length': 'Max length is 40',
        },
        help_text='The username must be valid',
        min_length=3,
        max_length=40,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password2': 'Password and Password confirmation must be equal'
            })

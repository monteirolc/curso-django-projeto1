from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

DICT = {'1234'}


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    password2 = forms.CharField(
        required=True,
        label='Password confirmation',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        }),
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
        # exclude = []

        labels = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'username': 'username',
            'email': 'email',
            'password': 'password',
        }

        help_text = {
            'email': 'The e-mail must be valid',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty',
                'invalid': 'This field is invalid',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your first name here',
                'class': 'outra_classe'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Input your key pass here'
            })
        }

    def clean_password(self):
        data = self.cleaned_data.get('password')

        for i in len(DICT):
            if DICT[i] in data:
                raise ValidationError(
                    "Valor proibido",
                    code='invalid'

                )

        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password2': 'Password and Password confirmation must be equal'
            })

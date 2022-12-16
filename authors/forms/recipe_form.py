from collections import defaultdict

from django.core.exceptions import ValidationError
from django.forms import FileInput, ModelForm, Select

from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorRecipeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time',\
            'preparation_time_unit', 'servings', 'servings_unit',\
            'preparation_steps', 'cover'
        widgets = {
            'cover': FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                    ('Dias', 'Dias'),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        description = cleaned_data.get('description')
        title = cleaned_data.get('title')
        if len(title) < 5:
            self._my_errors['title'].append('title is too short')
        if len(description) < 5:
            self._my_errors['description'].append('Description is too short')

        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean

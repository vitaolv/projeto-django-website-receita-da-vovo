from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    title = forms.CharField(
        label="Título",
    )

    description = forms.CharField(
        label="Descrição",
        widget=forms.Textarea(),
    )

    preparation_time = forms.IntegerField(
        label="Tempo de preparação",
    )

    preparation_time_unit = forms.CharField(
        label="Unidade de tempo de preparação",
        widget=forms.Select(
            choices=(
                ('Minutos', 'Minutos'),
                ('Horas', 'Horas'),
            ),
        ),
    )

    servings = forms.IntegerField(
        label="Rendimento",
    )

    servings_unit = forms.CharField(
        label="Unidade de rendimento",
        widget=forms.Select(
            choices=(
                ('Porções', 'Porções'),
                ('Pedaços', 'Pedaços'),
                ('Pessoas', 'Pessoas'),
            ),
        ),
    )

    preparation_steps = forms.CharField(
        label="Modo de preparação",
        widget=forms.Textarea(),
    )

    cover = forms.ImageField(
        label='Imagem',
        widget=forms.FileInput(
            attrs={
                'class': 'span-2'
            }
        ),
        required=False,
    )

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'cover']

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleanData = self.cleaned_data

        title = cleanData.get('title')
        description = cleanData.get('description')

        if title == description:
            self._my_errors['title'].append(
                'O título não pode ser igual à descrição.')
            self._my_errors['description'].append(
                'A descrição não pode ser igual ao título.')

        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append(
                'O título deve ter no mínimo 5 caracteres.')
        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append(
                'O campo deve ser um número positivo.')
        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append(
                'O campo deve ser um número positivo.')
        return field_value

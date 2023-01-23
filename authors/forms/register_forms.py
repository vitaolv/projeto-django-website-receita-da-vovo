from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['first_name'], 'Exemplo: Anne...')
        add_placeholder(self.fields['last_name'], 'Exemplo: Silva Dutra...')
        add_placeholder(self.fields['username'], 'Exemplo: AnneSD...')
        add_placeholder(self.fields['email'], 'Exemplo: annesd@mail.com...')
        add_placeholder(self.fields['password'], 'Digite sua senha...')
        add_placeholder(self.fields['password_confirm'],
                        'Redigite sua senha para confirmação...')

    first_name = forms.CharField(
        label="Nome",
        error_messages={
            'required': ('O nome não deve estar vazio. '
                         'Por favor, preencha este formulário.'),
            'min_length': 'O nome deve conter pelo menos 2 caracteres. '
            'Por favor, preencha este formulário corretamente.',
            'max_length': 'O nome não deve ultrapassar o limite máximo'
            'de 64 caracteres. Tente novamente.'
        },
        help_text=(
            'Pode escrever o seu nome ou seu apelido. No entanto, '
            'o comprimento do nome deve estar entre 2 a 64 caracteres.'
        ),
        min_length=2,
        max_length=64,
    )

    last_name = forms.CharField(
        label="Sobrenome",
        error_messages={
            'required': ('O sobrenome não deve estar vazio. '
                         'Por favor, preencha este formulário.'),
            'min_length': 'O sobrenome deve conter pelo menos 2 caracteres. '
            'Por favor, preencha este formulário corretamente.',
            'max_length': 'O sobrenome não deve ultrapassar o limite máximo'
            'de 128 caracteres. Tente novamente.'
        },
        help_text=(
            'Pode escrever um sobrenome completo ou abreviar o seu sobrenome, '
            'por exemplo: "D." apenas. No entanto, '
            'o comprimento do sobrenome deve estar entre 2 a 128 caracteres.'
        ),
        min_length=2,
        max_length=128,
    )

    username = forms.CharField(
        label='Usuário',
        error_messages={
            'required': 'O nome de usuário não deve estar vazio. '
            'Por favor, preencha este formulário.',
            'min_length': 'O nome de usuário deve ter 4 caracteres '
            'pelo menos.',
            'max_length': 'O nome de usuário não deve ultrapassar o limite '
            'máximo de 64 caracteres.',
        },
        help_text=(
            ('O comprimento de nome de usuário deve estar entre 4 a 64 '
             'caracteres. Pode incluir letras, números e '
             '@/./+/-/_.')
        ),
        min_length=4,
        max_length=64,
    )

    email = forms.CharField(
        label='Endereço de e-mail',
        error_messages={
            'required': ('O email não deve estar vazio. '
                         'Por favor, preencha este formulário.'),
            'invalid': 'O e-mail é inválido. Por favor, tente novamente.',
        },
        help_text=(
            'Coloque o seu melhor e-mail válido e registrado.'
        ),
    )

    password = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': ('A senha não deve estar vazia. '
                         'Por favor, preencha este formulário.'),
        },
        help_text=(
            ('A senha deve ter pelo menos uma letra maiúscula, '
             'uma letra minúscula e um número. '
             'O comprimento deve ter pelo menos 8 caracteres.')
        ),
        validators=[strong_password]
    )

    password_confirm = forms.CharField(
        label='Confirme a senha',
        required=True,
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A senha não deve estar vazia. '
            'Por favor, preencha este formulário.'
        },
        help_text=(
            'A senha de confirmação deve ser igual à senha que você digitou.'
        ),
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

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'Este e-mail já está em uso, tente novamente.',
                code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        password_is_ok = ''

        if password != password_confirm:
            password_confirmation_error = ValidationError(
                'A senha de confirmação é diferente da senha digitada. '
                'Por favor, verifique e tente novamente.',
                code='invalid'
            )
            raise ValidationError({
                'password': password_is_ok,
                'password_confirm': password_confirmation_error,
            })

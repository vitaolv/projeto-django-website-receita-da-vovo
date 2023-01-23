from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized

from authors.forms import RegisterForm


class authorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Exemplo: Anne...'),
        ('last_name', 'Exemplo: Silva Dutra...'),
        ('username', 'Exemplo: AnneSD...'),
        ('email', 'Exemplo: annesd@mail.com...'),
        ('password', 'Digite sua senha...'),
        ('password_confirm', 'Redigite sua senha para confirmação...'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('first_name', (
            'Pode escrever o seu nome ou seu apelido. No entanto, '
            'o comprimento do nome deve estar entre 2 a 64 caracteres.'
        )
        ),
        ('last_name', (
            'Pode escrever um sobrenome completo ou abreviar o seu sobrenome, '
            'por exemplo: "D." apenas. No entanto, '
            'o comprimento do sobrenome deve estar entre 2 a 128 caracteres.'
        )
        ),
        ('username', (
            'O comprimento de nome de usuário deve estar entre 4 a 64 '
            'caracteres. Pode incluir letras, números e '
            '@/./+/-/_.'
        )
        ),
        ('email', ('Coloque o seu melhor e-mail válido e registrado.'
                   )
         ),
        ('password', (
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. '
            'O comprimento deve ter pelo menos 8 caracteres.'
        )
        ),
        ('password_confirm', (
         'A senha de confirmação deve ser igual à senha que você digitou.'
         )
         ),
    ])
    def test_text_help_is_correct(self, field, needed):
        form = RegisterForm()
        current_text_help = form[field].field.help_text
        self.assertEqual(current_text_help, needed)

    @ parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Usuário'),
        ('email', 'Endereço de e-mail'),
        ('password', 'Senha'),
        ('password_confirm', 'Confirme a senha'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntergrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'first_name': 'first',
            'last_name': 'last',
            'username': 'user',
            'email': 'email@anyemail.com',
            'password': 'Password_1',
            'password_confirm': 'Password_1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'O nome não deve estar vazio. '
         'Por favor, preencha este formulário.'),

        ('last_name', 'O sobrenome não deve estar vazio. '
         'Por favor, preencha este formulário.'),

        ('username', 'O nome de usuário não deve estar vazio. '
         'Por favor, preencha este formulário.'),

        ('email', 'O email não deve estar vazio. '
         'Por favor, preencha este formulário.'),

        ('password', 'A senha não deve estar vazia. '
         'Por favor, preencha este formulário.'),

        ('password_confirm', 'A senha não deve estar vazia. '
         'Por favor, preencha este formulário.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_first_name_min_length_sould_be_2(self):
        msg = (
            'O nome deve conter pelo menos 2 caracteres. '
            'Por favor, preencha este formulário corretamente.'
        )

        self.form_data['first_name'] = 'A'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get('first_name'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_first_name_max_length_sould_be_64(self):
        msg = (
            'O nome não deve ultrapassar o limite máximo'
            'de 64 caracteres. Tente novamente.'
        )

        self.form_data['first_name'] = 'A' * 65

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get('first_name'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_last_name_min_length_sould_be_2(self):
        msg = (
            'O sobrenome deve conter pelo menos 2 caracteres. '
            'Por favor, preencha este formulário corretamente.'
        )

        self.form_data['last_name'] = 'A'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get('last_name'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_last_name_max_length_sould_be_128(self):
        msg = (
            'O sobrenome não deve ultrapassar o limite máximo'
            'de 128 caracteres. Tente novamente.'
        )

        self.form_data['last_name'] = 'A' * 129

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get('last_name'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_min_length_sould_be_4(self):
        msg = 'O nome de usuário deve ter 4 caracteres pelo menos.'
        self.form_data['username'] = 'joe'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_sould_be_64(self):
        msg = (
            'O nome de usuário não deve ultrapassar o limite '
            'máximo de 64 caracteres.'
        )
        self.form_data['username'] = 'A' * 65
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_email_is_invalid(self):

        msg = 'O e-mail é inválido. Por favor, tente novamente.'
        self.form_data['email'] = 'email@invalid'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):

        msg = (
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. '
            'O comprimento deve ter pelo menos 8 caracteres.'
        )
        self.form_data['password'] = 'abc123'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@ABCabc123'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):

        msg = (
            'A senha de confirmação é diferente da senha digitada. '
            'Por favor, verifique e tente novamente.'
        )
        self.form_data['password'] = '@ABCabc123'
        self.form_data['password_confirm'] = '@ABcabc1233'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(
            msg, response.context['form'].errors.get('password_confirm'))

        self.form_data['password'] = '@ABCabc123'
        self.form_data['password_confirm'] = '@ABCabc123'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        msg = 'Este e-mail já está em uso, tente novamente.'

        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password_confirm': '@Bc123456',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc123456'
        )

        self.assertTrue(is_authenticated)

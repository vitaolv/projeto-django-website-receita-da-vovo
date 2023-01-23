import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import authorsBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(authorsBaseTest):
    def fill_form_dummy_data(self, form):

        fields = form.find_elements(By.TAG_NAME, "input")

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/section/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + "/authors/register/")

        form = self.get_form()
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        self.sleep(3)
        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(
                form, 'Exemplo: Anne...')

            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('O nome não deve estar vazio.', form.text)

        self.sleep(3)
        self.form_field_test_with_callback(callback)

    def test_invalid_min_length_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(
                form, 'Exemplo: Silva Dutra...'
            )
            first_name_field.send_keys('A')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(
                ('O nome deve conter pelo menos 2 caracteres. '
                 'Por favor, preencha este formulário corretamente.'),
                form.text
            )

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(
                form, 'Exemplo: Silva Dutra...'
            )
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('O sobrenome não deve estar vazio.', form.text)
        self.sleep(3)
        self.form_field_test_with_callback(callback)

    def test_invalid_min_length_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(
                form, 'Exemplo: Silva Dutra...'
            )
            last_name_field.send_keys('A')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(
                ('O sobrenome deve conter pelo menos 2 caracteres. '
                 'Por favor, preencha este formulário corretamente.'),
                form.text
            )

        self.sleep(3)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(
                form, 'Exemplo: AnneSD...'
            )

            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(('O nome de usuário não deve estar vazio. '
                           'Por favor, preencha este formulário.'), form.text)
        self.sleep(3)
        self.form_field_test_with_callback(callback)

    def test_invalid_min_length_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(
                form, 'Exemplo: AnneSD...'
            )
            username_field.send_keys('A')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(
                ('O nome de usuário deve ter 4 caracteres '
                 'pelo menos.'),
                form.text
            )

        self.sleep(3)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(
                form, 'Exemplo: annesd@mail.com...'
            )
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(
                'O e-mail é inválido. Por favor, tente novamente.',
                form.text
            )

        self.sleep(3)
        self.form_field_test_with_callback(callback)

    def test_empty_password_error_message(self):
        def callback(form):
            password_field = self.get_by_placeholder(
                form,
                'Digite sua senha...'
            )

            password_field.send_keys(' ')
            password_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(
                ('A senha não deve estar vazia. '
                 'Por favor, preencha este formulário.'),
                form.text
            )

        self.sleep(3)
        self.form_field_test_with_callback(callback)

    def test_invalid_password_error_message(self):
        def callback(form):
            password_field = self.get_by_placeholder(
                form,
                'Digite sua senha...'
            )

            password_field.send_keys('password')

            password_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(
                (
                    'A senha deve ter pelo menos uma letra maiúscula, '
                    'uma letra minúscula e um número. '
                    'O comprimento deve ter pelo menos 8 caracteres.'
                ),
                form.text
            )

        self.sleep(3)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):
        def callback(form):
            password_field = self.get_by_placeholder(
                form,
                'Digite sua senha...'
            )

            password_confirm_field = self.get_by_placeholder(
                form,
                'Redigite sua senha para confirmação...'
            )

            password_field.send_keys('PASS_123_pass')
            password_confirm_field.send_keys('PASS_123_different')
            password_confirm_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn(
                ('A senha de confirmação é diferente da senha digitada. '
                 'Por favor, verifique e tente novamente.'),
                form.text
            )
        self.sleep(3)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfylly(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(
            form, 'Exemplo: Anne...').send_keys('First Name')
        self.get_by_placeholder(
            form, 'Exemplo: Silva Dutra...').send_keys('Last Name')
        self.get_by_placeholder(
            form, 'Exemplo: AnneSD...').send_keys('my_username')
        self.get_by_placeholder(
            form, 'Exemplo: annesd@mail.com...').send_keys('email@valid.com')
        self.get_by_placeholder(
            form, 'Digite sua senha...').send_keys('P@ssw0rd1')
        self.get_by_placeholder(
            form,
            'Redigite sua senha para confirmação...').send_keys('P@ssw0rd1')

        form.submit()

        self.assertIn(
            'Sua conta foi foi criada! Agora pode logar nessa plataforma.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

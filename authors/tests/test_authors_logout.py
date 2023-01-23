from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(
            username='testuser',
            password='password'
        )
        self.client.login(
            username='testuser',
            password='password'
        )

        response = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn(
            ('Ops! A solicitação de deslogar é inválida. '
             'Tente novamente ou entre em contato com suporte.'),
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(
            username='testuser',
            password='password',
        )

        self.client.login(
            username='testuser',
            password='password'
        )

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'another_user',
            },
            follow=True
        )

        self.assertIn(
            ('Ops! Usuário não foi deslogado corretamente.'),
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(
            username='testuser',
            password='password',
        )

        self.client.login(
            username='testuser',
            password='password'
        )

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'testuser',
            },
            follow=True
        )

        self.assertIn(
            ('Sua conta foi deslogada com sucesso!'),
            response.content.decode('utf-8'))

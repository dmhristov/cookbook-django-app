from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse


class UserLoginViewTestst(TestCase):
    VALID_USER_CREDENTIALS = {'email': 'testmail@test.bg',
                              'password': 'Varna2022', }

    def test_login_with_valid_credentials(self):
        get_user_model().objects.create_user(**self.VALID_USER_CREDENTIALS)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_login_with_invalid_credentials(self):
        credentials = {'email': 'testmail2@test.bg',
                       'password': 'Varna2022', }
        self.client.login(**credentials)
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_redirects_authenticated_users_to_dashboard(self):
        user = get_user_model().objects.create_user(**self.VALID_USER_CREDENTIALS)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(
            reverse('login'),
        )
        expected_url = reverse('dashboard', kwargs={'category': 'all'})
        self.assertRedirects(response, expected_url)


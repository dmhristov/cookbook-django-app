from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse


class UserLogoutViewTests(TestCase):
    VALID_USER_CREDENTIALS = {'email': 'testmail@test.bg',
                              'password': 'Varna2022', }

    def test_logout_correctly(self):
        get_user_model().objects.create_user(**self.VALID_USER_CREDENTIALS)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        self.client.logout()
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_successfull_logout_redirects_to_login(self):
        get_user_model().objects.create_user(**self.VALID_USER_CREDENTIALS)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.post(reverse('logout'))
        expected_url = reverse('login')
        self.assertRedirects(response, expected_url)

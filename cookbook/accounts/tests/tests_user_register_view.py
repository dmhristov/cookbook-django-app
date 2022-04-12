from django.contrib.auth import get_user, get_user_model
from django.test import TestCase
from django.urls import reverse

from cookbook.accounts.models import Profile, CbUser


class UserRegisterViewTests(TestCase):
    VALID_PROFILE_USER_DATA = {
        'email': 'dmhristov@test.bg',
        'password1': 'Varna2022',
        'password2': 'Varna2022',
        'first_name': 'Denislav',
        'last_name': 'Hristov',
    }

    def test_register__when_all_valid__expect_to_create(self):
        self.client.post(
            reverse('register'),
            data=self.VALID_PROFILE_USER_DATA,
        )

        profile = Profile.objects.first()
        user = CbUser.objects.first()
        self.assertIsNotNone(profile)
        self.assertEqual(self.VALID_PROFILE_USER_DATA['first_name'], profile.first_name)
        self.assertEqual(self.VALID_PROFILE_USER_DATA['last_name'], profile.last_name)
        self.assertEqual(self.VALID_PROFILE_USER_DATA['email'], user.email)

    def test_register__when_invalid_first_name__expect_profile_not_created(self):
        self.client.post(
            reverse('register'),
            data={'email': 'testmail@test.bg',
                  'password1': 'Varna2022',
                  'password2': 'Varna2022',
                  'first_name': 'qwe15%',
                  'last_name': 'Hristov',
                  }
        )

        profile = Profile.objects.first()
        user = CbUser.objects.first()
        self.assertIsNone(profile)
        self.assertIsNone(user)

    def test_register__when_invalid_last_name__expect_profile_not_created(self):
        self.client.post(
            reverse('register'),
            data={'email': 'testmail@test.bg',
                  'password1': 'Varna2022',
                  'password2': 'Varna2022',
                  'first_name': 'Denislav',
                  'last_name': 'Hris5tov',
                  }
        )

        profile = Profile.objects.first()
        user = CbUser.objects.first()
        self.assertIsNone(profile)
        self.assertIsNone(user)

    def test_register__when_all_valid__expect_to_redirect_to_dashboard(self):
        response = self.client.post(
            reverse('register'),
            data=self.VALID_PROFILE_USER_DATA,
        )

        expected_url = reverse('dashboard', kwargs={'category': 'all'})
        self.assertRedirects(response, expected_url)

    def test_register__when_logged_in_user__expect_redirect_to_dashboard(self):
        credentials = {
            'email': 'asdffghh@test.bg',
            'password': 'passwordtest12',
        }
        user = get_user_model().objects.create_user(**credentials)
        self.client.login(**credentials)
        response = self.client.get(
            reverse('register'),
        )
        expected_url = reverse('dashboard', kwargs={'category': 'all'})
        self.assertRedirects(response, expected_url)

    def test_register_with_correct_data__expect_to_login(self):
        response = self.client.post(
            reverse('register'),
            data=self.VALID_PROFILE_USER_DATA,
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

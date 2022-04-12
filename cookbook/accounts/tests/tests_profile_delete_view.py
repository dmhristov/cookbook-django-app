from django.contrib.auth import get_user_model
from django.urls import reverse

from cookbook.accounts.models import Profile

from django.test import TestCase

user_model = get_user_model()


class ProfileDeleteTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'dmhristov@test.bg',
        'password': 'Varna2022',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Denislav',
        'last_name': 'Hristov',
    }

    def __create_valid_user_profile(self):
        user = user_model.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return user, profile

    def test_delete_profile_renders_correct_template(self):
        user, profile = self.__create_valid_user_profile()
        self.client.get(reverse('delete profile', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed('accounts/profile-delete.html')

    def test_delete_profile_with_authenticated_authorized_user(self):
        _, profile = self.__create_valid_user_profile()
        self.client.post(reverse('delete profile', kwargs={'pk': profile.pk}))
        user = get_user_model().objects.first()
        self.assertIsNone(user)

    def test_delete_profile_with_unauthorized_user__expect_redirect_403(self):
        credentials_user2 = {
            'email': 'dmhristov@test2.bg',
            'password': 'Varna2022',
        }
        credentials_profile2 = {
            'first_name': 'Denislav',
            'last_name': 'Hristov',
        }
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        user2 = user_model.objects.create_user(**credentials_user2)
        profile2 = Profile.objects.create(**credentials_profile2, user=user2)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('delete profile', kwargs={'pk': profile2.pk}))
        expected_url = reverse('403')
        self.assertRedirects(response, expected_url)

    def test_delete_profile_redirects_unauthenticated_users_to_login(self):
        user, profile = self.__create_valid_user_profile()
        response = self.client.get(reverse('delete profile', kwargs={'pk': profile.pk}))
        expected_url = reverse('login') + '?next=/profile/delete/1/'
        self.assertRedirects(response, expected_url)
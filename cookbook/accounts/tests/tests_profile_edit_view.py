from django.contrib.auth import get_user_model
from django.urls import reverse

from cookbook.accounts.models import Profile

from django.test import TestCase

user_model = get_user_model()


class ProfileDetailsTests(TestCase):
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

    def test_correct_template_used(self):
        user, profile = self.__create_valid_user_profile()
        self.client.get(reverse('edit profile', kwargs={'pk': profile.pk}))
        self.assertTemplateUsed('accounts/edit-profile.html')

    def test_editing_with_correct_data_saves_profile(self):
        user, profile = self.__create_valid_user_profile()
        new_valid_data = {
            'first_name': 'Denislavvv',
            'last_name': 'Hristov',
        }
        response = self.client.post(reverse('edit profile', kwargs={'pk': profile.pk}), data=new_valid_data)
        edited_profile = Profile.objects.first()
        self.assertEqual('Denislavvv', edited_profile.first_name)

    def test_editing_with_invalid_data__expect_not_to_change_profile(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        new_invalid_data = {
            'first_name': 'Denislav5',
            'last_name': 'Hris tov',
        }
        response = self.client.post(reverse('edit profile', kwargs={'pk': profile.pk}), data=new_invalid_data)
        edited_profile = Profile.objects.first()
        self.assertNotEqual(edited_profile.first_name, new_invalid_data['first_name'])
        self.assertNotEqual(edited_profile.last_name, new_invalid_data['last_name'])

    def test_editing_profile_with_correct_data_redirects_to_details(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        new_valid_data = {
            'first_name': 'Denislavvv',
            'last_name': 'Hristov',
        }
        response = self.client.post(reverse('edit profile', kwargs={'pk': profile.pk}), data=new_valid_data)
        expected_url = reverse('profile details', kwargs={'pk': profile.pk})
        self.assertRedirects(response, expected_url)

    def test_edit_profile_redirects_unauthenticated_users_to_login(self):
        user, profile = self.__create_valid_user_profile()
        response = self.client.get(reverse('edit profile', kwargs={'pk': profile.pk}))
        expected_url = f'/profile/login/?next=/profile/edit/{profile.pk}/'
        self.assertRedirects(response, expected_url)

    def test_edit_profile_with_unauthorized_user__expect_redirect_403(self):
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
        response = self.client.get(reverse('edit profile', kwargs={'pk': profile2.pk}))
        expected_url = reverse('403')
        self.assertRedirects(response, expected_url)
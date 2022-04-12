from django.contrib.auth import get_user_model
from django.urls import reverse

from cookbook.accounts.models import Profile

from django.test import TestCase

user_model = get_user_model()


class HomeViewTests(TestCase):
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

    def test_correct_template_used__when_user_is_unauthenticated(self):
        self.client.get(reverse('home'))
        self.assertTemplateUsed('main/home-no-profile.html')

    def test__when_user_is_authenticated__expect_redirect_to_dashboard(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('home'))
        expected_url = reverse('dashboard', kwargs={'category': 'all'})
        self.assertRedirects(response, expected_url)

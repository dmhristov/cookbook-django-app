from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cookbook.accounts.models import Profile
from cookbook.main.models import Recipe

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

    VALID_RECIPE_DATA = {
        'title': 'Test Recipe',
        'ingredients': 'Test Ingredients',
        'description': 'Test Description',
        'image': 'test.jpg',
        'category': 'Dinner',
    }

    def __create_valid_user_profile(self):
        user = user_model.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return user, profile

    def __create_user(self, **credentials):
        return user_model.objects.create_user(**credentials)

    def test_expect_correct_template(self):
        user, profile = self.__create_valid_user_profile()

        self.assertTemplateUsed('accounts/profile-details.html')

    def test_context_is_owner__when_user_is_owner__expect_true(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertEqual(True, response.context['is_owner'])

    def test_context_is_owner__when_user_is_not_owner__expect_false(self):
        user, profile = self.__create_valid_user_profile()
        credentials = {
            'email': 'asdffghh@test.bg',
            'password': 'passwordtest12',
        }

        self.__create_user(**credentials)
        self.client.login(**credentials)

        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertFalse(response.context['is_owner'])

    def test_recipes__when_user_has_recipes__expect_context_showing_recipes(self):
        user, profile = self.__create_valid_user_profile()
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('profile details', kwargs={'pk': profile.pk}))
        self.assertIsNotNone(response.context['recipes'])

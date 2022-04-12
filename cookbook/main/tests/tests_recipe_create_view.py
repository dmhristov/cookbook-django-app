from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from cookbook.accounts.models import Profile, CbUser

from django.test import TestCase

from cookbook.main.models import Recipe

user_model = get_user_model()


class RecipeCreateTests(TestCase):
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
        'ingredients': 'Test ingredients',
        'description': 'Test description',
        'category': 'Dinner',
        'image': 'test.jpg',
    }

    def __create_valid_user_profile(self):
        user = user_model.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return user, profile

    def test_correct_template_used(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response = self.client.get(reverse('create recipe'))

        self.assertTemplateUsed('main/create-recipe.html')

    # def test_create_recipe__when_valid_data(self):
    #     user, profile = self.__create_valid_user_profile()
    #     self.client.login(**self.VALID_USER_CREDENTIALS)
    #
    #     response = self.client.post(reverse('create recipe'), data=self.VALID_RECIPE_DATA, )
    #     recipe = Recipe.objects.all()
    #
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(1, len(recipe))

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from cookbook.accounts.models import Profile

from django.test import TestCase

from cookbook.main.models import Recipe

user_model = get_user_model()


class RecipeDeleteTests(TestCase):
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
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        response = self.client.get(reverse('delete recipe', kwargs={'pk': recipe.pk}))

        self.assertTemplateUsed('main/delete-recipe.html')

    def test_delete_recipe__when_success__expect_recipe_deleted(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        response = self.client.post(reverse('delete recipe', kwargs={'pk': recipe.pk}))
        recipes = Recipe.objects.all()

        self.assertEqual(0, len(recipes))
        
    def test_delete_recipe__when_success__expect_redirect_to_dashboard_all(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        response = self.client.post(reverse('delete recipe', kwargs={'pk': recipe.pk}))
        expected_url = reverse('dashboard', kwargs={'category': 'all'})
        
        self.assertRedirects(response, expected_url)

    def test_delete_recipe__when_unauthenticated_user__expect_redirect_to_login(self):
        user, profile = self.__create_valid_user_profile()
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        response = self.client.get(reverse('delete recipe', kwargs={'pk': recipe.pk}))
        expected_url = reverse('login') + f'?next=/recipes/delete/{recipe.pk}/'

        self.assertRedirects(response, expected_url)

    def test_delete_recipe__when_unauthorized_user__expect_redirect_to_403_page(self):
        user, profile = self.__create_valid_user_profile()

        user2 = user_model.objects.create_user(email='dmhristov2@test.bg', password='Varna2022')
        profile2 = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user2)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user2)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('delete recipe', kwargs={'pk': recipe.pk}))
        expected_url = reverse('403')
        self.assertRedirects(response, expected_url)


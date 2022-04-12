from django.contrib.auth import get_user_model
from django.urls import reverse

from cookbook.accounts.models import Profile

from django.test import TestCase

from cookbook.main.models import Recipe

user_model = get_user_model()


class DashboardTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'dmhristov@test.bg',
        'password': 'Varna2022',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Denislav',
        'last_name': 'Hristov',
    }

    VALID_BREAKFAST_RECIPE_DATA = {
        'title': 'Test Recipe',
        'ingredients': 'Test ingredients',
        'description': 'Test description',
        'image': 'test.jpg',
        'category': 'Breakfast',
    }

    VALID_DINNER_RECIPE_DATA = {
        'title': 'Test Recipe',
        'ingredients': 'Test ingredients',
        'description': 'Test description',
        'image': 'test.jpg',
        'category': 'Dinner',
    }

    VALID_DESSERT_RECIPE_DATA = {
        'title': 'Test Recipe',
        'ingredients': 'Test ingredients',
        'description': 'Test description',
        'image': 'test.jpg',
        'category': 'Dessert',
    }

    def __create_valid_user_profile(self):
        user = user_model.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user)
        return user, profile

    def test_correct_template_for_different_categories(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response_all = self.client.get(reverse('dashboard', kwargs={'category': 'all'}))
        response_breakfast = self.client.get(reverse('dashboard', kwargs={'category': 'Breakfast'}))
        response_dinner = self.client.get(reverse('dashboard', kwargs={'category': 'Dinner'}))
        response_dessert = self.client.get(reverse('dashboard', kwargs={'category': 'Dessert'}))

        self.assertTemplateUsed(response_all, 'main/dashboard.html')
        self.assertTemplateUsed(response_breakfast, 'main/dashboard.html')
        self.assertTemplateUsed(response_dinner, 'main/dashboard.html')
        self.assertTemplateUsed(response_dessert, 'main/dashboard.html')

    def test__when_no_recipes__expect_no_recipes_returned(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        response_all = self.client.get(reverse('dashboard', kwargs={'category': 'all'}))
        response_breakfast = self.client.get(reverse('dashboard', kwargs={'category': 'Breakfast'}))
        response_dinner = self.client.get(reverse('dashboard', kwargs={'category': 'Dinner'}))
        response_dessert = self.client.get(reverse('dashboard', kwargs={'category': 'Dessert'}))

        self.assertEqual(0, len(response_all.context['recipes']))
        self.assertEqual(0, len(response_breakfast.context['recipes']))
        self.assertEqual(0, len(response_dinner.context['recipes']))
        self.assertEqual(0, len(response_dessert.context['recipes']))

    def test_recipe_count__when_category_all__expect_all_recipes_returned(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        recipe_breakfast = Recipe.objects.create(**self.VALID_BREAKFAST_RECIPE_DATA,
                                                 author=user)

        recipe_dinner = Recipe.objects.create(**self.VALID_DINNER_RECIPE_DATA,
                                              author=user)

        recipe_dessert = Recipe.objects.create(**self.VALID_DESSERT_RECIPE_DATA,
                                               author=user)
        response_all = self.client.get(reverse('dashboard', kwargs={'category': 'all'}))

        self.assertEqual(3, len(response_all.context['recipes']))

    def test_recipes__when_category_breakfast__expect_correct_category_recipes_returned(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        recipe_breakfast = Recipe.objects.create(**self.VALID_BREAKFAST_RECIPE_DATA,
                                                 author=user)

        recipe_dinner = Recipe.objects.create(**self.VALID_DINNER_RECIPE_DATA,
                                              author=user)

        recipe_dessert = Recipe.objects.create(**self.VALID_DESSERT_RECIPE_DATA,
                                               author=user)
        response_breakfast = self.client.get(reverse('dashboard', kwargs={'category': 'Breakfast'}))

        self.assertEqual(1, len(response_breakfast.context['recipes']))
        self.assertEqual(recipe_breakfast.category, response_breakfast.context['recipes'][0].category)

    def test_recipes__when_category_dinner__expect_correct_category_recipes_returned(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        recipe_breakfast = Recipe.objects.create(**self.VALID_BREAKFAST_RECIPE_DATA,
                                                 author=user)

        recipe_dinner = Recipe.objects.create(**self.VALID_DINNER_RECIPE_DATA,
                                              author=user)

        recipe_dessert = Recipe.objects.create(**self.VALID_DESSERT_RECIPE_DATA,
                                               author=user)
        response_dinner = self.client.get(reverse('dashboard', kwargs={'category': 'Dinner'}))

        self.assertEqual(1, len(response_dinner.context['recipes']))
        self.assertEqual(recipe_dinner.category, response_dinner.context['recipes'][0].category)

    def test_recipes__when_category_dessert__expect_correct_category_recipes_returned(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        recipe_breakfast = Recipe.objects.create(**self.VALID_BREAKFAST_RECIPE_DATA,
                                                 author=user)

        recipe_dinner = Recipe.objects.create(**self.VALID_DINNER_RECIPE_DATA,
                                              author=user)

        recipe_dessert = Recipe.objects.create(**self.VALID_DESSERT_RECIPE_DATA,
                                               author=user)
        response_dessert = self.client.get(reverse('dashboard', kwargs={'category': 'Dessert'}))

        self.assertEqual(1, len(response_dessert.context['recipes']))
        self.assertEqual(recipe_dessert.category, response_dessert.context['recipes'][0].category)

from django.contrib.auth import get_user_model
from django.urls import reverse

from cookbook.accounts.models import Profile

from django.test import TestCase

from cookbook.main.models import Recipe, Comment

user_model = get_user_model()


class CreateCommentTests(TestCase):
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

    def test_create_comment__expect_successfully_created_comment(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)

        response = self.client.post(reverse('comments', kwargs={'pk': recipe.pk}), data={'text': 'test'})
        comment = Comment.objects.all()

        self.assertEqual(1, len(comment))
        self.assertEqual('test', comment[0].text)
        self.assertEqual(recipe, comment[0].recipe)
        self.assertEqual(user, comment[0].author)

    def test_create_comment__when_success__expect_redirect_to_recipe_details(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)

        response = self.client.post(reverse('comments', kwargs={'pk': recipe.pk}), data={'text': 'test'})
        expected_url = reverse('recipe details', kwargs={'pk': recipe.pk})

        self.assertRedirects(response, expected_url)

    def test_create_comment__when_unauthenticated_user__expect_redirect_to_login(self):
        user, profile = self.__create_valid_user_profile()
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)

        response = self.client.post(reverse('comments', kwargs={'pk': recipe.pk}), data={'text': 'test'})
        expected_url = reverse('login') + f'?next=/recipes/details/{recipe.pk}/comments'

        self.assertRedirects(response, expected_url)

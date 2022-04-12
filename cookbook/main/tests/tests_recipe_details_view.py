from django.contrib.auth import get_user_model
from django.urls import reverse

from cookbook.accounts.models import Profile

from django.test import TestCase

from cookbook.main.forms import CreateCommentForm, CreateCommentReplyForm
from cookbook.main.models import Recipe, Comment

user_model = get_user_model()


class RecipeDetailsTests(TestCase):
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
        response = self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))

        self.assertTemplateUsed('main/recipe-details.html')

    def test_recipe_details_context_profile__expect_correct_profile(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        response = self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))

        self.assertEqual(profile, response.context['profile'])

    def test_recipe_details_context_is_owner__when_user_is_owner__expect_to_return_true(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        response = self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))

        self.assertTrue(response.context['is_owner'])

    def test_recipe_details_context_is_owner__when_user_is_not_owner__expect_to_return_false(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        user2 = user_model.objects.create_user(email='dmhristov2@test.bg', password='Varna2022')
        profile2 = Profile.objects.create(**self.VALID_PROFILE_DATA, user=user2)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user2)
        response = self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))

        self.assertFalse(response.context['is_owner'])

    def test_recipe_details_context_comment_form__expext_to_return_correct_form(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        response = self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))
        expected_form = CreateCommentForm

        self.assertEqual(expected_form, response.context['comment_form'])

    def test_recipe_details_context_comment_form__expext_to_return_correct_form(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        response = self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))
        expected_form = CreateCommentReplyForm

        self.assertEqual(expected_form, response.context['reply_form'])

    def test_recipe_details_context_comments__when_there_are_comments__expect_to_return_all_recipe_comments(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        comment = Comment.objects.create(text='test', author=user, recipe=recipe)
        response = self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))

        self.assertEqual(1, len(response.context['comments']))
        self.assertEqual(comment.text, response.context['comments'][0].text)

    def test_recipe_details_context_comments__when_there_are_no_comments__expect_to_return_all_recipe_comments(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        response = self.client.get(reverse('recipe details', kwargs={'pk': recipe.pk}))

        self.assertEqual(0, len(response.context['comments']))

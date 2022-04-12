from django.contrib.auth import get_user_model
from django.urls import reverse

from cookbook.accounts.models import Profile

from django.test import TestCase

from cookbook.main.models import Recipe, Comment, Reply

user_model = get_user_model()


class CreateReplyTests(TestCase):
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

    def test_create_reply__when_success__expect_reply_created(self):
        user, profile = self.__create_valid_user_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        comment = Comment.objects.create(text='test', author=user, recipe=recipe)
        response = self.client.post(reverse('replies', kwargs={'pk': recipe.pk, 'comment_pk': comment.pk}),
                                    data={'text': 'test'})
        replies = Reply.objects.all()

        self.assertEqual(1, len(replies))
        self.assertEqual('test', replies[0].text)
        self.assertEqual(user, replies[0].author)
        self.assertEqual(comment, replies[0].comment)

    def test_create_reply__when_unauthenticated_user__expect_redirect_to_login(self):
        user, profile = self.__create_valid_user_profile()
        recipe = Recipe.objects.create(**self.VALID_RECIPE_DATA, author=user)
        comment = Comment.objects.create(text='test', author=user, recipe=recipe)
        response = self.client.post(reverse('replies', kwargs={'pk': recipe.pk, 'comment_pk': comment.pk}),
                                    data={'text': 'test'})
        expected_url = reverse('login') + f'?next=/recipes/details/{recipe.pk}/comments/{comment.pk}/replies/'

        self.assertRedirects(response, expected_url)

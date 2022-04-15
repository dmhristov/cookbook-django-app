from django.db import models

from cookbook.accounts.models import CbUser


class Recipe(models.Model):
    TITLE_MAX_LENGTH = 50
    BREAKFAST = 'Breakfast'
    DINNER = 'Dinner'
    DESERT = 'Dessert'
    UPLOAD_TO_URL = 'recipes/'
    CATEGORY_CHOICES = [(c, c) for c in (BREAKFAST, DINNER, DESERT)]
    CATEGORY_MAX_LENGTH = max([len(x) for x, _ in CATEGORY_CHOICES])

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH
    )

    ingredients = models.TextField()

    description = models.TextField()

    image = models.ImageField(
        upload_to=UPLOAD_TO_URL,
    )

    created_on = models.DateField(
        auto_now_add=True,
    )

    author = models.ForeignKey(
        CbUser,
        on_delete=models.CASCADE,
    )

    total_likes = models.IntegerField(
        default=0,
    )

    category = models.CharField(
        max_length=CATEGORY_MAX_LENGTH,
        choices=CATEGORY_CHOICES,
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    author = models.ForeignKey(
        CbUser,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.text[:40]}...'

    class Meta:
        ordering = ['-created_on']


class Reply(models.Model):
    author = models.ForeignKey(
        CbUser,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.text[:40]}...'

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = 'Replies'


class Like(models.Model):
    user = models.ForeignKey(
        CbUser,
        on_delete=models.CASCADE,
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

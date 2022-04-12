from django.test import TestCase
from django.urls import reverse


class UnauthorizedViewTests(TestCase):
    def test_unauthorized_view_renders_correct_template(self):
        self.client.get(reverse('403'))
        self.assertTemplateUsed('base/403.html')

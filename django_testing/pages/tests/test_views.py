from django.test import SimpleTestCase
from django.urls import resolve, reverse

from pages.views import HomePageView


class HomePageViewTests(SimpleTestCase):
    def setUp(self):
        self.url = reverse("pages:home")
        self.response = self.client.get(self.url)

    def test_homepage_view_url(self):
        view = resolve(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(view.func.view_class, HomePageView)

    def test_homepage_view_template(self):
        self.assertTemplateUsed(self.response, "pages/home.html")
        self.assertContains(self.response, "Home")
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

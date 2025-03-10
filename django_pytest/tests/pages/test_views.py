from django.urls import resolve, reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from pages.views import HomePageView


def test_homepage_view(home_response):
    url = reverse("pages:home")
    view = resolve(url)

    assert home_response.status_code == 200
    assert view.func.view_class == HomePageView

    assertContains(home_response, "Home")
    assertNotContains(home_response, "Hi there! I should not be on this page.")
    assertTemplateUsed(home_response, "pages/home.html")

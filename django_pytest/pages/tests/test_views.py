from django.urls import resolve
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from pages.views import HomePageView


def test_homepage_view_url(home_url, home_response):
    view = resolve(home_url)
    assert home_response.status_code == 200
    assert view.func.view_class == HomePageView


def test_homepage_view_template(home_response):
    assertContains(home_response, "Home")
    assertNotContains(home_response, "Hi there! I should not be on this page.")
    assertTemplateUsed(home_response, "pages/home.html")

import pytest
from django.urls import reverse


@pytest.fixture
def home_url():
    return reverse("pages:home")


@pytest.fixture
def home_response(client, home_url):
    return client.get(home_url)

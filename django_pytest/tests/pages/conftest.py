import pytest
from django.urls import reverse


@pytest.fixture
def home_response(client):
    url = reverse("pages:home")
    return client.get(url)

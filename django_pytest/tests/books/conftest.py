import pytest
from django.urls import reverse

from books.models import Book


@pytest.fixture
def book(db):
    return Book.objects.create(
        title="Django 5 for Beginners",
        author="William S. Vincent",
        description="Learn Django fundamentals while building, testing, and deploying six complete web applications from scratch.",
        slug="django-5-for-beginners-1",
    )


@pytest.fixture
def book_list_response(client):
    url = reverse("books:book_list")
    return client.get(url)


@pytest.fixture
def book_detail_response(book, client):
    url = reverse("books:book_detail", kwargs={"slug": book.slug})
    return client.get(url)

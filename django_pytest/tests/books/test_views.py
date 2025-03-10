import pytest
from django.urls import resolve, reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from books.views import BookDetailView, BookListView


@pytest.mark.django_db
def test_book_list_view(book_list_response):
    url = reverse("books:book_list")
    view = resolve(url)
    response = book_list_response

    assert response.status_code == 200
    assert view.func.view_class == BookListView

    assertContains(response, "Books")
    assertNotContains(response, "Hi there! I should not be on this page.")
    assertTemplateUsed(response, "books/list.html")


@pytest.mark.django_db
def test_book_list_view_context(book, book_list_response):
    assert "books" in book_list_response.context
    assert len(book_list_response.context["books"]) == 1


@pytest.mark.django_db
def test_book_detail_view(book, book_detail_response):
    url = reverse("books:book_detail", kwargs={"slug": book.slug})
    view = resolve(url)
    response = book_detail_response

    assert response.status_code == 200
    assert view.func.view_class == BookDetailView

    assertContains(response, book.title)
    assertNotContains(response, "Hi there! I should not be on this page.")
    assertTemplateUsed(response, "books/detail.html")


@pytest.mark.django_db
def test_book_detail_view_context(book, book_detail_response):
    assert "book" in book_detail_response.context
    assert book_detail_response.context["book"] == book

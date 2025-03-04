import pytest
from django.urls import resolve
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from books.views import BookDetailView, BookListView


@pytest.mark.django_db
def test_book_list_view_url(book_list_url, book_list_response):
    view = resolve(book_list_url)
    assert book_list_response.status_code == 200
    assert view.func.view_class == BookListView


@pytest.mark.django_db
def test_book_list_view_template(book_list_response):
    assertContains(book_list_response, "Books")
    assertTemplateUsed(book_list_response, "books/list.html")


@pytest.mark.django_db
def test_book_list_view_context(book, book_list_response):
    assert "books" in book_list_response.context
    assert len(book_list_response.context["books"]) == 1


@pytest.mark.django_db
def test_book_detail_view_url(book_detail_url, book_detail_response):
    view = resolve(book_detail_url)
    assert book_detail_response.status_code == 200
    assert view.func.view_class == BookDetailView


@pytest.mark.django_db
def test_book_detail_view_template(book, book_detail_response):
    assertContains(book_detail_response, book.title)
    assertNotContains(book_detail_response, "Hi there! I should not be on this page.")
    assertTemplateUsed(book_detail_response, "books/detail.html")


@pytest.mark.django_db
def test_book_detail_view_context(book, book_detail_response):
    assert "book" in book_detail_response.context
    assert book_detail_response.context["book"] == book

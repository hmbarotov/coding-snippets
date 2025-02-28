from django.test import TestCase
from django.urls import resolve, reverse

from books.models import Book
from books.views import BookDetailView, BookListView


class BookListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title="Django 5 for Beginners",
            author="William S. Vincent",
            description="Learn Django fundamentals while building, testing, and deploying six complete web applications from scratch.",
        )
        cls.url = reverse("books:book_list")

    def setUp(self):
        self.response = self.client.get(self.url)

    def test_book_list_view_url(self):
        view = resolve(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(view.func.view_class, BookListView)

    def test_book_list_view_template(self):
        self.assertTemplateUsed(self.response, "books/list.html")
        self.assertContains(self.response, "Books")
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_book_list_view_context(self):
        self.assertIn(self.book, self.response.context["books"])
        self.assertEqual(len(self.response.context["books"]), 1)


class BookDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title="Django 5 for Beginners",
            author="William S. Vincent",
            description="Learn Django fundamentals while building, testing, and deploying six complete web applications from scratch.",
        )
        cls.url = reverse("books:book_detail", kwargs={"slug": cls.book.slug})

    def setUp(self):
        self.response = self.client.get(self.url)

    def test_book_detail_view_url(self):
        view = resolve(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(view.func.view_class, BookDetailView)

    def test_book_detail_view_template(self):
        self.assertTemplateUsed(self.response, "books/detail.html")
        self.assertContains(self.response, self.book.title)
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_book_detail_view_context(self):
        self.assertEqual(self.book, self.response.context["book"])

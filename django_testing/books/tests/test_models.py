from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BookModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.book = Book.objects.create(
            title="Django 5 for Beginners",
            author="William S. Vincent",
            description="Learn Django fundamentals while building, testing, and deploying six complete web applications from scratch.",
            slug="django-5-for-beginners-1",
        )

    def test_book_content(self):
        self.assertEqual(self.book.title, "Django 5 for Beginners")
        self.assertEqual(self.book.author, "William S. Vincent")
        self.assertEqual(
            self.book.description,
            "Learn Django fundamentals while building, testing, and deploying six complete web applications from scratch.",
        )

    def test_book_slug(self):
        self.assertEqual(self.book.slug, "django-5-for-beginners")
        self.assertNotEqual(self.book.slug, "django-5-for-beginners-1")

    def test_book_methods(self):
        self.assertEqual(str(self.book), "Django 5 for Beginners")
        self.assertEqual(
            self.book.get_absolute_url(),
            reverse("books:book_detail", kwargs={"slug": self.book.slug}),
        )

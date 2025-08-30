from django.urls import reverse


def test_book_content(book):
    assert book.title == "Django 5 for Beginners"
    assert book.author == "William S. Vincent"
    assert (
        book.description
        == "Learn Django from scratch"
    )


def test_book_slug(book):
    assert book.slug == "django-5-for-beginners"
    assert book.slug != "django-5-for-beginners-1"


def test_book_methods(book):
    assert str(book) == "Django 5 for Beginners"
    assert book.get_absolute_url() == reverse(
        "books:book_detail", kwargs={"slug": book.slug}
    )

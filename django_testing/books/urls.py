from django.urls import path

from .views import BookDetailView, BookListView

app_name = "books"
urlpatterns = [
    path("<slug:slug>/", BookDetailView.as_view(), name="book-detail"),
    path("", BookListView.as_view(), name="book-list"),
]

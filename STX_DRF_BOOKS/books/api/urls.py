from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.list_books),
    path("books/<str:book_id>", views.retrieve_book),
    path("db/", views.update_books),
]

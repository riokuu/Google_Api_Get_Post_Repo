from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework import status
from rest_framework.parsers import JSONParser
from .serializers import *
from .models import *
import requests


@api_view(["GET"])
def list_books(request):
    queryset = Book.objects.all()

    if request.GET.get("author") is not None:
        queryset = queryset.filter(authors__fullname=request.GET["author"])
    if request.GET.get("published_date") is not None:
        queryset = queryset.filter(published_date=request.GET["published_date"])
    if request.GET.get("sort") is not None:
        queryset = queryset.order_by(request.GET["sort"])

    serializer = BookSerialiser(queryset, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def retrieve_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        serializer = BookSerialiser(book)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@parser_classes([JSONParser])
def update_books(request):
    q = request.data.get("q", "")
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={q}")
    response.raise_for_status()

    # tutaj przydałoby się przeiterować po wszystkich stronach
    payload = response.json()
    save_book_batch(payload)

    return Response(status=status.HTTP_204_NO_CONTENT)


def save_book_batch(payload):
    # dałoby sie to zoptymalizować pod kątem liczby zapytań

    for book in payload["items"]:
        authors = []
        categories = []

        for author_name in book["volumeInfo"].get("authors", []):
            author, _ = Author.objects.get_or_create(fullname=author_name)
            authors.append(author)

        for category_name in book["volumeInfo"].get("categories", []):
            category, _ = Categories.objects.get_or_create(name=category_name)
            categories.append(category)

        instance, _ = Book.objects.get_or_create(id=book["id"])
        instance.title = book["volumeInfo"]["title"]
        instance.published_date = book["volumeInfo"]["publishedDate"]
        instance.average_rating = book.get("averageRating")
        instance.ratings_count = book.get("ratingsCount")
        instance.thumbnail = book.get("imageLinks", {}).get("thumbnail")
        instance.authors.set(authors)
        instance.categories.set(categories)
        instance.save()

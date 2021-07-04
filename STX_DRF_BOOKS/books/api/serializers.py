from rest_framework import serializers
from .models import *


class BookSerialiser(serializers.ModelSerializer):

    authors = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    def get_authors(self, instance):
        return [author.fullname for author in instance.authors.all()]

    def get_categories(self, instance):
        return [category.name for category in instance.categories.all()]

    class Meta:
        model = Book
        fields = [
            "title",
            "authors",
            "published_date",
            "categories",
            "average_rating",
            "ratings_count",
            "thumbnail",
        ]
        depth = 1

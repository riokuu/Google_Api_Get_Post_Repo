from django.db import models


class Author(models.Model):
    fullname = models.CharField(max_length=50)

    def __str__(self):
        return f"Author: {self.fullname}"


class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Category: {self.name}"


class Book(models.Model):

    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    authors = models.ManyToManyField(Author)
    published_date = models.CharField(max_length=30, blank=True)
    categories = models.ManyToManyField(Categories, blank=True)
    average_rating = models.IntegerField(null=True, blank=True)
    ratings_count = models.IntegerField(null=True, blank=True)
    thumbnail = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Book: {self.title}"

from django.db import models
from .constants import COMEDY, MOVIE_GENRES, ACTION


class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=3000, blank=True)
    cover_image_url = models.CharField(max_length=300)
    genre = models.CharField(max_length=2, choices=MOVIE_GENRES, default=COMEDY)
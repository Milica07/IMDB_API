from django.db import models
from .constants import COMEDY, MOVIE_GENRES
from django.contrib.auth import get_user_model

User = get_user_model()

class Movie(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=3000, blank=True)
    cover_image_url = models.CharField(max_length=300)
    genre = models.CharField(max_length=2, choices=MOVIE_GENRES, default=COMEDY)
    number_of_views = models.PositiveIntegerField(blank=False, null=False, default=0)
    likes = models.ManyToManyField(User, related_name='movies_liked')
    dislikes = models.ManyToManyField(User, related_name='movies_disliked')


    @classmethod
    def like_movie(cls, user, pk):
        movie = cls.objects.get(id=pk)
        if movie.likes.filter(id=user.id).exists():
            movie.likes.remove(user)
        else:
            if movie.dislikes.filter(id=user.id).exists():
                movie.dislikes.remove(user)
            movie.likes.add(user)
        return movie

    @classmethod
    def dislike_movie(cls, user, pk):
        movie = cls.objects.get(id=pk)
        if movie.dislikes.filter(id=user.id).exists():
            movie.dislikes.remove(user)
        else:
            if movie.likes.filter(id=user.id).exists():
                movie.likes.remove(user)
            movie.dislikes.add(user)
        return movie


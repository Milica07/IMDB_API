from django.db import models
from .constants import COMEDY, MOVIE_GENRES
from django.contrib.auth import get_user_model
import json

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
    def get_queryset(cls, request):
        queryset = cls.objects.all()
        title = request.query_params.get('title')
        genre = request.query_params.get('genre')
        description = request.query_params.get('description')
        cover_image_url = request.query_params.get('cover_image_url')
        if title is not None:
            queryset = queryset.filter(
                title__icontains=title, 
                genre__icontains=genre,
                description__icontains=description,
                cover_image_url__icontains=cover_image_url,)
        return queryset

    @classmethod
    def popular(cls):
        return cls.objects.all().annotate(likes_sum=models.Count('likes')).order_by('-likes_sum')[:10]

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

    @classmethod
    def watch_list(cls, request):
        user = request.user
        print(user)
        result = cls.objects.filter(watch_list_items__user=user)
        print(result)
        return result


class Comment(models.Model):
    content = models.CharField(max_length=500, blank=False)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)

    @classmethod
    def get_queryset(cls, movie_id):
        queryset = cls.objects.all()
        if movie_id is not None:
            queryset = queryset.filter(
                movie__id=movie_id)
        return queryset

    @classmethod
    def add_comment(cls, request, pk):
        user = request.user
        movie = Movie.objects.get(id=pk)
        content = json.loads(request.body)['content']
        return cls.objects.create(user=user, movie=movie, content=content)


class WatchListItem(models.Model):
    watched = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, related_name='watch_list_items', on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, related_name='watch_list_items', on_delete=models.CASCADE)

    @classmethod
    def add_remove(cls, user, movie_id):
        movie = Movie.objects.get(id=movie_id)
        item = cls.objects.filter(user=user, movie=movie)
        if item.exists():
            item.delete()
        else:
            cls.objects.create(user=user, movie=movie)
        return movie

    @classmethod
    def set_watched(cls, user, movie_id):
        movie = Movie.objects.get(id=movie_id)
        item = cls.objects.get(user=user, movie=movie)
        item.watched = not item.watched
        item.save()
        return movie

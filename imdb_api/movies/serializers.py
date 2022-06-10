from rest_framework import serializers
from .models import Movie, Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(source='user', read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'username']

class MovieSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()
    disliked_by_user = serializers.SerializerMethodField()
    watched_by_user = serializers.SerializerMethodField()
    in_users_watchlist = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'cover_image_url', 'genre', 
        'number_of_views',
        'likes', 'dislikes', 'liked_by_user', 'disliked_by_user', 
        'watched_by_user', 'in_users_watchlist']
    
    def get_likes(self, obj):
        return obj.likes.count()

    def get_dislikes(self, obj):
        return obj.dislikes.count()

    def get_liked_by_user(self, obj):
        user = self.context.get('request').user
        return True if obj.likes.filter(id=user.id).exists() else False

    def get_disliked_by_user(self, obj):
        user = self.context.get('request').user
        return True if obj.dislikes.filter(id=user.id).exists() else False

    def get_watched_by_user(self, obj):
        user = self.context.get('request').user
        return True if obj.watch_list_items.filter(user__id=user.id, watched=True).exists() else False

    def get_in_users_watchlist(self, obj):
        user = self.context.get('request').user
        return True if obj.watch_list_items.filter(user__id=user.id).exists() else False

class BasicMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'cover_image_url', 'genre']

class RetrieveMovieSerializer(BaseException):
    def retrieve(self, instance):
        instance.number_of_views += 1
        instance.save()
        return instance

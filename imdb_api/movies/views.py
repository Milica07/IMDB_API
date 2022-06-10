from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from .models import Movie
from .serializers import MovieSerializer, RetrieveMovieSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from .models import Movie, Comment, WatchListItem
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView

class CommentListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(movie_id = self.kwargs.get('pk'))
    
class MovieViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    queryset = Movie.objects.all()

    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title'] 
    filterset_fields = ['genre'] 
    
    def retrieve(self, request, pk):
        instance = self.get_object()
        retrieve_serializer = RetrieveMovieSerializer()
        movie = retrieve_serializer.retrieve(instance)
        serializer = MovieSerializer(
            movie,
            context={"request": self.request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return Movie.objects.all()
    
    def create(self, request):
        return Response(MovieSerializer(Movie.create(request), context={'request': request}).data)

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated, ])
def popular_movies(request):
    return Response(MovieSerializer(Movie.popular(), context={'request': request}, many=True).data)

@api_view(http_method_names=['PATCH'])
@permission_classes([IsAuthenticated, ])
def like_movie(request, pk):
    return Response(MovieSerializer(Movie.like_movie(request.user, pk), context={'request': request}).data)

@api_view(http_method_names=['PATCH'])
@permission_classes([IsAuthenticated, ])
def dislike_movie(request, pk):
    return Response(MovieSerializer(Movie.dislike_movie(request.user, pk), context={'request': request}).data)

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, ])
def add_comment(request, pk):
    return Response(CommentSerializer(Comment.add_comment(request, pk), context={'request': request}).data)

@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated, ])
def watch_list(request):
    return Response(MovieSerializer(Movie.watch_list(request), context={'request': request}, many=True).data)

@api_view(http_method_names=['PATCH'])
@permission_classes([IsAuthenticated, ])
def watch_list_add_remove(request, movie_id):
    return Response(MovieSerializer(WatchListItem.add_remove(request.user, movie_id), context={'request': request}).data)

@api_view(http_method_names=['PATCH'])
@permission_classes([IsAuthenticated, ])
def watched(request, movie_id):
    return Response(MovieSerializer(WatchListItem.set_watched(request.user, movie_id), context={'request': request}).data)

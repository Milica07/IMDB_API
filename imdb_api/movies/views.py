from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Movie
from .serializers import MovieSerializer, RetrieveMovieSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from .models import Movie
from rest_framework.decorators import api_view, permission_classes

class MovieViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):

    queryset = Movie.objects.all()

    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
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


@api_view(http_method_names=['PATCH'])
@permission_classes([AllowAny])
def like_movie(request, pk):
    return Response(MovieSerializer(Movie.like_movie(request.user, pk), context={'request': request}).data)


@api_view(http_method_names=['PATCH'])
@permission_classes([AllowAny])
def dislike_movie(request, pk):
    return Response(MovieSerializer(Movie.dislike_movie(request.user, pk), context={'request': request}).data)



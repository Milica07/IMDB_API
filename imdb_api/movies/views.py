from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Movie
from .serializers import MovieSerializer
from django_filters.rest_framework import DjangoFilterBackend

class MovieViewSet(mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet,
                mixins.CreateModelMixin):

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title'] 
    filterset_fields = ['genre'] 

    

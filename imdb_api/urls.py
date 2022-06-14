from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from imdb_api.users.urls import user_router
from imdb_api.movies.urls import movie_router
from imdb_api.movies import views as movies_views

urlpatterns = [
     path('admin/', admin.site.urls),
     path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/movies/popular/', 
        movies_views.popular_movies),
     path('api/watch-list', movies_views.watch_list),
     path('api/watch-list/<int:movie_id>/add-remove',
         movies_views.watch_list_add_remove),     
     path('api/watch-list/<int:movie_id>/watched',
         movies_views.watched),
     path('api/', include(user_router.urls)),
     path('api/', include(movie_router.urls)),
     path('api/movies/<int:pk>/like',
         movies_views.like_movie),
     path('api/movies/<int:pk>/dislike',
         movies_views.dislike_movie),
     path('api/movies/<int:pk>/comment',
         movies_views.add_comment), 
     path('api/movies/<int:pk>/comments',
         movies_views.CommentListAPIView.as_view()),
]
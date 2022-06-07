from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView
from imdb_api.users.urls import user_router
from imdb_api.movies.urls import movie_router
from imdb_api.movies import views as movies_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/', include(user_router.urls)),
    path('api/', include(movie_router.urls)),
    path('api/movies/<int:pk>/like',
         movies_views.like_movie),
    path('api/movies/<int:pk>/dislike',
         movies_views.dislike_movie),
]
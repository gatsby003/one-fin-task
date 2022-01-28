from django.urls import path
from .views import collection_get_post, collection_get_delete, get_movies,register

urlpatterns = [
    path('collections/', collection_get_post),
    path('collections/<str:id>', collection_get_delete),
    path('movies/', get_movies),
    path('register/', register)
]
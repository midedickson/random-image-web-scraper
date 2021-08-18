from django.urls import path
from .views import send_random_photos
urlpatterns = [
    path('fetch-photos/', send_random_photos)
]

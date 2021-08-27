from django.urls import path
from .views import send_random_photos, get_all_ads
urlpatterns = [
    path('fetch-photos/', send_random_photos),
    path('get-all-ads/', get_all_ads)
]

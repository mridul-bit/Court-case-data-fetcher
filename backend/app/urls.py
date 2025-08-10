from django.urls import path
from .views import fetch_case

urlpatterns = [
    path('fetch-case/', fetch_case ),
]



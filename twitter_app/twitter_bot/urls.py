from django.urls import path
from . import views

urlpatterns = [
    path('nonfollowers/', views.unfollowers, name='nonfollowers'),
]
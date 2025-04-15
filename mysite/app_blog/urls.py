# app_blog/urls.py
from django.urls import path
from app_blog import views
urlpatterns = [
 path('', views.HomePageView.as_view()),
]
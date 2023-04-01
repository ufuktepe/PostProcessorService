from django.urls import include, path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.handle_request, name='handle_request')
]
from django.contrib import admin
from django.urls import path, include
from .views import *

app_name='pages'
urlpatterns = [
    path("", PostListView.as_view(), name="all"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post_detail"),
]

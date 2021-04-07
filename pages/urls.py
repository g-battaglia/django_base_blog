from django.contrib import admin
from django.urls import path, include, reverse_lazy
from .views import *

app_name='pages'
urlpatterns = [
    path("", PostListView.as_view(), name="all"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path('post/create', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
]

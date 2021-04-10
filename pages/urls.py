from django.contrib import admin
from django.urls import path, include, reverse_lazy
from .views import *

app_name='pages'
urlpatterns = [
    path("", PostListView.as_view(), name="all"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    # Tags:
    path('tag/<slug:tg_slug>/', TagList.as_view(), name='tag_list'),
    # Comments:
    path('post/<int:pk>/comment', CommentCreateView.as_view(), name='post_comment_create'),
    path('post/<int:pk>/delete_comment', CommentDeleteView.as_view(success_url=reverse_lazy('post:all')), name='post_comment_delete'),
    # Likes:
    path('post/<int:pk>/like', AddLikeView.as_view(), name='post_like'),
    path('post/<int:pk>/dislike', DeleteLikeView.as_view(), name='post_dislike'),
]

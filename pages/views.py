from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Post
from .owner import OwnerCreateView, OwnerDeleteView, OwnerUpdateView
# Create your views here.

class PostListView(ListView):
    def get_queryset(self):
        post_list = Post.objects.order_by('-updated_at')[:10]
        return post_list
    
class PostDetailView(DetailView):
    model = Post

class PostCreateView(OwnerCreateView):
    model = Post
    fields = ['title', 'body','image',]
    success_url = reverse_lazy('pages:all')

class PostDeleteView(OwnerDeleteView):
    model = Post
    success_url=reverse_lazy('pages:all')

class PostUpdateView(OwnerUpdateView):
    model = Post
    fields = ['title', 'body','image',]
    success_url = reverse_lazy('pages:all')
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .forms import CommentForm
from .models import Post, Comment
from .owner import OwnerCreateView, OwnerDeleteView, OwnerUpdateView
# Create your views here.

class PostListView(ListView):
    def get_queryset(self):
        post_list = Post.objects.order_by('-updated_at')[:10]
        return post_list
    
class PostDetailView(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        comments = Comment.objects.filter(post=self.object).order_by('-updated_at')
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context

class PostCreateView(OwnerCreateView):
    model = Post
    fields = ['title', 'body','image', 'tags',]
    success_url = reverse_lazy('pages:all')

class PostDeleteView(OwnerDeleteView):
    model = Post
    success_url=reverse_lazy('pages:all')

class PostUpdateView(OwnerUpdateView):
    model = Post
    fields = ['title', 'body','image', 'tags',]
    success_url = reverse_lazy('pages:all')
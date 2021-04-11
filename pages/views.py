# Django:
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.urls import reverse_lazy

# Forms:
from .forms import CommentForm
# Models:
from .models import Post, Comment, Like
# Views:
from django.views.generic import View, ListView, DetailView
from .owner import OwnerCreateView, OwnerDeleteView, OwnerUpdateView
# Likes:
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

# Post's views:

class PostListView(ListView):
    def get_queryset(self):
        post_list = Post.objects.order_by('-updated_at')[:10]
        return post_list

# ! DO IT!
class PostListViewPlusLike(ListView):
    model = Post
    def get(self, request) :
        post_list = Post.objects.order_by('-updated_at')[:10]
        likes = []
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.liked_posts.values('id')
            # likes = [2, 4, ...] using list comprehension
            likes = [ row['id'] for row in rows ]
        ctx = {'post_list' : thing_list, 'likes': likes}
        return render(request, self.template_name, ctx)    
    
class PostDetailView(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        comments = Comment.objects.filter(post=self.object).order_by('-updated_at')
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form

        # Likes:
        if self.request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = self.request.user.liked_posts.values('id')
            # likes = [2, 4, ...] using list comprehension
            likes = [ row['id'] for row in rows ]
            context['likes'] = likes

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

# Tag's views

class TagList(ListView):
    model = Post
    template_name = 'pages/tag_list.html'

    def get_context_data(self, *args, **kwargs):
        print(self.kwargs, self.args)
        context = super().get_context_data()
        Post_list = Post.objects.filter(tags__slug=self.kwargs['tg_slug'])
        context['post_list'] = Post_list
        return context

# Comment's views:

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Post, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, post=f)
        comment.save()
        return redirect(reverse('pages:post_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "pages/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        post = self.object.post
        return reverse('pages:post_detail', args=[post.id])

# Like's views:

@method_decorator(csrf_exempt, name='dispatch')
class AddLikeView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        a = get_object_or_404(Post, id=pk)
        like_inst = Like(user=request.user, post=a)
        try:
            like_inst.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteLikeView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        t = get_object_or_404(Post, id=pk)
        try:
            like_inst = Like.objects.get(user=request.user, post=t).delete()
        except Like.DoesNotExist as e:
            pass

        return HttpResponse()
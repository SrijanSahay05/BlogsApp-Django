from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)

class PostListview(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10


def about(request):
    return render(request, "blog/about.html", {"title": "About"})


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            post = self.get_object()
            context['comments'] = post.comments.all()  # Fetch comments related to the post
            context['form'] = CommentForm()  # Add the comment form
            return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user  # Assign the logged-in user as the author
            comment.post = post  # Link the comment to the post
            comment.save()
            return redirect('post-detail', pk=post.pk)
        else:
            return self.get(request, *args, **kwargs)  # If the form is not valid, re-render the page



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class UserPostListview(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'

    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post-detail', pk=pk)

@login_required
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
    return redirect('post-detail', pk=pk)

from django.urls import path
from .views import UserPostListview, PostListview, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, like_post, dislike_post
from . import views

urlpatterns = [
    path("", PostListview.as_view(), name="blog-home"),
    path("user/<str:username>", UserPostListview.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:pk>/like/", like_post, name="post-like"),
    path("post/<int:pk>/dislike/", dislike_post, name="post-dislike"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("about/", views.about, name="blog-about"),
]

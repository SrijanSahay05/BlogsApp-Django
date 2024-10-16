from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    dislikes = models.ManyToManyField(User, related_name="post_dislike", blank=True)
    image = models.ImageField(upload_to="post_media", blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date_posted"]

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

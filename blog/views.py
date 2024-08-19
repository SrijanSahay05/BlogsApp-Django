from django.shortcuts import render
from django.http import HttpResponse

posts = [
    {
        "author": "Srijan Sahay",
        "title": "Blog Post 1",
        "content": "First Post content",
        "date_posted": "19/08/2024",
    },
    {
        "author": "Srijan Sahay",
        "title": "Blog Post 2",
        "content": "Second Post content",
        "date_posted": "20/08/2024",
    },
]


def home(request):
    context = {"posts": posts}
    return render(request, "blog/home.html", context)


def about(request):
    return render(request, "blog/about.html", {"title": "About"})

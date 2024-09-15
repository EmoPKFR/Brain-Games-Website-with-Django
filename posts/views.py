from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from . import forms

def posts_list(request):
    posts = Post.objects.all().order_by("-date")
    return render(request, "posts/posts_list.html", {"posts": posts})

def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, "posts/post_page.html", {"post": post})

@login_required(login_url="/users/login/")
def new_post(request):
    if request.method == "POST":
        form = forms.CreatePost(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = request.user
            newpost.save()
            return redirect("posts:list")
    else:
        form = forms.CreatePost()
    return render(request, "posts/new_post.html", {"form": form})

@login_required(login_url="/users/login/")
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Check if the post author is the same as the user
    if post.author == request.user:
        if request.method == "POST":
            # If a POST request is made, delete the post
            post.delete()
            return redirect("posts:list")
        # Otherwise, show the confirmation page
        return render(request, "posts/delete_post.html", {"post": post})
    
    return HttpResponseForbidden("You are not allowed to delete this post.")
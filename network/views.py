from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from network import forms
from .models import Following, User, Post
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == "POST":
        form = forms.PostForm(request.POST)
        if form.is_valid():
            post_message = form.cleaned_data["post_message"]
            new = Post(post_message= post_message, writed_by = request.user)
            new.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html",  {"post_form": forms.PostForm(), "posts":Post.objects.all().order_by('-timestamp') })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url='login')
def profile(request, usernm):
        user_profile = User.objects.get(username=usernm)
        if request.user != user_profile:
            flag = False
            
            if Following.objects.check(influencer=user_profile, follower=request.user):
                flag = True
            return render(request, "network/profile.html", { "follow_flag":flag, "view_profile": User.objects.get(username=user_profile), 
                "posts": Post.objects.filter(writed_by=user_profile).order_by('-timestamp')})
        else:
            return render(request, "network/profile.html", { "follow_flag":"NO!", "view_profile": User.objects.get(username=user_profile), 
                "posts": Post.objects.filter(writed_by=user_profile).order_by('-timestamp')})

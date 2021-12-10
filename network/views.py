from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from network import forms
from .models import Following, User, Post, Like
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.method == "POST":
        form = forms.PostForm(request.POST)
        if form.is_valid():
            post_message = form.cleaned_data["post_message"]
            new = Post(post_message= post_message, writed_by = request.user)
            new.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        all_posts = Post.objects.all().order_by('-timestamp')
        paginator = Paginator(all_posts, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html",  {"post_form": forms.PostForm(), "posts": page_obj})


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
def profile(request, usernm): #requested by username
    try:
        user_profile = User.objects.get(username=usernm) #get the User from db 
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
        
    n_following = Following.objects.filter(follower=user_profile).count() 
    n_follows = Following.objects.filter(influencer=user_profile).count()
    
    return render(request, "network/profile.html", { 
            "n_following":n_following, "n_follows":n_follows,
            "view_profile": User.objects.get(username=user_profile), 
            "posts": Post.objects.filter(writed_by=user_profile).order_by('-timestamp')})

@login_required(login_url='login')
def following(request):

    user = User.objects.get(id=request.user.id)
    following = user.following.all()
    following_users = [follow.influencer for follow in following]
    
    all_posts = Post.objects.filter(writed_by__in=following_users).order_by("-timestamp")

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", { "post_form": forms.PostForm(),
        "posts": page_obj } )

#Endpoint to know if given user is followed by the actual user.
@csrf_exempt
def isFollowing(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid user_id."}, status=404)

    if request.method != "GET":
        return JsonResponse({"error": "It's not GET method! :|"}, status=400)
    else:
        #If user exists, check if is follower
        try:
            Following.objects.get(influencer=user, follower=request.user)
            return JsonResponse({"response": True}, status=200)
        except Following.DoesNotExist:
            return JsonResponse({"response": False}, status=200)

@csrf_exempt
def isLiked(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not existing."}, status=404)

    if request.method != "GET":
        return JsonResponse({"error": "It's not GET method! :|"}, status=400)
    else:
        #If user exists, check if is follower
        try:
            Like.objects.get(like_user=request.user, like_post=post)
            return JsonResponse({"response": True}, status=200)
        except Like.DoesNotExist:
            return JsonResponse({"response": False}, status=200)
            


#Endpoints to Follow/Unfollow action
@csrf_exempt
@login_required(login_url='login')
def action_follow(request, user_id):
    if request.method == "POST":
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid user_id."}, status=400)
        #User exist
        if request.user == user:
            return JsonResponse({"error": "Can not follow yourself"}, status=400)
        #And is not themself
        try:
            Following.objects.get(influencer=user, follower=request.user).delete()
            return JsonResponse({"message": "Unfollow action executed."},status=200)
        except Following.DoesNotExist:
            user_following = Following.objects.create(influencer=user, follower=request.user)
            #user_following.followers.add(request.user)
            user_following.save()
            return JsonResponse({"message": "Follow action executed."},status=200)
        
    return JsonResponse({"message": "Can only post to method"}, status=400)

@csrf_exempt
@login_required(login_url='login')
def edit_post(request, post_id, post_message):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Couldnt edit a NO EXISTING POST."}, status=400)
        if request.user != post.writed_by:
            return JsonResponse({"error": "It`s NOT YOUR POST."}, status=400)
        else:
            post.post_message = post_message
            post.save()
            return JsonResponse({"message": "Post modified successfully."}, status=200)
    return JsonResponse({"error": "Only post method allowed."}, status=400)
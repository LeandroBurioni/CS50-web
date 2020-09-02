from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", { "listings": Listing.objects.all() })

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



class CreateForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50)
    description = forms.CharField(label="Description")
    price = forms.FloatField(label="Initial Bid", min_value=0)
    url_image = forms.URLField(label="URL's Image" , required=False)
    #Category is a choice field

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            url_image = form.cleaned_data["url_image"]
            new = Listing.objects.create(owner=request.user ,title=title, description=description, price=price, url_image=url_image)
            new.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "create_form": CreateForm()})

class CommentForm(forms.Form):
    text = forms.CharField()

def listing(request,listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            new = Comment(owner=request.user, auction=listing_id, text=text)
            new.save()
            return HttpResponseRedirect(reverse("listing", listing_id))
    else:
        return render(request, "auctions/auction.html", {
            "comment_form": CommentForm(),
            "listing": Listing.objects.get(id=listing_id),
            #"comments":  Comment.objects.filter(auction=listing_id)
            })
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from auctions import forms

from .models import User, Listing, Bid, Comment

def index(request):
    return render(request, "auctions/index.html", { "listings": Listing.objects.filter(open=True)})

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

def create(request):
    if request.method == "POST":
        form = forms.CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            url_image = form.cleaned_data["url_image"]
            category = form.cleaned_data["category"]
            new = Listing.objects.create(owner=request.user ,title=title, description=description, price=price, url_image=url_image, category=category)
            new.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html", {
            "create_form": forms.CreateForm()})

def listing(request,listing_id):
    if request.method == "POST":
        auction=Listing.objects.get(pk=listing_id)
        if 'comment' in request.POST:
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data["text"]
                new = Comment(author=request.user, auction=auction, text=text)
                new.save()
                return redirect("listing", listing_id)
        elif 'close' in request.POST:
            auction.open=False
            auction.save()
            return redirect("listing", listing_id)
        elif 'watchlist' in request.POST:
            #CheckBox to add or drop this auction from the user's watchlist
            pass           
    else:
        lists = get_object_or_404(Listing, pk=listing_id)
        return render(request, "auctions/auction.html", {
            "comment_form": forms.CommentForm(),
            "listing": lists})

def category(request, cat):
    return render(request, "auctions/index.html", { "listings": Listing.objects.filter(open=True, category=cat) })
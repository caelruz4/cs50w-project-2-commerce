from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    # send all active listings
    listings = Listing.objects.filter(active=True)
    context = {'listings': listings}
    return render(request, 'auctions/index.html', context)


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
                "message": "Invalid username and/or password.",
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

# view listing info
@login_required
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    on_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    highest_bid = get_highest_bid(listing_id)
    comments = Comment.objects.filter(listing=listing)
    is_owner = listing.owner == request.user
    context = {
        'listing': listing,
        'highest_bid': highest_bid,
        'on_watchlist': on_watchlist,
        'comments': comments,
        'is_owner': is_owner,
        "active": listing.active,

    }
    return render(request, 'auctions/listing.html', context)

# Funcion para tener la oferta más alta de una subasta
def get_highest_bid(listing_id):
    bids = Bid.objects.filter(listing=listing_id).order_by('-amount')
    if len(bids) > 0:
        return bids[0].amount
    else:
        return 0
    
# make a bid
@login_required
def bid(request, listing_id):
    if request.method == "POST":
        amount = float(request.POST['amount'])
        listing = get_object_or_404(Listing, pk=listing_id)
        user = request.user
        # initial price
        initial_price = listing.initial_price
        highest_bid = get_highest_bid(listing_id)
        # validate bid
        if amount <= highest_bid or amount < initial_price:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "highest_bid": highest_bid,
                "message": "Your bid must be higher than the current highest bid."
            })
        else:
            # save bid
            bid = Bid.objects.create(amount=amount, listing=listing, user=user)
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    # redirect to listing
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# add to watchlist
@login_required
def add_watchlist(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        user = request.user
        watchlist = Watchlist.objects.create(listing=listing, user=user)
        watchlist.save()
        # return to listing and 
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    # redirect to listing
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# remove from watchlist
@login_required
def remove_watchlist(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        user = request.user
        watchlist = Watchlist.objects.get(listing=listing, user=user)
        watchlist.delete()
        # return to listing and 
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    # redirect to listing
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# send comment
@login_required
def comment(request, listing_id):
    if request.method == "POST":
        content = request.POST['content']
        listing = get_object_or_404(Listing, pk=listing_id)
        user = request.user
        comment = Comment.objects.create(content=content, listing=listing, user=user)
        comment.save()
        # return to listing and 
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    # redirect to listing
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# close listing
@login_required
def close(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        listing.active = False
        listing.save()
        # return to listing and 
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    # redirect to listing
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# open
@login_required
def open(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        listing.active = True
        listing.save()
        # return to listing and 
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    # redirect to listing
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from .forms import ListingForm
from django.contrib.auth.decorators import user_passes_test


def user_is_authenticated(user):
    return user.is_authenticated

login_required_custom = user_passes_test(
    user_is_authenticated, login_url='login'
)

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
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    try:
        on_watchlist = Watchlist.objects.filter(listing=listing, user=request.user).exists()
    except:
        on_watchlist = False

    highest_bid = get_highest_bid(listing_id)
    comments = Comment.objects.filter(listing=listing)
    is_owner = listing.owner == request.user
    winner = None
    if not listing.active:
        check_win = Bid.objects.filter(listing=listing).order_by('-amount').first().user
        if check_win == request.user:
            winner = check_win
    else:
        winner = None

    context = {
        'listing': listing,
        'highest_bid': highest_bid,
        'on_watchlist': on_watchlist,
        'comments': comments,
        'is_owner': is_owner,
        "active": listing.active,
        "winner": winner

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
@login_required_custom
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
            messages.error(request, "Your bid must be higher than the current highest bid.")
            return redirect('listing', listing_id=listing_id)
        
        else:
            # save bid
            bid = Bid.objects.create(amount=amount, listing=listing, user=user)
            bid.save()
            # redirect to listing and
            messages.success(request, f"You have successfully made your bid!")
            return redirect('listing', listing_id=listing_id)
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

@login_required_custom
def remove_watchlist(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        user = request.user
        watchlist = Watchlist.objects.get(listing=listing, user=user)
        watchlist.delete()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# send comment
@login_required_custom
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
@login_required_custom
def close(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        listing.active = False
        listing.save()
        # return to listing and 
        messages.success(request, 'This listing has been closed')
        return redirect('listing', listing_id=listing_id)


    # redirect to listing
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# open
@login_required_custom
def open(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        listing.active = True
        listing.save()
        # return to listing and 
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    # redirect to listing
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

# all categories
def categories(request):
    categories = Category.objects.all()
    # amount of elements in that category
    for category in categories:
        category.amount = Listing.objects.filter(category=category).count()

    context = {
        "categories": categories
    }
    return render(request, "auctions/categories.html", context)

# category
def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category)
    context = {
        "category": category,
        "listings": listings
    }
    return render(request, "auctions/category.html", context)

# watchlist
@login_required_custom

def watchlist(request):
    user = request.user
    watchlists = Watchlist.objects.filter(user=user)
    # print every listing on watchlist
    context = {
        "watchlist": watchlists
    }
    return render(request, "auctions/watchlist.html", context)

# create listing route
@login_required_custom
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
        else:
            # print errors
            print(form.errors)
        
    form = ListingForm()
    categories = Category.objects.all()
    context = {
            "form": form,
            "categories": categories
        }
    return render(request, "auctions/create.html", context)

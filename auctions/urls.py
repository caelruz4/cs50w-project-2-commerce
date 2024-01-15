from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path("create_listing", views.create_listing, name="create_listing"),
    # path("categories", views.categories, name="categories"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("add-watchlist/<int:listing_id>", views.add_watchlist, name="add-watchlist"),
    path("remove-watchlist/<int:listing_id>", views.remove_watchlist, name="remove-watchlist"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("open/<int:listing_id>", views.open, name="open"),

]

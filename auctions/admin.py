from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)

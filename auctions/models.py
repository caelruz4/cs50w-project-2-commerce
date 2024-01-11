from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=255, null=False)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='auctions')
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, null=False)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True, default="https://react.semantic-ui.com/images/image-16by9.png")
    def __str__(self):
        return f"{self.title} - {self.owner}"

# bids
class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    def __str__(self):
        return f"{self.user} - {self.listing} - {self.amount}"
    
# comments
class Comment(models.Model):
    content = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    def __str__(self):
        return f"{self.user} - {self.listing} - {self.content}"

# watchlist
class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    def __str__(self):
        return f"{self.user} - {self.listing}"
    
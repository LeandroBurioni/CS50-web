from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)

    def get_queryset(self):
        return Category.objects.all()
        
    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField(blank=True)
    url_image = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, related_name="listing_category")
    open = models.BooleanField(default=True) #True if the auction is opened
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="own_auctions") #Deleting a user, all the auctions will be deleted.
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist_content")
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="win_auctions", null=True)

    def __str__(self):
        return f"#{self.id}: {self.title} ${self.price}"
    
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments") 
    text = models.TextField(help_text="Make a comment here.")
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} said {self.text}"

class Bid(models.Model):
    price = models.IntegerField()
    #date = models.DateTimeField(auto_now=True)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, default=Listing, related_name="bids") 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bids_made" ) #Each auction have a owner, a owner can have many auctions 

    def __str__(self):  
        return f"{self.price}"

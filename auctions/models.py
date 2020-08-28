from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

#class Inherence(models.Model):

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    #Optional Fields
    url_image = models.URLField(blank=True)
    #category
    open = models.BooleanField(default=True) #True if the auction is opened
    
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Deleting a user, all the auctions will be deleted.

def __str__(self):
    return f"#{self.id}: {self.title} ${self.price}"
    
class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField
    date = models.DateTimeField(auto_now=True)
    #owner = models.ManyToManyRel(User, related_name="bids") #Each auction have a owner, a owner can have many auctions 

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    #owner = models.ManyToOneRel(User, related_name="comments")
    commentary = models.TextField
    date = models.DateTimeField(auto_now=True)
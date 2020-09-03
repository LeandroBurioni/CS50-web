from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass
 
#I can do Inheritance for DRY with owner and date fields but dont know a way to use related_name with it.

class Listing(models.Model):
    title = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    url_image = models.URLField(blank=True)
    
    open = models.BooleanField(default=True) #True if the auction is opened
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Deleting a user, all the auctions will be deleted.
    CAT = (
        ('NA', 'Not Category Selected'),
        ('w', 'Weareable'),
        ('n', 'new'),
        ('u', 'used'),
    )
    category = models.CharField(max_length=2, choices=CAT, blank=True, default='NA', )

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
    date = models.DateTimeField(auto_now=True)
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, default=Listing) 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name="bids") #Each auction have a owner, a owner can have many auctions 

    def __str__(self):
        return self.price


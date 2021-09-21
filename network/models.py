from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    writed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted", null=False)
    post_message = models.TextField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} {self.writed_by} ${self.post_message} // {self.timestamp} "

#class Like(models.Model):
#    like_user 
#    like_post

#class Following(models.Model):
#   follower = 
#   



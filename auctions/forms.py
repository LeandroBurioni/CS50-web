from django import forms
from .models import Category,Listing

class CreateForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50)
    description = forms.CharField(label="Description")
    price = forms.FloatField(label="Initial Bid", min_value=0)
    url_image = forms.URLField(label="URL's Image" , required=False)
    category = forms.ModelChoiceField(queryset= Category.objects.all(), required=False)

class BidForm(forms.Form):
    new_bid = forms.FloatField(label="")

class CommentForm(forms.Form):
    text = forms.CharField()
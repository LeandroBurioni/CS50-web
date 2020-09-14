from django import forms

class CreateForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50)
    description = forms.CharField(label="Description")
    price = forms.FloatField(label="Initial Bid", min_value=0)
    url_image = forms.URLField(label="URL's Image" , required=False)
    category = forms.CharField(label="Category", required=False)

class CommentForm(forms.Form):
    text = forms.CharField()
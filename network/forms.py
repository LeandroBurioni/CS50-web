from django import forms
#from .models import Post


class PostForm(forms.Form):
    post_message = forms.CharField(label="", max_length= 15 ,widget=forms.TextInput(attrs={'placeholder': 'Que hay de nuevo, viejo?'}))
    
#class LikeForm(forms.Form):

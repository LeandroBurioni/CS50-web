from django import forms

class PostForm(forms.Form):
    post_message = forms.CharField(label="", max_length= 150 ,widget=forms.Textarea(attrs={'placeholder': 'What`s up?',}))
    

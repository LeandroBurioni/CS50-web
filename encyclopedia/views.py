from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2, random
from . import util
from django import forms

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request, title):
    if util.get_entry(title):
        entry_html = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", 
            {"entry_html":entry_html, "entry_title": title} )
    else:
        entry_html = "<h1> Not founded element!</h1><p>May be you can create an entry... Thanks!</p>"
        return render(request, "encyclopedia/entry.html", 
            {"entry_html": entry_html, "entry_title": "Not Found!"})

def rand(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return redirect("encyclopedia:search", entry)

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry's title")
    entry_md = forms.CharField(widget=forms.Textarea)

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry_md = form.cleaned_data["entry_md"]
            if util.is_repeated(title):
                entry_html = "<h1> This entry already exists!</h1><p>Please search and add the information you know... Thanks!</p>"
                return render(request, "encyclopedia/entry.html", 
                        {"entry_html": entry_html, "entry_title": "Repeated!"})
            else:
                util.save_entry(title, entry_md)
                return redirect("encyclopedia:index")                        
    else: 
        return render(request, "encyclopedia/new.html", 
            {"form": NewEntryForm() })

def results(request): #it was very dificult, i tried to use Django's form but i cant
    if request.method == "POST": #i understand that for search form is better to use GET method but i dont know how
            title = request.POST['searched'] #this line is not very good for me, but works.
            if util.is_repeated(title):
                return redirect("encyclopedia:search", title)
    else:
        entry_html = "<h1> What are you doing here?</h1><p>Please, try again... Thanks!</p>"
        return render(request, "encyclopedia/entry.html", 
                        {"entry_html": entry_html, "entry_title": "Nothing here!"})

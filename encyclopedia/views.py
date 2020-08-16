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
            repeated = False
            title = form.cleaned_data["title"]
            entry_md = form.cleaned_data["entry_md"]
            entries = util.list_entries()
            for entry in entries:
                if title == entry:
                    repeated = True
            if repeated: #validate is not repeated and save the entry
                entry_html = "<h1> This entry already exists!</h1><p>Please search and add the information you know... Thanks!</p>"
                return render(request, "encyclopedia/entry.html", 
                        {"entry_html": entry_html, "entry_title": "Repeated!"})
            else:
                util.save_entry(title, entry_md)
                return redirect("encyclopedia:index")                        
    else:
        return render(request, "encyclopedia/new.html", 
            {"form": NewEntryForm() })


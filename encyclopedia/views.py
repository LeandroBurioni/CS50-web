from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import markdown2, random
from . import util

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

from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request, title):
    entry_html = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "entry_html":entry_html, "entry_title": title
    })

from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
    })

def search(request, entry):
    if entry == "CSS":
        return render(request, "encyclopedia/css.html", {"entry": util.get_entry("css")})
    elif entry == "Django":
        return render(request, "encyclopedia/django.html", {"entry": util.get_entry("django")})
    elif entry == "Git":
        return render(request, "encyclopedia/git.html", {"entry": util.get_entry("Git")})
    elif entry == "HTML":
        return render(request, "encyclopedia/html.html", {"entry": util.get_entry("HTML")})
    elif entry == "Python":
        return render(request, "encyclopedia/python.html", {"entry": util.get_entry("Python")})
    else:
        return render(request, "encyclopedia/notfound.html",{"entry": entry})
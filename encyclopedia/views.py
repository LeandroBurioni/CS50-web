from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), 
    })

def css(request):
    return render(request, "encyclopedia/css.html", {
        "entry": util.get_entry("css")
    })

def django(request):
    return render(request, "encyclopedia/django.html", {
        "entry": util.get_entry("django")
    })

def git(request):
    return render(request, "encyclopedia/git.html", {
        "entry": util.get_entry("Git")
    })

def html(request):
    return render(request, "encyclopedia/html.html", {
        "entry": util.get_entry("HTML")
    })

def python(request):
    return render(request, "encyclopedia/python.html", {
        "entry": util.get_entry("Python")
    })

def notfound(request, search):
    return render(request, "encyclopedia/notfound.html",{
        "search": search
    })
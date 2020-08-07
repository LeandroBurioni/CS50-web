from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def css(request):
    return render(request, "encyclopedia/css.html", {
        "entry": util.get_entry("CSS")
    })

def django(request):
    return render(request, "encyclopedia/django.html", {
        "entry": util.get_entry("Django")
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

def noesta(request, noesta):
    return render(request, "encyclopedia/noesta.html",{
        "noesta": noesta
    })
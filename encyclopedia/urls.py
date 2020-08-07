from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/css", views.css, name="css"),
    path("wiki/django", views.django, name="django"),
    path("wiki/git", views.git, name="git"),
    path("wiki/html", views.html, name="html"),
    path("wiki/python", views.python, name="python"),
    path("wiki/<str:noesta>", views.noesta, name="noesta")

    
]

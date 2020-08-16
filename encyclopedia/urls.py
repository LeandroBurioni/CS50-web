from django.urls import path

from . import views

app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.rand, name="rand"),
    path("new/", views.new, name="new"),
    path("wiki/<str:title>", views.search, name="search"),

]

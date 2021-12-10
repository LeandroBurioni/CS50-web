
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:usernm>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    #API's route
    path("isFollow/<int:user_id>", views.isFollowing, name="isFollowing"),
    path("isLike/<int:post_id>", views.isLiked, name="isLiked"),
    path("actFollow/<int:user_id>", views.action_follow, name="Follow"),
    path("edit/<int:post_id>/<str:message>", views.edit_post, name="Edit")

]

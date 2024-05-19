from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/signup", views.UserSignup.as_view(), name="user-signup")
]

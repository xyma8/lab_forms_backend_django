from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/signup", views.UserSignup.as_view(), name="user-signup"),
    path("users/login", views.UserLogin.as_view(), name="user-login"),
    path("users/data", views.GetUserDataByToken.as_view(), name="user-data-by-token"),
    path("users/theme", views.GetUserTheme.as_view(), name="user-theme"),
    path("users/theme/change", views.ChangeUserTheme.as_view(), name="user-theme-change"),
    path("recaptcha", views.ReCaptchaVerification.as_view(), name="recaptcha-verification")
]

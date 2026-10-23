from django.urls import path
from .views import register_user, login_user, logout_view

app_name = "accounts_app"
urlpatterns = [
    path("login/", login_user, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_user, name="register_page"),
]
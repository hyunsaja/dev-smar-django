
from django.urls import path, include

from core.views import Login
from core.views import Signup
from core.views import Logout

urlpatterns = [
    path("Login/", Login.as_view(), name="Login"),
    path("Signup/", Signup.as_view(), name="Signup"),
    path("Logout/", Logout.as_view(), name="Logout"),
]
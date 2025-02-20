from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api_auth.views import CreateUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("token/", obtain_auth_token, name="token"),
]

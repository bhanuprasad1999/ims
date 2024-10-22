from django.urls import path, include

from user.views import login_user, register_user


urlpatterns = [
    path('register/', register_user),
    path('login/', login_user)
]
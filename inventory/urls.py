

from django.urls import path
from inventory.views import ping

urlpatterns = [
    path('ping/', ping)
]

from django.urls import path
from .views import index, details

urlpatterns = [
    path("", index, name="index"),
    path("<str:account_id>", details, name="account_details")
]

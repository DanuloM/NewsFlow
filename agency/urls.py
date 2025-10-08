from django.urls import path
from agency.views import index

app_name = "agency"

urlpatterns = [
    path("", index, name="index"),
]

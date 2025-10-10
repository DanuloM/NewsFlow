from django.urls import path
from agency.views import index, NewspaperListView, NewspaperDetailView

app_name = "agency"

urlpatterns = [
    path("", index, name="index"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>", NewspaperDetailView.as_view(), name="newspaper-detail"),
]

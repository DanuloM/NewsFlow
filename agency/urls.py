from django.urls import path
from agency.views import (
    index,
    NewspaperListView,
    NewspaperDetailView,
    TopicListView,
    RedactorListView,
    RedactorDetailView,
    NewspaperCreateView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
    RedactorCreateView,
    RedactorUpdateView,
    RedactorDeleteView, ToggleRedactorAssignmentView,
)

app_name = "agency"

urlpatterns = [
    path("", index, name="index"),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspapers/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspaper-delete"),
    path("topic/", TopicListView.as_view(), name="topic-list"),
    path("topic/create/", TopicCreateView.as_view(), name="topic-create"),
    path("topic/<int:pk>/update/", TopicUpdateView.as_view(), name="topic-update"),
    path("topic/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic-delete"),
    path("redactors/", RedactorListView.as_view(), name="redactor-list"),
    path("redactors/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"),
    path("redactors/create", RedactorCreateView.as_view(), name="redactor-create"),
    path("redactors/<int:pk>/update", RedactorUpdateView.as_view(), name="redactor-update"),
    path("redactors/<int:pk>/delete", RedactorDeleteView.as_view(), name="redactor-delete"),
    path("newspapers/<int:pk>/toggle", ToggleRedactorAssignmentView.as_view(), name="toggle-redactor"),
]
